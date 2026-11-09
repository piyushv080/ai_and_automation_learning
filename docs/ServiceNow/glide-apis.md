# Glide APIs — GlideRecord, Form, User, System, Session, Date, and Aggregation

Study notes for the core ServiceNow Glide APIs. These classes let developers interact with the platform and its database through JavaScript instead of writing SQL. This page covers the server-side and client-side APIs from Lessons 1–8 of the ServiceNow Live book.

> **Before you begin:** Most server-side examples run from **System Definition > Scripts - Background**. Always test queries on a non-production instance. An incorrectly constructed encoded query (for example, an invalid field name) produces an invalid query, and calling `insert()`, `update()`, or `deleteRecord()` on a bad query can cause data loss.

## Glide API overview

ServiceNow developers use the Glide APIs to change the default behavior of an application and to customize existing functionality. Glide classes provide flexibility for interacting with application data through scripting. Using the Glide APIs you can perform database operations without writing SQL.

Each API contains many methods, and each method performs a different operation on ServiceNow applications.

| Client side | Server side |
| --- | --- |
| GlideForm | GlideRecord |
| GlideUser | GlideSystem |
| GlideAjax | GlideDate |
| GlideDialogWindow | GlideDateTime |
| GlideMenu | GlideAggregate |
| GlideList | GlideElement |

---

## Lesson 1: GlideRecord

GlideRecord is the most common and most important API and is used frequently on the platform. It is a special native JavaScript class that runs on the server side. GlideRecord performs CRUD operations instead of writing SQL queries, and it handles both rows and columns in the underlying database.

On ServiceNow you cannot interact directly with the database to perform CRUD operations with SQL. Use GlideRecord instead.

Key characteristics:

1. Most common API.
2. Runs on the server side.
3. Used to generate SQL queries.
4. Performs CRUD operations.

### GlideRecord architecture

Instead of passing SQL queries, you use JavaScript. GlideRecord maps your JavaScript calls to the underlying database operations.

### Common GlideRecord methods

| Method | Purpose | Method | Purpose |
| --- | --- | --- | --- |
| `query()` | Run the query | `insert()` | Insert a record |
| `addQuery()` | Add a condition | `update()` | Update the current record |
| `addActiveQuery()` | Filter `active = true` | `updateMultiple()` | Update many records |
| `addInactiveQuery()` | Filter `active = false` | `deleteRecord()` | Delete the current record |
| `addEncodedQuery()` | Add a raw encoded query | `deleteMultiple()` | Delete many records |
| `addNullQuery()` | Field is null | `get()` | Fetch one record by sys_id or field |
| `addNotNullQuery()` | Field is not null | `next()` | Advance to the next record |
| `addJoinQuery()` | Join another table | `hasNext()` | More records available |
| `orderBy()` / `orderByDesc()` | Sort results | `getRowCount()` | Number of rows |
| `setLimit()` | Limit result count | `getValue()` / `getDisplayValue()` | Read field values |
| `chooseWindow()` | Page through results | `setValue()` | Set a field value |
| `getTableName()` | Current table name | `isValid()` / `isValidRecord()` | Validity checks |
| `getUniqueValue()` | Record sys_id | `canCreate()` / `canRead()` / `canWrite()` / `canDelete()` | ACL checks |
| `getElement()` | Column element | `autoSysFields()` / `setWorkflow()` | Control system field / workflow behavior |

### GlideRecord exercises

**1. Output in ServiceNow**

```javascript
gs.print('Welcome to ServiceNow Academy');
gs.info('Welcome to ServiceNow Academy');
```

**2. Add two numbers**

```javascript
var a = 10;
var b = 20;
var c = a + b;
gs.print(a + b); // 30
```

**3. Query all incidents**

```javascript
var inc = new GlideRecord('incident'); // GlideRecord object; 'incident' is the table
inc.query();                            // execute the query on the table
while (inc.next()) {                    // loop over the result set
    gs.print(inc.number);               // print each incident number
}
```

**4. Query with addQuery — priority 1 tickets**

```javascript
var inc = new GlideRecord('incident');
inc.addQuery('priority', 1);
inc.query();
while (inc.next()) {
    gs.print(inc.number);
}
```

**5. Multiple queries**

```javascript
var inc = new GlideRecord('incident');
inc.addQuery('active', true);
inc.addQuery('priority', 1);
inc.addQuery('category', 'software');
inc.query();
while (inc.next()) {
    gs.print(inc.number);
}
```

**6. addEncodedQuery**

Build the condition in the Incident list view, click **Run**, then use **Copy query** and paste the encoded query into your script.

```javascript
var inc = new GlideRecord('incident');
inc.addEncodedQuery('active=true^category=software^priority=1');
inc.query();
while (inc.next()) {
    gs.print(inc.number);
}
```

Encoded query stored in a variable:

```javascript
var ecq = 'active=true^category=software^priority=1';
var inc = new GlideRecord('incident');
inc.addEncodedQuery(ecq);
inc.query();
while (inc.next()) {
    gs.print(inc.number);
}
```

**7. addQuery with an operator — `addQuery(field, operator, value)`**

Supported operators:

- Numeric/date: `=`, `!=`, `>`, `>=`, `<`, `<=`
- Strings (uppercase): `=`, `!=`, `IN`, `NOT IN`, `STARTSWITH`, `ENDSWITH`, `CONTAINS`, `DOES NOT CONTAIN`, `INSTANCEOF`

```javascript
// Active and priority <= 2
var inc = new GlideRecord('incident');
inc.addActiveQuery();
inc.addQuery('priority', '<=', 2);
inc.query();
while (inc.next()) {
    gs.print(inc.number);
}
```

```javascript
// priority <= 2 and short_description contains SAP
var inc = new GlideRecord('incident');
inc.addActiveQuery();
inc.addQuery('priority', '<=', 2);
inc.addQuery('short_description', 'CONTAINS', 'SAP');
inc.query();
while (inc.next()) {
    gs.print(inc.number + ' ' + inc.short_description);
}
```

```javascript
// category IN (software, hardware)
var cat = ['software', 'hardware'];
var inc = new GlideRecord('incident');
inc.addQuery('category', 'IN', cat);
inc.query();
while (inc.next()) {
    gs.print(inc.getValue('number') + ' ' + inc.getValue('short_description'));
}
```

```javascript
// category STARTSWITH net
var inc = new GlideRecord('incident');
inc.addQuery('category', 'STARTSWITH', 'net');
inc.query();
while (inc.next()) {
    gs.print(inc.number);
}
```

**8. addActiveQuery**

```javascript
var inc = new GlideRecord('incident');
inc.addActiveQuery(); // instead of active = true
inc.addQuery('priority', 1);
inc.query();
while (inc.next()) {
    gs.info(inc.number);
}
```

**9. addInactiveQuery**

```javascript
var inc = new GlideRecord('incident');
inc.addInactiveQuery(); // opposite of active query
inc.addQuery('priority', 1);
inc.query();
while (inc.next()) {
    gs.print(inc.number);
}
```

**10. getEncodedQuery**

```javascript
var inc = new GlideRecord('incident');
inc.addEncodedQuery('active=true^category=software^priority=1');
inc.query();
while (inc.next()) {
    gs.print(inc.getEncodedQuery());
}
```

**11. orderBy (ascending)**

```javascript
var inc = new GlideRecord('incident');
inc.addQuery('priority', 1);
inc.addQuery('category', 'software');
inc.orderBy('short_description');
inc.query();
while (inc.next()) {
    gs.print(inc.number + ' ' + inc.short_description);
}
```

**12. orderByDesc (descending)**

```javascript
var inc = new GlideRecord('incident');
inc.addQuery('priority', 1);
inc.addQuery('category', 'software');
inc.orderByDesc('short_description');
inc.query();
while (inc.next()) {
    gs.print(inc.number + ' ' + inc.short_description);
}
```

**13. setLimit**

```javascript
var inc = new GlideRecord('incident');
inc.addQuery('priority', 1);
inc.orderByDesc('short_description');
inc.setLimit(10);
inc.query();
while (inc.next()) {
    gs.print(inc.number + ' ' + inc.short_description);
}
```

**14. get()**

```javascript
// Get sys_id from an incident number
var inc = new GlideRecord('incident');
inc.get('number', 'INC0009005');
gs.print(inc.sys_id);
```

```javascript
// Get incident number from a sys_id
var inc = new GlideRecord('incident');
inc.get('965c9e5347c12200e0ef563dbb9a7156');
gs.print(inc.number);
```

**15. chooseWindow — paging**

```javascript
var inc = new GlideRecord('incident');
inc.addQuery('priority', 1);
inc.addActiveQuery();
inc.chooseWindow(3, 7); // first value included, second excluded
inc.query();
while (inc.next()) {
    gs.print(inc.number);
}
```

**16. getRowCount**

```javascript
var inc = new GlideRecord('incident');
inc.query();
gs.print(inc.getRowCount());
```

```javascript
var inc = new GlideRecord('sys_user');
inc.addQuery('active', true);
inc.query();
gs.print('Active users are: ' + inc.getRowCount());
```

**17. getTableName**

```javascript
var inc = new GlideRecord('change_request');
gs.print(inc.getTableName());
```

**18. getValue**

```javascript
var inc = new GlideRecord('incident');
inc.addQuery('active', true);
inc.query();
while (inc.next()) {
    gs.print(inc.getValue('short_description'));
}
```

**19. getDisplayValue**

```javascript
var inc = new GlideRecord('incident');
inc.addQuery('priority', 1);
inc.query();
while (inc.next()) {
    gs.print(inc.priority.getDisplayValue());
}
```

**20. hasNext**

```javascript
var inc = new GlideRecord('incident');
inc.query();
gs.print(inc.hasNext()); // true if more elements remain
```

**21. getUniqueValue**

```javascript
var inc = new GlideRecord('incident');
inc.query();
inc.next();
var uniqvalue = inc.getUniqueValue();
gs.print(uniqvalue);
```

**22. setValue**

```javascript
var attriName = 'category';
var inc = new GlideRecord('incident');
inc.initialize();
inc.setValue(attriName, 'network');
inc.setValue('short_description', 'Critical VPN Issue');
inc.insert();
gs.print('Category is ' + inc.category + ' and issue is: ' + inc.short_description);
```

**23. getElement**

```javascript
var elementName = 'short_description';
var inc = new GlideRecord('incident');
inc.initialize();
inc.setValue(elementName, 'I am facing VPN Problem');
inc.insert();
gs.print(inc.getElement('short_description'));
```

**24. getRecordClassName**

```javascript
var inc = new GlideRecord('change_request');
var grcn = inc.getRecordClassName();
gs.info(grcn);
```

**25. initialize() and insert()**

```javascript
var inc = new GlideRecord('incident');
inc.initialize();                              // compose the incident form
inc.category = 'network';                      // set field values
inc.short_description = 'Firewall Issue';
inc.priority = 1;
inc.insert();                                  // create the new record
gs.print(inc.number);                          // print the new incident number
```

**26. isNewRecord() and newRecord()**

```javascript
var inc = new GlideRecord('incident');
inc.newRecord();
gs.info(inc.isNewRecord()); // true
```

**27. isValid**

```javascript
var inc = new GlideRecord('incident');
gs.print(inc.isValid()); // true

var bad = new GlideRecord('srinivas');
gs.print(bad.isValid()); // false
```

**28. isValidField**

```javascript
var inc = new GlideRecord('incident');
gs.print(inc.isValidField('category')); // true
```

**29. getLink() and getProperty()**

```javascript
var inc = new GlideRecord('incident');
inc.addActiveQuery();
inc.addQuery('category', 'software');
inc.addQuery('priority', 1);
inc.query();
while (inc.next()) {
    gs.print(gs.getProperty('glide.servlet.uri') + inc.getLink(false));
}
```

**30. isValidRecord**

```javascript
var inc = new GlideRecord('incident');
inc.get('number', 'INC0010012');
gs.print(inc.number + ' exists: ' + inc.isValidRecord());
```

**31. newRecord**

```javascript
var inc = new GlideRecord('incident');
inc.newRecord();
inc.short_description = 'Creating new record';
inc.category = 'software';
inc.insert();
gs.print(inc.number);
```

**32. addNullQuery**

```javascript
var inc = new GlideRecord('incident');
inc.addNullQuery('short_description');
inc.query();
while (inc.next()) {
    gs.print(inc.number);
}
```

**33. addNotNullQuery**

```javascript
var inc = new GlideRecord('incident');
inc.addNotNullQuery('short_description');
inc.query();
while (inc.next()) {
    gs.print(inc.number);
}
```

**34. update() — single record**

```javascript
var inc = new GlideRecord('incident');
inc.get('number', 'INC0000057');
inc.setValue('state', 2);
inc.update();
```

**35. updateMultiple() — many records**

```javascript
var inc = new GlideRecord('incident');
inc.addQuery('category', 'hardware');
inc.setValue('category', 'software');
inc.updateMultiple();
```

**36. deleteRecord() — single record**

```javascript
var inc = new GlideRecord('incident');
inc.get('number', 'INC0010013');
inc.deleteRecord();
```

**37. deleteMultiple() — many records**

```javascript
var inc = new GlideRecord('incident');
inc.addQuery('priority', 4);
inc.query();
inc.deleteMultiple();
```

**38–41. canCreate / canRead / canWrite / canDelete**

```javascript
var inc = new GlideRecord('incident');
gs.print(inc.canCreate());
gs.print(inc.canRead());
gs.print(inc.canWrite());
gs.print(inc.canDelete());
```

**42. autoSysFields() and setWorkflow()**

`autoSysFields(false)` stops updates to system fields such as `sys_updated_by`, `sys_updated_on`, `sys_mod_count`, `sys_created_by`, and `sys_created_on`. It does not work on scoped applications. `setWorkflow(false)` stops other business rules from running.

```javascript
var inc = new GlideRecord('incident');
inc.addQuery('state', 1);
inc.query();
while (inc.next()) {
    inc.autoSysFields(false);
    inc.setWorkflow(false);
    inc.setValue('state', 2);
    inc.update();
}
```

**44. addJoinQuery**

```javascript
// Problems that have an incident attached
var prob = new GlideRecord('problem');
prob.addJoinQuery('incident', 'opened_by', 'caller_id');
prob.query();
while (prob.next()) {
    gs.print(prob.number);
}
```

**45. getGlideObject(), getNumericValue(), and setAbortAction()**

```javascript
if ((!current.u_date1.nil()) && (!current.u_date2.nil())) {
    var start = current.u_date1.getGlideObject().getNumericValue();
    var end = current.u_date2.getGlideObject().getNumericValue();
    if (start > end) {
        gs.addInfoMessage('start must be before end');
        current.u_date1.setError('start must be before end');
        current.setAbortAction(true);
    }
}
```

---

## Lesson 2: GlideForm (g_form)

GlideForm is a client-side API used to change the default behavior of the current record. Its methods run only on the client side (browser) and are accessed through the global `g_form` object. They customize the form view of records and are commonly used in Client Scripts (and Catalog Client Scripts).

> For field visibility, mandatory, and read-only rules, a UI Policy is usually a better practice than `g_form` methods.

### Common g_form methods

| Method | Purpose |
| --- | --- |
| `getValue()` / `setValue()` | Read / write a field value |
| `getUniqueValue()` | Current record sys_id |
| `getTableName()` | Current table name |
| `setDisabled()` | Make a field read-only |
| `setMandatory()` / `isMandatory()` | Control / check mandatory |
| `setDisplay()` | Hide/unhide a field and its space |
| `setVisible()` | Hide a field but keep its space |
| `addInfoMessage()` / `addErrorMessage()` / `clearMessages()` | Form messages |
| `addOption()` / `removeOption()` / `clearOptions()` | Choice list control |
| `clearValue()` | Clear a field |
| `hideRelatedLists()` / `showRelatedLists()` | Related list control |
| `isNewRecord()` | New record check |
| `showFieldMsg()` / `hideFieldMsg()` / `showErrorBox()` | Field-level messages |
| `getSections()` / `setSectionDisplay()` | Section control |
| `addDecoration()` / `flash()` | Field decoration and highlight |

### Running exercises on the client

1. Navigate to the Incident table.
2. Open an existing record.
3. Press **Ctrl+Shift+J** to open the JavaScript executor.
4. Run your code there.

```javascript
alert(g_form.getValue('category'));            // get a field value
g_form.setValue('category', 'hardware');       // set a field value
g_form.setDisabled('category', true);          // read-only
g_form.setMandatory('category', true);         // mandatory
g_form.setDisplay('business_service', false);  // hide field and space
g_form.setVisible('subcategory', false);       // hide field, keep space
g_form.isMandatory('category');
g_form.addInfoMessage('Please fill all mandatory fields');
g_form.addErrorMessage('Fill mandatory fields');
g_form.disableAttachments();
g_form.enableAttachments();
g_form.clearMessages();
g_form.addOption('priority', '6', '6 - Really Low');
g_form.removeOption('impact', 4);
g_form.clearOptions('category');
g_form.clearValue('category');
g_form.hideRelatedLists();
g_form.showRelatedLists();
g_form.isNewRecord();
g_form.showFieldMsg('cmdb_ci', 'At least select one service app', 'info');
g_form.hideFieldMsg('impact');        // remove only the last message
g_form.hideFieldMsg('impact', true);  // remove all messages for the field
alert(g_form.getTableName());
alert(g_form.getUniqueValue());
g_form.addDecoration('caller_id', 'icon-star', 'Mark as Favorite', 'color-green');
g_form.flash('incident.number', '#FFFACD', 0);
```

Sections example (Change form):

```javascript
function onChange(control, oldValue, newValue, isLoading) {
    var sections = g_form.getSections();
    if (newValue == '2') {
        g_form.setSectionDisplay(sections[1], false);
    } else {
        g_form.setSectionDisplay(sections[1], true);
    }
}
```

---

## Lesson 3: GlideUser (g_user)

GlideUser provides details about the current logged-in user and their roles. It runs on the client side and is typically used in Client Scripts and client UI Actions. Access it through the global `g_user` object. Using GlideUser avoids slower GlideRecord queries to get user information.

> You cannot use `g_user` in Business Rules or server-side UI Actions.

### Client-side (g_user) examples

```javascript
alert(g_user.firstName);
alert(g_user.lastName);
alert(g_user.fullName);
alert(g_user.userID);                     // 32-character user sys_id
alert(g_user.hasRole('admin'));           // true if user has role
alert(g_user.hasRoleExactly('itil'));     // true only if role is exact
alert(g_user.hasRoleFromList('itil, admin'));
alert('User Name is ' + g_user.userName);
```

```javascript
alert("First Name = " + g_user.firstName
    + ", \n Last Name = " + g_user.lastName
    + ", \n User Name = " + g_user.userName
    + ", \n User ID = " + g_user.userID);
```

### Server-side / scoped (gs.getUser())

The scoped GlideUser API provides access to current-user information from server-side scripts. Run these from **Scripts - Background**.

```javascript
var cu = gs.getUser();
gs.print(cu.getFirstName());
gs.print(cu.getLastName());
gs.print(cu.getFullName());
gs.print(cu.getEmail());
gs.print(cu.getID());
gs.print(cu.getName());
gs.print(cu.getCompanyID());
gs.print(cu.getDisplayName());
gs.print(cu.getDomainDisplayValue());
gs.print(cu.getRoles());
gs.print(cu.getUserRoles());
gs.print(cu.hasRole('admin'));
gs.print(cu.isMemberOf('database'));

// Active groups the user belongs to
var myGroupsArray = gs.getUser().getMyGroups().toArray();
gs.print(myGroupsArray[0]);

// Look up another user
var newUser = gs.getUser();
gs.print(newUser.getUserByID('abel.tuter').getFirstName());
```

---

## Lesson 4: GlideSystem (gs)

GlideSystem runs on the server side and provides methods for information about the system and the current logged-in user. The global object is `gs`. Many methods make it easy to include dates in query ranges, and it is often used in filters and reports.

> Run these from **Scripts - Background**.

### Common gs methods

| Category | Methods |
| --- | --- |
| Messages | `addInfoMessage()`, `addErrorMessage()`, `getErrorMessage()`, `getInfoMessage()`, `flushMessages()` |
| Current user | `getUser()`, `getUserID()`, `getUserName()`, `getUserDisplayName()`, `hasRole()`, `hasRoleInGroup()` |
| Session | `getSession()`, `getSessionID()`, `isInteractive()`, `isLoggedIn()`, `setRedirect()` |
| Date helpers | `now()`, `nowDateTime()`, `nowNoTZ()`, `daysAgo()`, `hoursAgo()`, `beginningOf*`, `endOf*`, `yesterday()`, `lastWeek()` |
| Misc | `getProperty()`, `setProperty()`, `tableExists()`, `getDisplayColumn()`, `getMessage()`, `nil()`, `isDebugging()` |

### Examples

```javascript
gs.addInfoMessage('Start date should be before end date');
gs.addErrorMessage('Please provide valid info');

var currentUser = gs.getUser();
gs.print(currentUser.getEmail());
gs.print(gs.getUserDisplayName());
gs.print(gs.getUserID());
gs.print(gs.getUserName());
gs.print(gs.getUserNameByUserID('admin'));
gs.print(gs.hasRole('itil'));
gs.print(gs.isInteractive());
```

Role within a group:

```javascript
var group = new GlideRecord('sys_user_group');
group.addQuery('name', 'software');
group.setLimit(1);
group.query();
if (group.next()) {
    if (gs.hasRoleInGroup('itil', group)) {
        gs.print('User has role in group');
    } else {
        gs.print('User does NOT have role in group');
    }
}
```

Avatar, initials, messages:

```javascript
var userPhoto = gs.getUser().getAvatar();
gs.addInfoMessage('User avatar ID: ' + userPhoto);

var userInitials = gs.getUser().getInitials();
gs.addInfoMessage('User initials: ' + userInitials);

gs.flushMessages(); // clear session messages
```

Date helpers:

```javascript
gs.print(gs.beginningOfLastMonth());
gs.print(gs.beginningOfLastWeek());
gs.print(gs.beginningOfNextWeek());
gs.print(gs.beginningOfNextYear());
gs.print(gs.beginningOfThisMonth());
gs.print(gs.beginningOfThisQuarter());
gs.print(gs.beginningOfThisWeek());
gs.print(gs.beginningOfThisYear());
gs.print(gs.beginningOfToday());
gs.print(gs.beginningOfTomorrow());
gs.print(gs.beginningOfYesterday());

gs.print(gs.daysAgo(4));
gs.print(gs.daysAgoEnd(10));
gs.print(gs.daysAgoStart(4));
gs.print(gs.hoursAgo(7));
gs.print(gs.hoursAgoStart(2));

gs.print(gs.endOfLastMonth());
gs.print(gs.endOfLastWeek());
gs.print(gs.endOfLastYear());
gs.print(gs.endOfNextMonth());
gs.print(gs.endOfNextWeek());
gs.print(gs.endOfNextYear());
gs.print(gs.endOfThisMonth());
gs.print(gs.endOfThisQuarter());
gs.print(gs.endOfThisWeek());
gs.print(gs.endOfThisYear());
gs.print(gs.endOfToday());
gs.print(gs.endOfTomorrow());
gs.print(gs.endOfYesterday());

gs.print(gs.now());
gs.print(gs.nowDateTime());
gs.print(gs.nowNoTZ());
gs.print(gs.lastWeek());
```

Properties and redirect:

```javascript
gs.setProperty('glide.foo', 'bar', 'foo');
gs.info(gs.getProperty('glide.foo'));

gs.setRedirect('com.glideapp.servicecatalog_cat_item_view.do?sysparm_id=...&sysparm_user=' + current.sys_id);
```

---

## Lesson 5: GlideSession

GlideSession lets you find information about the current session.

```javascript
// putClientData / getClientData
var myData = gs.getSession();
myData.putClientData('userName', 'Srinivas');
var clientData = gs.getSession().getClientData('userName');
gs.print(clientData);

// clearClientData
gs.getSession().clearClientData('userName');
clientData = gs.getSession().getClientData('userName');
gs.print(clientData);

// Language, roles, time zone
var session = gs.getSession();
gs.info(session.getLanguage());
gs.info(gs.getSession().getRoles());
gs.print(session.getTimeZoneName());

// Interactive / logged in
gs.info(gs.getSession().isInteractive());
gs.info(gs.getSession().isLoggedIn());
```

> The role list from `getRoles()` does not reflect changes made during the current session. The user must log out and back in to get an updated list.

---

## Lesson 6: GlideDate

GlideDate works with date fields on forms. The global object is `GlideDate`.

```javascript
var date = new GlideDate();
gs.print(date);

gs.print(date.getByFormat('dd-MM-yyyy'));
gs.print(date.getDayOfMonthNoTZ());
gs.print(date.getDisplayValue());
gs.print(date.getDisplayValueInternal());
gs.print(date.getMonthNoTZ());
gs.print(date.getValue());
gs.print(date.getYearNoTZ());

// setDisplayValue / setValue
var d = new GlideDate();
d.setDisplayValue('2020-04-18');
gs.print(d.getValue());

var d2 = new GlideDate();
d2.setValue('2020-04-18');
gs.print(d2.getValue());

// subtract — difference between two GlideDate values
var firstDate = new GlideDate();
firstDate.setDisplayValue('2020-01-25');
var secondDate = new GlideDate();
secondDate.setDisplayValue('2020-01-29');
var difference = GlideDate.subtract(firstDate, secondDate);
gs.info(difference.getDisplayValue());
```

---

## Lesson 7: GlideDateTime

GlideDateTime performs operations on date-time objects, including date-time calculations, formatting, and conversions. It runs on the server side.

```javascript
var gdt = new GlideDateTime();
gs.print(gdt);

gdt.addDays(4);
gs.print(gdt);

// Local and UTC variants
var gdt2 = new GlideDateTime('2020-01-28 08:00:00');
gdt2.addDaysLocalTime(4);
gs.print(gdt2.getLocalDate());

var gdt3 = new GlideDateTime('2020-01-28 08:00:00');
gdt3.addDaysUTC(4);
gs.print(gdt3.getDate());
```

Add months, seconds, weeks, and years:

```javascript
var gdt = new GlideDateTime();
gdt.addMonths(2);
gs.print(gdt.getDate());

gdt.addSeconds(45);
gs.print(gdt.getValue());

gdt.addWeeks(5);
gs.print(gdt.getValue());

gdt.addYears(3);
gs.print(gdt.getValue());
```

Compare and check equality:

```javascript
var initDate = new GlideDateTime('2011-08-01 12:00:00');
var compDate1 = new GlideDateTime('2011-08-01 12:00:00');
var compDate2 = new GlideDateTime('2011-07-31 12:00:00');
var compDate3 = new GlideDateTime('2011-08-04 16:00:00');
gs.info(initDate.compareTo(compDate1)); // 0 (equal)
gs.info(initDate.compareTo(compDate2)); // 1 (after)
gs.info(initDate.compareTo(compDate3)); // -1 (before)

var gdt = new GlideDateTime('2020-04-19 00:00:00');
gs.print(gdt.equals('2020-04-15 00:00:00'));
```

Getters:

```javascript
var gdt = new GlideDateTime();
gs.print(gdt.getDate());
gs.print(gdt.getDayOfMonth());
gs.print(gdt.getDayOfMonthLocalTime());
gs.print(gdt.getDayOfWeek());
gs.print(gdt.getDaysInMonth());
gs.print(gdt.getDisplayValue());
gs.print(gdt.getDisplayValueInternal());
gs.print(gdt.getDSTOffset());
gs.print(gdt.getLocalDate());
gs.print(gdt.getLocalTime());
gs.print(gdt.getMonth());
gs.print(gdt.getNumericValue());
gs.print(gdt.getValue());
gs.print(gdt.getYear());
gs.print(gdt.hasDate());
```

Error message handling:

```javascript
var gdt = new GlideDateTime('2011-08-31 aa:00:00'); // bad value
gs.print(gdt.isValid());    // false
gs.print(gdt.getErrorMsg()); // reason
```

Setters and subtract:

```javascript
var gdt = new GlideDateTime();
gdt.setDayOfMonth(4);
gs.print(gdt.getDayOfMonth());

var g2 = new GlideDateTime('2011-02-02 12:00:00');
g2.setDisplayValue('2011-01-01 12:00:00');
gs.print(g2.getValue());

var g3 = new GlideDateTime();
g3.setMonth(1);
gs.print(g3.getMonth());

var g4 = new GlideDateTime('2011-01-01 12:00:00');
g4.setValue('2011-02-02 08:00:00');
gs.print(g4.getValue());

var g5 = new GlideDateTime();
g5.setYearUTC(2020);
gs.print(g5.getYearUTC());

var g6 = new GlideDateTime('2011-08-31 08:00:00');
var gtime1 = new GlideTime();
gtime1.setValue('00:00:20');
g6.subtract(gtime1);
gs.print(g6.getTime());

var g7 = new GlideDateTime('2011-08-31 08:00:00');
gs.print(g7.toString()); // same as getValue()
```

---

## Lesson 8: GlideAggregate

GlideAggregate creates database aggregation queries. It extends GlideRecord and provides COUNT, SUM, MIN, MAX, AVG (and STDDEV) queries. It is useful for customized reports and calculated fields and works on number fields.

**Count active software incidents**

```javascript
var count = new GlideAggregate('incident');
count.addEncodedQuery('active=true');
count.addQuery('category', 'software');
count.addAggregate('COUNT');
count.query();
var incidents = 0;
if (count.next()) {
    incidents = count.getAggregate('COUNT');
}
gs.info(incidents);
```

**Multiple aggregates on one field**

```javascript
var incidentGA = new GlideAggregate('incident');
incidentGA.addQuery('category', 'software');
incidentGA.setGroup(false);
incidentGA.addAggregate('COUNT', 'sys_mod_count');
incidentGA.addAggregate('SUM', 'sys_mod_count');
incidentGA.addAggregate('AVG', 'sys_mod_count');
incidentGA.addAggregate('MIN', 'sys_mod_count');
incidentGA.addAggregate('MAX', 'sys_mod_count');
incidentGA.addAggregate('STDDEV', 'sys_mod_count');
incidentGA.query();
if (incidentGA.next()) {
    gs.info('COUNT: ' + incidentGA.getAggregate('COUNT', 'sys_mod_count'));
    gs.info('SUM: ' + incidentGA.getAggregate('SUM', 'sys_mod_count'));
    gs.info('AVG: ' + incidentGA.getAggregate('AVG', 'sys_mod_count'));
    gs.info('MIN: ' + incidentGA.getAggregate('MIN', 'sys_mod_count'));
    gs.info('MAX: ' + incidentGA.getAggregate('MAX', 'sys_mod_count'));
    gs.info('STDDEV: ' + incidentGA.getAggregate('STDDEV', 'sys_mod_count'));
}
```

**Group by category**

```javascript
var count = new GlideAggregate('incident');
count.addQuery('active', '=', 'true');
count.addAggregate('COUNT', 'category');
count.query();
while (count.next()) {
    var category = count.category;
    var categoryCount = count.getAggregate('COUNT', 'category');
    gs.info('There are currently ' + categoryCount + ' incidents with a category of ' + category);
}
```

**Trend — count incidents opened each quarter**

```javascript
var ga = new GlideAggregate('incident');
ga.addAggregate('COUNT');
ga.addTrend('opened_at', 'quarter');
ga.query();
while (ga.next()) {
    gs.info([ga.getValue('timeref'), ga.getAggregate('COUNT')]);
}
```

**MIN/MAX/AVG grouped by category**

```javascript
var count = new GlideAggregate('incident');
count.addAggregate('MIN', 'sys_mod_count');
count.addAggregate('MAX', 'sys_mod_count');
count.addAggregate('AVG', 'sys_mod_count');
count.groupBy('category');
count.query();
gs.info(count.getRowCount());
while (count.next()) {
    var min = count.getAggregate('MIN', 'sys_mod_count');
    var max = count.getAggregate('MAX', 'sys_mod_count');
    var avg = count.getAggregate('AVG', 'sys_mod_count');
    var category = count.category.getDisplayValue();
    gs.info(category + ' Update counts: MIN = ' + min + ' MAX = ' + max + ' AVG = ' + avg);
}
```

---

## Next steps

- Continue to [Client-Side Scripting](client-side-scripting.md) for Client Scripts and UI Actions.
- See [Server-Side Scripting](server-side-scripting.md) for Scheduled Jobs, Business Rules, Script Includes, and GlideAjax.
