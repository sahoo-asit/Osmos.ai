# Part 1: Manual Test Cases — Login → Create Lead → List Lead

## 1. Login Functionality

### 1.1 Positive Scenarios

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-L01 | Admin login with valid credentials | App is accessible, user is on login page | 1. Enter email: `admin@company.com` 2. Enter password: `Admin@123` 3. Click "Sign in" | User is redirected to `/leads` dashboard. Email and role "Administrator" displayed in header. |
| TC-L02 | Manager login with valid credentials | App is accessible, user is on login page | 1. Enter email: `qa@company.com` 2. Enter password: `password123` 3. Click "Sign in" | User is redirected to leads dashboard with "Manager" role badge. |
| TC-L03 | Viewer login with valid credentials | App is accessible, user is on login page | 1. Enter email: `tester@company.com` 2. Enter password: `Test@456` 3. Click "Sign in" | User is redirected to leads dashboard with "Viewer" role badge. Read-only access. |
| TC-L04 | Login persists on page refresh | User is logged in | 1. Refresh the browser page | User remains on the leads dashboard without being redirected to login. |

### 1.2 Negative Scenarios

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-L05 | Login with wrong password | User is on login page | 1. Enter email: `admin@company.com` 2. Enter password: `wrongpass` 3. Click "Sign in" | Error message displayed (e.g., "Invalid credentials"). User remains on login page. |
| TC-L06 | Login with non-existent email | User is on login page | 1. Enter email: `nobody@company.com` 2. Enter password: `Admin@123` 3. Click "Sign in" | Error message displayed. User remains on login page. |
| TC-L07 | Login with empty email field | User is on login page | 1. Leave email empty 2. Enter password: `Admin@123` 3. Click "Sign in" | Validation error or HTML5 required field validation prevents submission. |
| TC-L08 | Login with empty password field | User is on login page | 1. Enter email: `admin@company.com` 2. Leave password empty 3. Click "Sign in" | Validation error or HTML5 required field validation prevents submission. |
| TC-L09 | Login with both fields empty | User is on login page | 1. Leave both fields empty 2. Click "Sign in" | Validation errors shown. User stays on login page. |
| TC-L10 | Login with invalid email format | User is on login page | 1. Enter email: `not-an-email` 2. Enter password: `Admin@123` 3. Click "Sign in" | Validation error for invalid email format. |

### 1.3 Edge Cases

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-L11 | Login with leading/trailing spaces in email | User is on login page | 1. Enter email: `  admin@company.com  ` 2. Enter password: `Admin@123` 3. Click "Sign in" | Login succeeds (spaces trimmed) or appropriate error is shown. |
| TC-L12 | Login with case-different email | User is on login page | 1. Enter email: `ADMIN@COMPANY.COM` 2. Enter password: `Admin@123` 3. Click "Sign in" | Behavior documented — login should be case-insensitive for email or show clear error. |
| TC-L13 | SQL injection in email field | User is on login page | 1. Enter email: `' OR 1=1 --` 2. Enter password: `anything` 3. Click "Sign in" | Login fails. No data leakage or server error. |
| TC-L14 | XSS script in password field | User is on login page | 1. Enter email: `admin@company.com` 2. Enter password: `<script>alert('xss')</script>` 3. Click "Sign in" | Login fails gracefully. Script is not executed. |
| TC-L15 | Accessing leads page without login | User is not logged in | 1. Navigate directly to `/leads` URL | User is redirected to login page. |

---

## 2. Create Lead Functionality

### 2.1 Positive Scenarios

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-C01 | Create lead with required fields only | User is logged in as Admin, on leads page | 1. Click "Create Lead" 2. Enter Name: `John Doe` 3. Enter Email: `john@test.com` 4. Click "Create Lead" (submit) | Lead is created. Dialog closes. Lead appears in the table. Success notification shown. |
| TC-C02 | Create lead with all fields populated | User is logged in, on leads page | 1. Click "Create Lead" 2. Fill: Name, Email, Phone, Company, Job Title 3. Select: Industry, Source, Priority, Status 4. Enter Deal Value, Notes 5. Toggle Qualified & Email Opt-in 6. Submit | Lead is created with all fields saved correctly. Appears in table with correct data. |
| TC-C03 | Create lead with different priority levels | User is logged in | 1. Create lead with Priority = Low 2. Create lead with Priority = High 3. Create lead with Priority = Critical | Each lead is created with the correct priority badge displayed in the table. |
| TC-C04 | Create lead with different statuses | User is logged in | 1. Create lead with Status = New 2. Create lead with Status = Contacted 3. Create lead with Status = Qualified | Each lead is created with the correct status badge in the table. |

### 2.2 Negative Scenarios

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-C05 | Submit create lead form with empty name | User is logged in, create lead dialog open | 1. Leave Name empty 2. Enter valid Email 3. Click Submit | Validation error for Name field. Form is not submitted. |
| TC-C06 | Submit create lead form with empty email | User is logged in, create lead dialog open | 1. Enter valid Name 2. Leave Email empty 3. Click Submit | Validation error for Email field. Form is not submitted. |
| TC-C07 | Submit with invalid email format | User is logged in, create lead dialog open | 1. Enter Name: `Test User` 2. Enter Email: `invalid-email` 3. Click Submit | Validation error for invalid email format. |
| TC-C08 | Submit with all fields empty | User is logged in, create lead dialog open | 1. Clear all fields 2. Click Submit | Validation errors shown for required fields (Name, Email). |
| TC-C09 | Create lead with duplicate email | User is logged in, lead with email `dup@test.com` exists | 1. Click Create Lead 2. Enter Name and email: `dup@test.com` 3. Submit | Either error for duplicate email or lead is created (document behavior). |

### 2.3 Edge Cases & Validation

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-C10 | Create lead with very long name (255+ chars) | User is logged in, dialog open | 1. Enter a name with 300 characters 2. Fill email 3. Submit | Lead is created with truncated name, or validation error for max length. |
| TC-C11 | Create lead with special characters in name | User is logged in, dialog open | 1. Enter Name: `José María O'Brien-Smith` 2. Enter valid email 3. Submit | Lead is created successfully. Special characters are preserved. |
| TC-C12 | Create lead with XSS in name field | User is logged in, dialog open | 1. Enter Name: `<script>alert('xss')</script>` 2. Enter valid email 3. Submit | Lead is created with sanitized name. Script is not executed. |
| TC-C13 | Cancel create lead dialog | User is logged in, dialog open with data filled | 1. Fill some fields 2. Click Cancel or X button | Dialog closes. No lead is created. Table remains unchanged. |
| TC-C14 | Close dialog by clicking outside | User is logged in, dialog open | 1. Click outside the dialog overlay | Dialog closes without creating a lead (or remains open — document behavior). |
| TC-C15 | Create lead with negative deal value | User is logged in, dialog open | 1. Enter Name, Email 2. Enter Deal Value: `-5000` 3. Submit | Validation error for negative value, or lead is created (document behavior). |

---

## 3. List Lead Functionality

### 3.1 Positive Scenarios

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-LL01 | Verify leads table displays after login | User just logged in | 1. Observe the leads page | Table is visible with columns: ID, Name, Email, Company, Priority, Status, Deal Value, Source, Created, Actions. |
| TC-LL02 | Verify pagination info is displayed | Leads exist in the system | 1. Observe pagination area | Text like "Showing 1 to 10 of 20 leads" is displayed. |
| TC-LL03 | Navigate to next page | More than 10 leads exist | 1. Click "Next" button | Table updates to show next set of leads. Pagination text updates. |
| TC-LL04 | Navigate to previous page | User is on page 2+ | 1. Click "Previous" button | Table shows the previous set of leads. |
| TC-LL05 | Search leads by name | Leads exist | 1. Type a known lead name in search box | Table filters to show matching leads. |
| TC-LL06 | Search leads by email | Leads exist | 1. Type a known email in search box | Table filters to show matching leads. |
| TC-LL07 | Filter leads by status | Leads with various statuses exist | 1. Click status dropdown 2. Select "Contacted" | Only leads with "Contacted" status are shown. |
| TC-LL08 | Newly created lead appears in table | Lead just created | 1. Create a new lead 2. Observe the table | New lead appears in the list (may need to refresh or navigate). |

### 3.2 View Lead Details

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-LL09 | View lead details via eye icon | User is logged in, leads exist | 1. Click the eye icon (👁) in Actions column | Lead Details dialog opens showing: Lead ID, Status badge, Priority badge, Name, Email, Phone, Qualification Status, Email Opt-In, Created At, Last Updated. |
| TC-LL10 | View lead with all fields populated | Lead exists with all fields filled | 1. Click eye icon on that lead | All fields display correctly including Company, Job Title, Industry, Source, Deal Value, Notes. |
| TC-LL11 | View lead with minimal fields | Lead exists with only Name & Email | 1. Click eye icon | Dialog shows Name, Email. Other fields show "Not provided" or empty. |
| TC-LL12 | Close view dialog via X button | View dialog is open | 1. Click X button | Dialog closes. User returns to leads list. |
| TC-LL13 | Close view dialog by clicking outside | View dialog is open | 1. Click outside the dialog | Dialog closes (or stays open - document behavior). |

### 3.3 Edit Lead

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-LL14 | Edit lead via pencil icon | User is logged in as Admin/Manager | 1. Click pencil icon (✏) in Actions column | Edit Lead dialog opens with all current values pre-filled. |
| TC-LL15 | Edit lead name | Edit dialog open | 1. Change Name to "Updated Name" 2. Click Save | Lead is updated. Table shows new name. Success notification. |
| TC-LL16 | Edit lead email | Edit dialog open | 1. Change Email to new value 2. Save | Lead email is updated in table. |
| TC-LL17 | Edit lead priority | Edit dialog open | 1. Change Priority from Medium to High 2. Save | Priority badge updates in table. |
| TC-LL18 | Edit lead status | Edit dialog open | 1. Change Status from New to Contacted 2. Save | Status badge updates in table. |
| TC-LL19 | Edit multiple fields at once | Edit dialog open | 1. Change Name, Phone, Company, Priority 2. Save | All fields update correctly. |
| TC-LL20 | Cancel edit without saving | Edit dialog open with changes | 1. Make changes 2. Click Cancel | Dialog closes. No changes saved. Original values remain. |
| TC-LL21 | Edit with invalid email | Edit dialog open | 1. Change email to "invalid" 2. Save | Validation error. Changes not saved. |
| TC-LL22 | Edit with empty name | Edit dialog open | 1. Clear Name field 2. Save | Validation error for required field. |

### 3.4 Delete Lead

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-LL23 | Delete lead via trash icon | User is Admin, lead exists | 1. Click trash icon (🗑) in Actions column | Confirmation dialog appears OR lead is deleted immediately. |
| TC-LL24 | Confirm delete | Delete confirmation shown | 1. Click Confirm/Yes | Lead is removed from table. Success notification. Total count decreases. |
| TC-LL25 | Cancel delete | Delete confirmation shown | 1. Click Cancel/No | Lead remains in table. No changes. |
| TC-LL26 | Delete and verify removal | Lead "Test Delete" exists | 1. Delete the lead 2. Search for "Test Delete" | Lead not found in search results. |
| TC-LL27 | Delete last lead on page | User on page 2, only 1 lead on page | 1. Delete the lead | User is redirected to page 1. Pagination updates. |

### 3.5 Search Functionality

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-LL28 | Search by exact name | Lead "John Doe" exists | 1. Type "John Doe" in search box | Only leads with "John Doe" in name appear. |
| TC-LL29 | Search by partial name | Lead "John Doe" exists | 1. Type "John" in search box | Leads with "John" in name appear (John Doe, Johnny, etc.). |
| TC-LL30 | Search by email | Lead with email "test@example.com" exists | 1. Type "test@example.com" in search | Lead with that email appears. |
| TC-LL31 | Search by partial email | Leads with @testmail.com exist | 1. Type "testmail" in search | All leads with "testmail" in email appear. |
| TC-LL32 | Search by phone number | Lead with phone "555-123-4567" exists | 1. Type "555-123" in search | Lead with matching phone appears. |
| TC-LL33 | Search is case-insensitive | Lead "John Doe" exists | 1. Type "john doe" (lowercase) | Lead "John Doe" appears in results. |
| TC-LL34 | Search with no results | No lead named "ZZZZZ" | 1. Type "ZZZZZ" in search | Empty table or "No leads found" message. |
| TC-LL35 | Clear search restores list | Search filter active | 1. Clear search input 2. Press Enter or wait | Full leads list is restored. |
| TC-LL36 | Search with special characters | User on leads page | 1. Type "<script>" in search | No results. No XSS execution. App handles gracefully. |

### 3.6 Status Filter

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-LL37 | Filter by status "New" | Leads with various statuses exist | 1. Click "All Statuses" dropdown 2. Select "New" | Only leads with status "New" are shown. |
| TC-LL38 | Filter by status "Contacted" | Leads with Contacted status exist | 1. Select "Contacted" from dropdown | Only Contacted leads shown. |
| TC-LL39 | Filter by status "Qualified" | Leads with Qualified status exist | 1. Select "Qualified" from dropdown | Only Qualified leads shown. |
| TC-LL40 | Filter by status "Lost" | Leads with Lost status exist | 1. Select "Lost" from dropdown | Only Lost leads shown. |
| TC-LL41 | Reset filter to "All Statuses" | Status filter is active | 1. Select "All Statuses" | All leads shown regardless of status. |
| TC-LL42 | Combine search and status filter | Leads exist | 1. Search for "John" 2. Filter by "New" | Only leads with "John" AND status "New" shown. |
| TC-LL43 | Status filter persists on pagination | Filter active, multiple pages | 1. Filter by "New" 2. Click Next | Next page shows only "New" status leads. |

### 3.7 Sorting

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-LL44 | Sort by ID ascending | Leads exist | 1. Click "ID" column header | Leads sorted by ID ascending (1, 2, 3...). Arrow indicator shows ↑. |
| TC-LL45 | Sort by ID descending | Sorted by ID asc | 1. Click "ID" header again | Leads sorted by ID descending (100, 99, 98...). Arrow shows ↓. |
| TC-LL46 | Sort by Name ascending | Leads exist | 1. Click "Name" column header | Leads sorted alphabetically A-Z. |
| TC-LL47 | Sort by Name descending | Sorted by Name asc | 1. Click "Name" header again | Leads sorted Z-A. |
| TC-LL48 | Sort by Email | Leads exist | 1. Click "Email" column header | Leads sorted by email alphabetically. |
| TC-LL49 | Sort by Company | Leads exist | 1. Click "Company" column header | Leads sorted by company name. |
| TC-LL50 | Sort by Priority | Leads exist | 1. Click "Priority" column header | Leads sorted by priority (Low → Critical or vice versa). |
| TC-LL51 | Sort by Status | Leads exist | 1. Click "Status" column header | Leads sorted by status alphabetically. |
| TC-LL52 | Sort by Deal Value | Leads exist | 1. Click "Deal Value" column header | Leads sorted by deal value numerically. |
| TC-LL53 | Sort by Created date | Leads exist | 1. Click "Created" column header | Leads sorted by creation date. |
| TC-LL54 | Sort persists on pagination | Sort active, multiple pages | 1. Sort by Name 2. Click Next | Next page maintains Name sort order. |
| TC-LL55 | Sort with filter active | Status filter active | 1. Filter by "New" 2. Sort by Name | Filtered results are sorted by Name. |

### 3.8 Pagination

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-LL56 | Verify pagination info | More than 10 leads exist | 1. Observe pagination area | Shows "Showing 1 to 10 of X leads". |
| TC-LL57 | Click Next button | On page 1, more pages exist | 1. Click "Next" button | Table shows leads 11-20. Pagination updates to "Showing 11 to 20 of X". |
| TC-LL58 | Click Previous button | On page 2 | 1. Click "Previous" button | Table shows leads 1-10. Back to page 1. |
| TC-LL59 | Previous disabled on first page | On page 1 | 1. Observe Previous button | Previous button is disabled or not clickable. |
| TC-LL60 | Next disabled on last page | On last page | 1. Observe Next button | Next button is disabled or not clickable. |
| TC-LL61 | Navigate to last page | Many pages exist | 1. Click Next repeatedly until last page | Last page shows remaining leads. Next is disabled. |
| TC-LL62 | Pagination with search filter | Search active, results span pages | 1. Search for common term 2. Click Next | Pagination works within filtered results. |
| TC-LL63 | Pagination with status filter | Status filter active | 1. Filter by "New" 2. Click Next | Pagination works within status-filtered results. |
| TC-LL64 | Page size is 10 | Leads exist | 1. Count rows on page 1 | Exactly 10 leads shown per page (or less on last page). |

### 3.9 Negative / Edge Cases

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-LL65 | Export leads | User is on leads page with data | 1. Click "Export" button | CSV/data file is downloaded with lead information. |
| TC-LL66 | Rapid pagination clicks | Multiple pages exist | 1. Click Next rapidly multiple times | App handles gracefully. No duplicate requests or errors. |
| TC-LL67 | Sort then search | Sort by Name active | 1. Search for "John" | Search results maintain sort order. |
| TC-LL68 | Edit lead then verify in list | Lead edited | 1. Edit lead name 2. Observe table | Updated name appears immediately in table. |
| TC-LL69 | Delete lead then verify count | Note total count | 1. Delete a lead 2. Check pagination info | Total count decreases by 1. |

---

## 4. End-to-End Flow: Login → Create Lead → List Lead

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-E2E01 | Complete flow: Login, Create, Verify | Application accessible | 1. Navigate to login page 2. Login as admin 3. Verify leads page loads 4. Click "Create Lead" 5. Fill Name & Email (unique) 6. Submit 7. Search for the created lead by name | Lead appears in filtered search results with correct name and email. |
| TC-E2E02 | Create multiple leads and verify count | User is logged in | 1. Note current total leads count 2. Create 2 new leads 3. Observe pagination count | Total leads count increases by 2. |
| TC-E2E03 | Create lead and verify via API | User is logged in via UI | 1. Create a lead via UI with unique email 2. Call GET /api/leads 3. Search response for the email | Lead exists in API response confirming data persistence. |

---

## 5. Role-Based Access Control (RBAC)

### 5.1 Admin Role Tests

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-R01 | Admin can create leads | Logged in as Admin (`admin@company.com`) | 1. Click "Create Lead" 2. Fill required fields 3. Submit | Lead is created successfully. |
| TC-R02 | Admin can edit leads | Logged in as Admin, lead exists | 1. Click Edit on a lead 2. Modify fields 3. Save | Lead is updated successfully. |
| TC-R03 | Admin can delete leads | Logged in as Admin, lead exists | 1. Click Delete on a lead 2. Confirm deletion | Lead is removed from the list. |
| TC-R04 | Admin can export leads | Logged in as Admin | 1. Click Export button | CSV file is downloaded with all leads. |
| TC-R05 | Admin can view all leads | Logged in as Admin | 1. Navigate to leads page | All leads are visible in the table. |

### 5.2 Manager Role Tests

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-R06 | Manager can create leads | Logged in as Manager (`qa@company.com`) | 1. Click "Create Lead" 2. Fill required fields 3. Submit | Lead is created successfully. |
| TC-R07 | Manager can edit leads | Logged in as Manager, lead exists | 1. Click Edit on a lead 2. Modify fields 3. Save | Lead is updated successfully. |
| TC-R08 | Manager cannot delete leads | Logged in as Manager, lead exists | 1. Attempt to delete a lead | Delete option is hidden or disabled. Error if attempted via API. |
| TC-R09 | Manager can export leads | Logged in as Manager | 1. Click Export button | CSV file is downloaded. |
| TC-R10 | Manager can view all leads | Logged in as Manager | 1. Navigate to leads page | All leads are visible in the table. |

### 5.3 Viewer Role Tests

| TC# | Title | Preconditions | Steps | Expected Result |
|-----|-------|---------------|-------|-----------------|
| TC-R11 | Viewer cannot create leads | Logged in as Viewer (`tester@company.com`) | 1. Look for "Create Lead" button | Button is hidden or disabled. |
| TC-R12 | Viewer cannot edit leads | Logged in as Viewer, lead exists | 1. Look for Edit option on leads | Edit option is hidden or disabled. |
| TC-R13 | Viewer cannot delete leads | Logged in as Viewer, lead exists | 1. Look for Delete option on leads | Delete option is hidden or disabled. |
| TC-R14 | Viewer cannot export leads | Logged in as Viewer | 1. Look for Export button | Export button is hidden or disabled. |
| TC-R15 | Viewer can view all leads | Logged in as Viewer | 1. Navigate to leads page | All leads are visible (read-only). |

---

## 6. API Test Cases

### 6.1 Authentication API

| TC# | Title | Method | Endpoint | Request | Expected Response |
|-----|-------|--------|----------|---------|-------------------|
| TC-API01 | Login with valid Admin credentials | POST | `/api/login` | `{"email":"admin@company.com","password":"Admin@123"}` | 200 OK, `{"success":true,"token":"...","email":"...","role":"admin"}` |
| TC-API02 | Login with valid Manager credentials | POST | `/api/login` | `{"email":"qa@company.com","password":"password123"}` | 200 OK, `{"success":true,"token":"...","role":"manager"}` |
| TC-API03 | Login with valid Viewer credentials | POST | `/api/login` | `{"email":"tester@company.com","password":"Test@456"}` | 200 OK, `{"success":true,"token":"...","role":"viewer"}` |
| TC-API04 | Login with wrong password | POST | `/api/login` | `{"email":"admin@company.com","password":"wrong"}` | 401, `{"success":false,"error":"Invalid credentials"}` |
| TC-API05 | Login with empty body | POST | `/api/login` | `{}` | 400, `{"success":false,"error":"Email and password are required"}` |
| TC-API06 | SQL injection in email | POST | `/api/login` | `{"email":"' OR 1=1 --","password":"x"}` | 401, No data leakage |

### 6.2 Leads API - CRUD Operations

| TC# | Title | Method | Endpoint | Auth | Request | Expected Response |
|-----|-------|--------|----------|------|---------|-------------------|
| TC-API07 | Get all leads | GET | `/api/leads` | Bearer token | - | 200 OK, `{"success":true,"leads":[...]}` |
| TC-API08 | Get leads without auth | GET | `/api/leads` | None | - | 401, `{"success":false,"error":"Authorization header is required"}` |
| TC-API09 | Create lead with required fields | POST | `/api/leads` | Bearer token | `{"name":"Test","email":"test@test.com"}` | 201, `{"success":true,"lead":{...}}` |
| TC-API10 | Create lead with all fields | POST | `/api/leads` | Bearer token | Full payload with all fields | 201, Lead created with all fields |
| TC-API11 | Create lead without name | POST | `/api/leads` | Bearer token | `{"email":"test@test.com"}` | 400, Validation error for name |
| TC-API12 | Create lead without email | POST | `/api/leads` | Bearer token | `{"name":"Test"}` | 400, Validation error for email |

### 6.3 Leads API - Get Single Lead

| TC# | Title | Method | Endpoint | Auth | Expected Response |
|-----|-------|--------|----------|------|-------------------|
| TC-API13 | Get lead by valid ID | GET | `/api/leads/{id}` | Bearer token | 200 OK, `{"success":true,"lead":{...}}` with all lead fields |
| TC-API14 | Get lead by invalid ID | GET | `/api/leads/99999` | Bearer token | 404, `{"success":false,"error":"Lead not found"}` |
| TC-API15 | Get lead without auth | GET | `/api/leads/{id}` | None | 401, Unauthorized |
| TC-API16 | Get lead with non-numeric ID | GET | `/api/leads/abc` | Bearer token | 400 or 404, Invalid ID error |

### 6.4 Leads API - Update (PUT)

| TC# | Title | Method | Endpoint | Auth | Request | Expected Response |
|-----|-------|--------|----------|------|---------|-------------------|
| TC-API17 | Update lead name | PUT | `/api/leads/{id}` | Bearer token | `{"name":"Updated Name","email":"..."}` | 200 OK, Lead updated with new name |
| TC-API18 | Update lead email | PUT | `/api/leads/{id}` | Bearer token | `{"name":"...","email":"new@email.com"}` | 200 OK, Lead updated with new email |
| TC-API19 | Update lead priority | PUT | `/api/leads/{id}` | Bearer token | `{"name":"...","email":"...","priority":"High"}` | 200 OK, Priority updated |
| TC-API20 | Update lead status | PUT | `/api/leads/{id}` | Bearer token | `{"name":"...","email":"...","status":"Contacted"}` | 200 OK, Status updated |
| TC-API21 | Update multiple fields | PUT | `/api/leads/{id}` | Bearer token | `{"name":"New","email":"new@test.com","phone":"555-1234","company":"NewCo"}` | 200 OK, All fields updated |
| TC-API22 | Update with empty name | PUT | `/api/leads/{id}` | Bearer token | `{"name":"","email":"..."}` | 400, Validation error |
| TC-API23 | Update with invalid email | PUT | `/api/leads/{id}` | Bearer token | `{"name":"...","email":"invalid"}` | 400, Validation error |
| TC-API24 | Update non-existent lead | PUT | `/api/leads/99999` | Bearer token | `{"name":"Test","email":"..."}` | 404, Lead not found |
| TC-API25 | Update without auth | PUT | `/api/leads/{id}` | None | `{"name":"Test","email":"..."}` | 401, Unauthorized |
| TC-API26 | Update with invalid status | PUT | `/api/leads/{id}` | Bearer token | `{"name":"...","email":"...","status":"Won"}` | 400, Invalid status |

### 6.5 Leads API - Delete

| TC# | Title | Method | Endpoint | Auth | Expected Response |
|-----|-------|--------|----------|------|-------------------|
| TC-API27 | Delete lead by valid ID | DELETE | `/api/leads/{id}` | Bearer token | 200 OK, `{"success":true,"message":"Lead deleted"}` |
| TC-API28 | Delete non-existent lead | DELETE | `/api/leads/99999` | Bearer token | 404, Lead not found |
| TC-API29 | Delete without auth | DELETE | `/api/leads/{id}` | None | 401, Unauthorized |
| TC-API30 | Delete with invalid token | DELETE | `/api/leads/{id}` | Invalid token | 401, Unauthorized |
| TC-API31 | Verify deleted lead is gone | GET | `/api/leads/{id}` | Bearer token | After delete: 404, Lead not found |
| TC-API32 | Delete same lead twice | DELETE | `/api/leads/{id}` | Bearer token | Second delete: 404, Lead not found |

### 6.6 Leads API - Pagination

| TC# | Title | Method | Endpoint | Auth | Query Params | Expected Response |
|-----|-------|--------|----------|------|--------------|-------------------|
| TC-API33 | Get leads page 1 | GET | `/api/leads` | Bearer token | `?page=1` | 200 OK, First 10 leads |
| TC-API34 | Get leads page 2 | GET | `/api/leads` | Bearer token | `?page=2` | 200 OK, Leads 11-20 |
| TC-API35 | Get leads with limit | GET | `/api/leads` | Bearer token | `?limit=5` | 200 OK, 5 leads returned |
| TC-API36 | Get leads page + limit | GET | `/api/leads` | Bearer token | `?page=2&limit=5` | 200 OK, Leads 6-10 |
| TC-API37 | Get leads invalid page | GET | `/api/leads` | Bearer token | `?page=0` | 200 OK (defaults to page 1) or 400 |
| TC-API38 | Get leads negative page | GET | `/api/leads` | Bearer token | `?page=-1` | 200 OK (defaults) or 400 |
| TC-API39 | Get leads very large page | GET | `/api/leads` | Bearer token | `?page=9999` | 200 OK, Empty leads array |

### 6.7 Leads API - Search

| TC# | Title | Method | Endpoint | Auth | Query Params | Expected Response |
|-----|-------|--------|----------|------|--------------|-------------------|
| TC-API40 | Search by name | GET | `/api/leads` | Bearer token | `?search=John` | 200 OK, Leads with "John" in name |
| TC-API41 | Search by email | GET | `/api/leads` | Bearer token | `?search=test@` | 200 OK, Leads with "test@" in email |
| TC-API42 | Search by phone | GET | `/api/leads` | Bearer token | `?search=555` | 200 OK, Leads with "555" in phone |
| TC-API43 | Search case insensitive | GET | `/api/leads` | Bearer token | `?search=JOHN` | 200 OK, Same as lowercase search |
| TC-API44 | Search no results | GET | `/api/leads` | Bearer token | `?search=zzzznonexistent` | 200 OK, Empty leads array |
| TC-API45 | Search with special chars | GET | `/api/leads` | Bearer token | `?search=<script>` | 200 OK, No XSS, empty or safe results |
| TC-API46 | Search + pagination | GET | `/api/leads` | Bearer token | `?search=test&page=2` | 200 OK, Page 2 of search results |

### 6.8 Leads API - Status Filter

| TC# | Title | Method | Endpoint | Auth | Query Params | Expected Response |
|-----|-------|--------|----------|------|--------------|-------------------|
| TC-API47 | Filter by status New | GET | `/api/leads` | Bearer token | `?status=New` | 200 OK, Only leads with status "New" |
| TC-API48 | Filter by status Contacted | GET | `/api/leads` | Bearer token | `?status=Contacted` | 200 OK, Only "Contacted" leads |
| TC-API49 | Filter by status Qualified | GET | `/api/leads` | Bearer token | `?status=Qualified` | 200 OK, Only "Qualified" leads |
| TC-API50 | Filter by status Lost | GET | `/api/leads` | Bearer token | `?status=Lost` | 200 OK, Only "Lost" leads |
| TC-API51 | Filter invalid status | GET | `/api/leads` | Bearer token | `?status=Won` | 200 OK (ignored) or 400 |
| TC-API52 | Filter + search | GET | `/api/leads` | Bearer token | `?status=New&search=John` | 200 OK, "New" leads with "John" |
| TC-API53 | Filter + pagination | GET | `/api/leads` | Bearer token | `?status=New&page=2` | 200 OK, Page 2 of "New" leads |

### 6.9 Leads API - Sorting

| TC# | Title | Method | Endpoint | Auth | Query Params | Expected Response |
|-----|-------|--------|----------|------|--------------|-------------------|
| TC-API54 | Sort by ID ascending | GET | `/api/leads` | Bearer token | `?sortBy=id&order=asc` | 200 OK, Leads sorted by ID 1,2,3... |
| TC-API55 | Sort by ID descending | GET | `/api/leads` | Bearer token | `?sortBy=id&order=desc` | 200 OK, Leads sorted by ID 100,99,98... |
| TC-API56 | Sort by name ascending | GET | `/api/leads` | Bearer token | `?sortBy=name&order=asc` | 200 OK, Leads A-Z by name |
| TC-API57 | Sort by name descending | GET | `/api/leads` | Bearer token | `?sortBy=name&order=desc` | 200 OK, Leads Z-A by name |
| TC-API58 | Sort by email | GET | `/api/leads` | Bearer token | `?sortBy=email&order=asc` | 200 OK, Leads sorted by email |
| TC-API59 | Sort by priority | GET | `/api/leads` | Bearer token | `?sortBy=priority&order=asc` | 200 OK, Leads sorted by priority |
| TC-API60 | Sort by status | GET | `/api/leads` | Bearer token | `?sortBy=status&order=asc` | 200 OK, Leads sorted by status |
| TC-API61 | Sort by dealValue | GET | `/api/leads` | Bearer token | `?sortBy=dealValue&order=desc` | 200 OK, Leads sorted by deal value |
| TC-API62 | Sort by createdAt | GET | `/api/leads` | Bearer token | `?sortBy=createdAt&order=desc` | 200 OK, Newest leads first |
| TC-API63 | Sort + filter + search | GET | `/api/leads` | Bearer token | `?sortBy=name&order=asc&status=New&search=test` | 200 OK, Combined filters |
| TC-API64 | Sort invalid field | GET | `/api/leads` | Bearer token | `?sortBy=invalid` | 200 OK (ignored) or 400 |

### 6.10 Leads API - Validation & Boundary

| TC# | Title | Method | Endpoint | Request | Expected Response |
|-----|-------|--------|----------|---------|-------------------|
| TC-API13 | Name with 1 character | POST | `/api/leads` | `{"name":"A","email":"..."}` | 400, "Name must be at least 2 characters" |
| TC-API14 | Name with 2 characters | POST | `/api/leads` | `{"name":"AB","email":"..."}` | 201, Lead created |
| TC-API15 | Invalid phone format | POST | `/api/leads` | `{"name":"Test","email":"...","phone":"+1 (555) 123"}` | 400, "Phone must contain only digits, spaces, and phone symbols" |
| TC-API16 | Valid phone format | POST | `/api/leads` | `{"name":"Test","email":"...","phone":"555-123-4567"}` | 201, Lead created |
| TC-API17 | Invalid status value | POST | `/api/leads` | `{"name":"Test","email":"...","status":"Won"}` | 400, "Status must be one of: New, Contacted, Qualified, Lost" |
| TC-API18 | XSS in name field | POST | `/api/leads` | `{"name":"<script>alert(1)</script>","email":"..."}` | 201 (stored) or 400 (rejected) - document behavior |

### 6.4 Leads API - Security

| TC# | Title | Method | Endpoint | Request | Expected Response |
|-----|-------|--------|----------|---------|-------------------|
| TC-API19 | Invalid token | GET | `/api/leads` | Auth: `Bearer invalid` | 401, Unauthorized |
| TC-API20 | Expired/malformed token | GET | `/api/leads` | Auth: `Bearer eyJ...expired` | 401, Unauthorized |
| TC-API21 | SQL injection in name | POST | `/api/leads` | `{"name":"'; DROP TABLE leads; --","email":"..."}` | 201 or 400, No SQL execution |
| TC-API22 | Path traversal in name | POST | `/api/leads` | `{"name":"../../../etc/passwd","email":"..."}` | 201 or 400, No file access |

---

## 7. Create Lead Form - All Fields Reference

Based on the UI screenshots, the Create Lead form contains:

### Basic Information
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Name | Text input | Yes* | Min 2 characters |
| Email | Email input | Yes* | Valid email format |
| Phone | Text input | No | Digits, dashes, spaces only |
| Company | Text input | No | - |
| Job Title | Text input | No | - |

### Lead Classification
| Field | Type | Options |
|-------|------|---------|
| Industry | Dropdown | Technology, Healthcare, Finance, Education, Retail, Manufacturing, Other |
| Source | Dropdown | Website, LinkedIn, Referral, Email Campaign, Trade Show |
| Priority | Dropdown | Low, Medium, High, Critical |
| Status | Dropdown | New, Contacted, Qualified, Lost |

### Deal Information
| Field | Type | Validation |
|-------|------|------------|
| Deal Value ($) | Number input | Positive integer |
| Expected Close Date | Date picker | Future date |
| Follow-up Date | Date picker | Future date |

### Additional Details
| Field | Type | Default |
|-------|------|---------|
| Lead is qualified | Checkbox | Unchecked |
| Opted in for email communications | Checkbox | Unchecked |
| Notes | Textarea | Empty |
