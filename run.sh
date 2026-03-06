#!/bin/bash
# ============================================================================
# Lead Manager QA Automation - One-Click Test Runner
# ============================================================================
# Usage: ./run.sh [options]
#
# Test Selection:
#   --ui              Run only UI tests
#   --api             Run only API tests
#   --smoke           Run only smoke tests
#   --headed          Run UI tests in headed mode (visible browser)
#
# Environment:
#   --env=lower       Target lower/dev-QA environment (default)
#   --env=preprod     Target pre-production environment
#   --env=prod        Target production environment
#
# Execution:
#   --parallel        Run tests in parallel (auto workers)
#   --workers=N       Run tests in parallel with N workers
#   --report          Open HTML report after tests
#   --port=NUMBER     Allure server port (default: 5050)
#   --help            Show this help message
#
# Examples:
#   ./run.sh                          Run all tests (lower env)
#   ./run.sh --env=preprod            Run all tests on pre-prod
#   ./run.sh --api --env=prod         Run API tests on prod
#   ./run.sh --ui --headed            Run UI tests visibly
#   ./run.sh --api --parallel         Run API tests in parallel
#   ./run.sh --smoke --workers=4      Run smoke tests with 4 workers
#   ./run.sh --report --port=8080     Open Allure on port 8080
# ============================================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
REPORTS_DIR="$PROJECT_DIR/reports"

# Create timestamped report folder for this run
RUN_TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RUN_DIR="$REPORTS_DIR/run_$RUN_TIMESTAMP"
ALLURE_RESULTS="$RUN_DIR/allure-results"
ALLURE_REPORT="$RUN_DIR/allure-report"
PYTEST_HTML="$RUN_DIR/report.html"
ALLURE_PORT="${ALLURE_PORT:-5050}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}============================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}============================================${NC}\n"
}

print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
print_error()   { echo -e "${RED}✗ $1${NC}"; }

show_help() {
    grep "^#" "$0" | grep -v "^#!/" | sed 's/^# \{0,1\}//'
    exit 0
}

# ---- Parse Arguments ----
RUN_UI=false
RUN_API=false
RUN_SMOKE=false
HEADED=false
OPEN_REPORT=false
PARALLEL=false
WORKERS="auto"
TARGET_ENV="lower"
PYTEST_ARGS=""

for arg in "$@"; do
    case $arg in
        --ui)           RUN_UI=true ;;
        --api)          RUN_API=true ;;
        --smoke)        RUN_SMOKE=true ;;
        --headed)       HEADED=true ;;
        --report)       OPEN_REPORT=true ;;
        --parallel)     PARALLEL=true ;;
        --workers=*)    PARALLEL=true; WORKERS="${arg#--workers=}" ;;
        --env=*)        TARGET_ENV="${arg#--env=}" ;;
        --port=*)       ALLURE_PORT="${arg#--port=}" ;;
        --help)         show_help ;;
        *)              PYTEST_ARGS="$PYTEST_ARGS $arg" ;;
    esac
done

# Default: run all tests if none specified
if [ "$RUN_UI" = false ] && [ "$RUN_API" = false ] && [ "$RUN_SMOKE" = false ]; then
    RUN_UI=true
    RUN_API=true
fi

# ---- Step 1: Setup Python Virtual Environment ----
print_header "Setting Up Environment"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

source "$VENV_DIR/bin/activate"
print_success "Virtual environment activated"

# ---- Step 2: Install Dependencies ----
echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r "$PROJECT_DIR/requirements.txt"
print_success "Dependencies installed"

# ---- Step 3: Install Playwright Browsers ----
if [ "$RUN_UI" = true ]; then
    echo "Installing Playwright browsers..."
    python -m playwright install chromium --with-deps 2>/dev/null || python -m playwright install chromium
    print_success "Playwright browsers ready"
fi

# ---- Step 4: Create Timestamped Report Directories ----
mkdir -p "$RUN_DIR/screenshots"
mkdir -p "$ALLURE_RESULTS"
print_success "Report folder: $RUN_DIR"

# ---- Step 5: Set Environment Variables ----
export ENV="$TARGET_ENV"
if [ "$HEADED" = true ]; then
    export HEADLESS=false
fi

# ---- Step 6: Build Pytest Arguments ----
print_header "Running Tests [ENV: $TARGET_ENV]"
echo -e "  Environment : ${YELLOW}$TARGET_ENV${NC}"

MARKER_ARGS=""
if [ "$RUN_SMOKE" = true ]; then
    MARKER_ARGS="-m smoke"
    echo -e "  Test scope  : ${YELLOW}smoke${NC}"
elif [ "$RUN_UI" = true ] && [ "$RUN_API" = false ]; then
    MARKER_ARGS="-m ui"
    echo -e "  Test scope  : ${YELLOW}ui${NC}"
elif [ "$RUN_API" = true ] && [ "$RUN_UI" = false ]; then
    MARKER_ARGS="-m api"
    echo -e "  Test scope  : ${YELLOW}api${NC}"
else
    echo -e "  Test scope  : ${YELLOW}all${NC}"
fi

# Parallel execution flag
PARALLEL_ARGS=""
if [ "$PARALLEL" = true ]; then
    # UI tests cannot run in parallel (single browser session per test)
    if [ "$RUN_UI" = true ] && [ "$RUN_API" = false ]; then
        print_warning "UI-only run: parallel execution disabled (Playwright requires serial UI tests)"
    else
        PARALLEL_ARGS="-n $WORKERS"
        echo -e "  Parallel    : ${YELLOW}yes (workers: $WORKERS)${NC}"
    fi
fi
echo ""

# ---- Step 7: Run Tests ----
cd "$PROJECT_DIR"
python -m pytest $MARKER_ARGS $PARALLEL_ARGS $PYTEST_ARGS \
    --env="$TARGET_ENV" \
    --alluredir="$ALLURE_RESULTS" \
    --html="$PYTEST_HTML" \
    --self-contained-html \
    || true

# ---- Step 8: Generate & Serve Allure Report ----
if [ -d "$ALLURE_RESULTS" ] && [ "$(ls -A $ALLURE_RESULTS 2>/dev/null)" ]; then
    if command -v allure &>/dev/null; then
        echo "Generating Allure HTML report..."
        allure generate "$ALLURE_RESULTS" --clean -o "$ALLURE_REPORT" 2>/dev/null
        print_success "Allure Report generated: $ALLURE_REPORT/index.html"
        
        # Create symlink to latest for convenience
        ln -sfn "$ALLURE_REPORT" "$REPORTS_DIR/latest" 2>/dev/null || true
        
        if [ "$OPEN_REPORT" = true ]; then
            print_header "Opening Allure Report in Browser"
            echo "Starting Allure server on http://localhost:${ALLURE_PORT} ..."
            echo "Press Ctrl+C to stop the server"
            echo ""
            
            # Kill any existing process on the port
            lsof -ti:${ALLURE_PORT} | xargs kill 2>/dev/null || true
            sleep 1
            
            # Start allure serve in background and open browser
            (allure serve "$ALLURE_RESULTS" -p ${ALLURE_PORT} &) 
            sleep 3
            open http://localhost:${ALLURE_PORT}
            
            # Keep script running until user interrupts
            echo "Allure server running. Press Ctrl+C to stop..."
            wait
        fi
    else
        print_warning "allure CLI not found. Install via: brew install allure"
        print_warning "Then run: allure generate $ALLURE_RESULTS --clean -o $ALLURE_REPORT"
    fi
fi

# ---- Step 9: Report Summary ----
print_header "Test Execution Complete"

if [ -f "$PYTEST_HTML" ]; then
    print_success "pytest HTML  : $PYTEST_HTML"
    echo -e "  Open with  : ${YELLOW}open $PYTEST_HTML${NC}"
fi

if [ -f "$ALLURE_REPORT/index.html" ]; then
    print_success "Allure HTML  : $ALLURE_REPORT/index.html"
    echo -e "  View with  : ${YELLOW}allure serve $ALLURE_RESULTS${NC}"
    echo -e "  Or open    : ${YELLOW}open $ALLURE_REPORT/index.html${NC}"
fi

print_success "All reports  : $RUN_DIR"
print_success "Latest link  : $REPORTS_DIR/latest -> $ALLURE_REPORT"

if [ "$OPEN_REPORT" = false ] || [ -z "$OPEN_REPORT" ]; then
    # Don't auto-open unless --report flag was used
    :  # no-op
fi

deactivate 2>/dev/null || true
print_success "Done!"
