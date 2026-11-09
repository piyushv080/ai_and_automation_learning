# Server-Side Scripting — Scheduled Jobs, Business Rules, Script Includes, and GlideAjax

Study notes for automating work on the server side. This page covers Scheduled Jobs (Lesson 11), Business Rules and Script Includes (Lesson 12), and GlideAjax from the ServiceNow Live book.

> Server-side scripts run on the ServiceNow server and have access to the database. Test in a non-production instance before deploying to production.

---

## Lesson 11: Scheduled Jobs

Scheduled Jobs are automated pieces of work performed at a specific time or on a recurring schedule. A scheduled job runs a script or operation on the server at an interval you define. They remove administrative burden from ServiceNow administrators.

You can automate tasks such as:

- Generate and schedule records (incident, change, configuration item) from a template.
- Run and distribute a report automatically.
- Run a business rule and perform whatever the rule contains.
- Schedule work at the end of a month or on weekdays.
- Execute scheduled jobs from scripts.
- Fire an email notification from a scheduled job.

Common scenarios:

- Deliver a specific report to stakeholders every day, week, or month.
- Create and assign a task record to a team every month.
- Email a report with complete information to stakeholders.
- Auto-close incidents in Pending Customer Action when the customer has not responded for days.
- Auto-close incidents that have been Resolved for a set period.
- Trigger events weekly, monthly, or at any period.

### Scheduled job tables

| Table | Purpose |
| --- | --- |
| `sysauto_script` | Scheduled Script Execution |
| `scheduled_import_set` | Scheduled Import Sets |
| `sysauto_template` | Scheduled Template Generation |
| `sysauto_report` | Scheduled Report |

### Exercise 1 — Generate and distribute a report by email

1. Navigate to **System Definition > Scheduled Jobs**.
2. Click **New**.
3. Select **Automate the generation and distribution of a report**.
4. Complete the scheduled job form and submit.

> Before testing, set the instance time zone: **Settings > Time Zone > GMT**.

### Exercise 2 — Auto-close resolved incidents every six months

1. Navigate to **System Definition > Scheduled Jobs**.
2. Click **New**.
3. Select **Automatically run a script of your choosing**.
4. Name: `All resolved incidents should get closed automatically`.
5. Active: `true`. Run: `Weekly`. Time Zone: `GMT`. Set the day and time.
6. Submit, then add this script:

```javascript
var eq = 'resolved_atONLast 6 months@javascript:gs.beginningOfLast6Months()@javascript:gs.endOfLast6Months()';
var gr = new GlideRecord('incident');
gr.addEncodedQuery(eq);
gr.query();
while (gr.next()) {
    gr.state = '7';
    gr.work_notes = 'All resolved incidents are closing through scheduled jobs';
    gr.update();
}
```

### Exercise 3 — Create an incident every Saturday at 9 AM

1. Navigate to **System Definition > Scheduled Jobs**.
2. Click **New**.
3. Select **Automatically generate something (a change, an incident, a ci, etc) from a template**.
4. Active: `true`. Run: `Weekly`. Time Zone: `GMT`. Set the time.
5. Generate This: `Network Servers Maintenance`.
6. Create a template: Name `Network Servers maintenance`, Table `Incident`, Active `true`, Short description `Network Server Maintenance`, Category `Network`, Subcategory `DNS`, Caller `ITIL User`.

---

## Lesson 12: Business Rules

Business Rules are server-side scripts that run when a record is displayed, inserted, updated, or deleted. Use them to update form values automatically when a condition is met, create events, send emails, invoke web services, and more. Business Rule records are stored in the `sys_script` table.

Business Rules run faster than many other scripts and are not affected by the browser. They can perform complex database lookups and assignment rules. Dot-walking many levels is possible, though three levels is often the recommended maximum.

### What Business Rules can do

- Update record fields when a database query runs.
- Modify date formats.
- Set field values on related records when a record is saved.
- Manage failed login attempts.
- Generate events.
- Determine if a user has a specific role.
- Send emails to customers.
- Generate and respond to events.
- Display an info message when a record is inserted.
- Compare two dates to determine which comes first.
- Determine if today is a weekend or weekday.
- Calculate when the next quarter starts.
- Initiate integration and API calls to other systems.
- Invoke web services, send REST messages, and retrieve results.
- Change field values and write log messages.
- Abort an insert or update when data is invalid.
- Display a message on the form.

### Types of Business Rules

There are four types, selected in the **When** dropdown:

| Type | Runs | Use for |
| --- | --- | --- |
| **Before** | Before the database operation, before data is saved | Modify field values before the write |
| **After** | Immediately after the write, before the form renders | Update related records that must display immediately |
| **Async** | After the write, asynchronously on a scheduler thread | Work that does not need immediate display |
| **Display** | When a form loads and a record is read | Populate `g_scratchpad` for client scripts |

**Before** — Code executes when the user submits the form, before data is saved. Use it when field values must be modified before database access. Example: concatenate two fields into the Description.

**After** — Executes synchronously immediately after the database operation and before the resulting form renders. Use it when no changes are needed to the accessed record but related records must be updated. Example: propagate a change from a parent record to its children.

**Async** — Like After, runs after the database operation, but asynchronously on a different processing thread. It is queued by a scheduler and runs as soon as possible, letting the current transaction finish without waiting. Prefer Async over After whenever possible. Use it for things like calculating metrics and SLAs.

**Display** — Executes when a form loads and a record is read from the database. It must complete before control of the form is given to the user. Its purpose is to populate `g_scratchpad`, which is passed to the client. Do not use `current.update()` in a display Business Rule.

### Business rule process flow

A table can have multiple Business Rules of different When types. They run in a defined order based on type and order value. Business Rules run based on two criteria:

1. **When to run** — the timing/type of Business Rule (Before, After, Async, Display).
2. **When the action occurs** — the database operation: Insert, Update, Query, Delete.

The rule fires when both the condition and the database operation match.

### Prevent recursive Business Rules

Do not use `current.update()` inside a Business Rule. `update()` triggers Business Rules again on the same table, potentially causing a rule to call itself repeatedly. When ServiceNow detects recursion it stops it and logs an error, but this can hurt performance. Prevent recursion with `current.setWorkflow(false)`, which stops Business Rules and related functions from running on that database access. Use `update()` together with `setWorkflow(false)` only in special circumstances.

### Global variables in Business Rules

| Variable | Description |
| --- | --- |
| `current` | State of the record being worked on |
| `previous` | Previous state of the record before update/delete |
| `g_scratchpad` | Object available in Display Business Rules to pass data to the client |
| `gs` | GlideSystem server-side methods |

### Exercise 1 — Auto-assign group by category (configuration)

Requirement: When Category is Network and Subcategory is VPN on the Incident table, the Assignment Group should be Network.

1. Navigate to **System Definition > Business Rules**.
2. Click **New**.
3. Name: `Auto Assign to Assignment Group`. Table: `Incident`. Active: `true`.
4. When to run: Insert `true`, Update `true`. Condition: Category `Network`, Subcategory `VPN`.
5. Action: Set field values — Assignment Group → Network. Add message: `This ticket has been assigned to Network assignment group`.

### Exercise 2 — Auto-assign group with a script

Requirement: When Category is Network, set Assignment Group to Network Assignment Group.

1. Name: `Auto assign to Group`. Table: `Incident`.
2. Advanced: `true`. Insert: `true`. Update: `true`.
3. Condition: Category is Network.

```javascript
current.assignment_group = 'Network Assignment Group';
```

### Before Business Rules

Use cases:

- Automatically change form field values when conditions are met.
- Create events for email notifications and script actions.
- Abort an update if the form does not have the expected value.
- Auto-populate field values while creating an incident.
- Prevent deletion when a condition does not match.
- Update a date before inserting a record.

**Exercise 3 — Prevent creation (configuration)**

Requirement: A user cannot create a new incident when Category is Inquiry/Help and Assignment Group is Service Desk.

1. Name: `User should not create Incident`. Table: `Incident`. Active: `true`.
2. When: `Before`. Order: `300`. Insert: checked.
3. Filter Conditions: Category `Inquiry/Help`, Assignment Group `Service Desk`.
4. Actions: Abort action checked. Message: `User should not be able to create new incident record with above criteria`.

**Exercise 4 — Prevent duplicate incident (script)**

Requirement: A user cannot create a new incident when an existing incident has the same Short Description, Category, and Caller.

```javascript
var gr = new GlideRecord('incident');
gr.addQuery('short_description', current.short_description);
gr.addQuery('category', current.category);
gr.addQuery('caller_id', current.caller_id);
gr.query();
if (gr.hasNext()) {
    gs.addErrorMessage('User should not create new incident with same details');
    current.setAbortAction(true);
}
```

**Exercise 5 — Prevent priority change**

Requirement: A user cannot change Priority once an incident is created.

1. Name: `User should not change the Priority once created an incident`. Table: `Incident`.
2. When: `Before`. Order: `200`. Update: `true`.
3. Filter Conditions: Priority changes.
4. Actions: Add message + Abort action checked. Message: `User should not change the Priority once created an incident ticket`.

**Exercise 6 — Prevent deletion in New state**

Requirement: A user cannot delete an incident in New state.

1. Name: `User should not delete Incident ticket`. Table: `Incident`.
2. When: `Before`. Order: `350`. Delete: `true`.
3. Filter Conditions: State is New.
4. Advanced: abort the action and add a message `User should not delete incident ticket in NEW State`.

### After Business Rules

Use cases:

- Show info or error messages after create/update.
- Create an incident task after an incident is created.
- Update the work notes of a child incident when the parent's work notes change.
- Create a knowledge article after an incident closes.
- Delete associated records after a parent record is deleted.

**Exercise 7 — Info message after creation**

Requirement: Display an info message after a new incident is created: `New incident has been created`.

1. Name: `Display info message`. Table: `Incident`.
2. When: `After`. Order: `100`. Insert: `true`.
3. Add message.

**Exercise 8 — Info message with caller and number**

```javascript
gs.addInfoMessage('New incident has been created by ' + current.caller_id.getDisplayValue()
    + ' and incident number ' + current.number);
```

**Exercise 9 — Update work notes on assignment group change**

Requirement: When the Assignment Group changes, update work notes and display an info message.

1. Name: `Worknotes should be update on assignment group change`. Table: `Incident`.
2. When: `After`. Update: `true`. Order: `300`.
3. Filter Condition: Assignment Group changes.

```javascript
current.work_notes = 'Assignment group changed to ' + current.assignment_group.getDisplayValue();
current.update();
gs.addInfoMessage('Assignment group updated');
```

**Exercise 10 — Create a change request from an incident**

Requirement: When Incident state changes to On Hold with On Hold Reason Awaiting Change, create a change record. Set the current user as Requested By, copy the short description, set Type to Normal, and display an info message.

```javascript
var gr = new GlideRecord('change_request');
gr.initialize();
gr.setValue('requested_by', gs.getUserID());
gr.setValue('short_description', current.short_description);
gr.setValue('type', 'Normal');
gr.insert();
gs.addInfoMessage(gs.getMessage('New change has {0} created', gr.number));
```

**Exercise 11 — Close incidents when a problem closes**

```javascript
var gr = new GlideRecord('incident');
gr.addQuery('problem_id', current.sys_id);
gr.query();
while (gr.next()) {
    gr.state = 7;
    gr.close_code = 'Solved (Work Around)';
    gr.close_notes = 'Successfully fixed issue';
    gr.setWorkflow(false); // don't run other business rules
    gr.update();
}
```

**Exercise 12 — Create an incident task automatically**

Requirement: When an incident is created, create an incident task and copy Caller, Category, Priority, Short Description, Description, State, and Work Notes.

```javascript
var gr = new GlideRecord('incident_task');
gr.initialize();
gr.incident = current.sys_id;
gr.priority = current.priority;
gr.assignment_group = current.assignment_group;
gr.assigned_to = current.assigned_to;
gr.cmdb_ci = current.cmdb_ci;
gr.work_notes = 'New incident task has created from ' + current.number;
gr.short_description = current.short_description;
gr.description = current.description;
gr.insert();
gs.addInfoMessage('Incident task has created # ' + gr.number);
```

**Exercise 13 — Date validation**

Requirement: Create two custom fields (Start Date, End Date) on Incident. End date must be greater than start date.

```javascript
var st_date = current.u_start_date.getGlideObject().getNumericValue();
var end_date = current.u_end_date.getGlideObject().getNumericValue();
if (st_date > end_date) {
    gs.addErrorMessage('Start date can not be greater than end date');
    current.setAbortAction(true);
}
```

### Async Business Rules

Async Business Rules run in the background and handle work that does not need to be shown to the user after insert/update — for example, calculating metrics and SLAs. When the scheduler runs the scheduled job created from the Business Rule, the system executes it after the user submits the form and the record action occurs.

Use cases:

- Send a REST API call to another application on ticket update.
- Calculate SLAs and metrics.
- Create events through the event registry.
- Send email notifications through events.
- While importing data, insert a new user record and notify the user's manager.

> Async Business Rules cannot use `changes()`, `changesTo()`, or `changesFrom()`. They do not have access to the `previous` version of a record.

### After vs Async Business Rules

| After Business Rule | Async Business Rule |
| --- | --- |
| Used when fields must be updated and displayed immediately after save | Creates a background scheduler that runs based on node availability |
| Updates related objects that must display immediately | Runs in the background for work the user need not see |
| Executes synchronously | Executes asynchronously |
| Can access `previous` and `current` | Cannot access `previous` |
| User waits for the response | Runs later via the scheduler |

**Exercise 14 — Async notification when a critical network incident is created**

Create three objects: an event registry, a notification, and a Business Rule.

1. **Event Registry** — **System Policy > Events > Registry > New**.
   - Event name: `incident.critical.network`.
   - Table: `Incident`.
   - Fired by: `Business Rules`.
2. **Notification** — **System Notification > Email > Notification > New**.
   - Name: `Critical incident with network`. Table: `Incident`. Active: `true`.
   - Send when: `Event is fired`, event name `incident.critical.network`.
   - Event parm 1 contains recipients: `true`. Send event creator: `true`.
   - Subject: `New incident has been created by Caller: ${caller_id} and Category: ${category}`.
3. **Business Rule** — Name `Critical incident with network`, Table `Incident`, Advanced `true`.
   - When: `async`. Order: `100`. Insert: `true`.
   - Filter Conditions: Priority `1 - Critical`, Category `Network`.

```javascript
gs.eventQueue('incident.critical.network', current, current.assignment_group);
```

> To test an Async Business Rule, add log statements and check the `syslog` table, or update a record in another table from the script and verify the change.

### Display Business Rules

Display Business Rules get data from the server to the client through the `g_scratchpad` object.

Use cases:

1. Data is read from the database, display rules run, and the form is presented.
2. The `current` object is available and represents the record retrieved.
3. Field changes are temporary and not yet submitted to the database.
4. To the client, form values appear to be the database values.
5. The main purpose is the shared `g_scratchpad` object, which is sent to the client with the form.
6. Useful when a client script needs server data that is not part of the displayed record.
7. More efficient than a client script making a server callback when the data can be determined before the form displays.
8. `g_scratchpad` is empty by default and stores name/value pairs.

**Exercise 15 — Info message when fields are empty (configuration)**

Requirement: Display an info message when an incident opens and Assignment Group and Assigned to are empty.

1. Name: `Display info message on assignment group and assigned to are empty`. Table: `Incident`.
2. When: `display`. Order: `100`.
3. Filter Conditions: Assignment Group is empty, Assigned to is empty.
4. Add message: `Assignment group and Assigned to both are empty`.

**Exercise 16 — VIP caller via g_scratchpad**

Display Business Rule:

```javascript
// Condition: !current.isNewRecord()
g_scratchpad.is_vip = current.caller_id.vip;
```

Client Script (OnLoad):

```javascript
function onLoad() {
    if (!g_form.isNewRecord() && g_scratchpad.is_vip) {
        alert('Caller is VIP ' + g_scratchpad.is_vip);
    }
}
```

**Exercise 17 — Display incident details**

Display Business Rule:

```javascript
g_scratchpad.mail = current.caller_id.email;
g_scratchpad.pri = current.priority.getDisplayValue();
g_scratchpad.cat = current.category;
```

Client Script (OnLoad):

```javascript
function onLoad() {
    alert('Current Caller is ' + g_scratchpad.mail);
    alert('Current Priority is ' + g_scratchpad.pri);
    alert('Current Category is ' + g_scratchpad.cat);
}
```

**Exercise 18 — Count associated incidents**

```javascript
var gr = new GlideRecord('incident');
gr.addQuery('problem_id', current.sys_id);
gr.query();
gs.addInfoMessage('Associated incident count ' + gr.getRowCount());
```

### Getting data from server to client

There are three common ways to get data from server to client:

1. `g_scratchpad` (Display Business Rule)
2. `getReference` (client-side reference lookup)
3. `GlideAjax` (asynchronous server call)

**getReference example — show caller email**

```javascript
function onLoad() {
    g_form.getReference('caller_id', getMail);
}

function getMail(userEmail) {
    g_form.addInfoMessage('Current caller email is ' + userEmail.email);
}
```

---

## Script Includes

Script Includes are reusable server-side script logic that define a function or class. They execute only when explicitly called by other scripts. Types:

1. On demand / classless.
2. Extend an existing class.
3. Define a new class.

### On-demand Script Include

An on-demand (classless) Script Include defines a single function callable from other server-side scripts. On-demand Script Includes can never be used client-side, even if Client callable is selected. The Script Include name must exactly match the function name.

```javascript
function sumTwoNums(a, b) {
    return a + b;
}
```

Used from a Business Rule:

```javascript
var total = sumTwoNums(2, 3);
gs.info(total);
```

### Exercise — Validate an email address

1. Add a string field (`Requested for email`) to the Incident table.
2. Create the Script Include: **System UI > Script Includes > New**.
   - Name: `validateEmailAddress`.
   - API Name: `global.validateEmailAddress`.
   - Accessible from: `This application scope only`.
   - Active: `true`.

```javascript
function validateEmailAddress(emailStr) {
    emailStr = emailStr + '';
    if (emailStr.match(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)) {
        return true;
    }
    return false;
}
```

Use it in a Business Rule:

```javascript
var isEmail = validateEmailAddress(current.u_requested_for_email);
if (isEmail == false) {
    gs.addErrorMessage(current.u_requested_for_email + ' is not a valid email address. You must provide a valid email address.');
    current.setAbortAction(true);
}
```

---

## GlideAjax

GlideAjax lets a client script call server-side code in a Script Include. General steps:

1. Create a GlideAjax instance, passing the Script Include class name.
2. Call `addParam` with `sysparm_name` set to the Script Include method name.
3. (Optional) Call `addParam` again for additional parameters.
4. Execute the server-side code with `getXML()`.

> `getXML()` is preferred because it is asynchronous and does not block other client code. `getXMLWait()` exists but is not recommended — it can make the application appear unresponsive and is not available to scoped applications.

### GlideAjax syntax example

```javascript
var ga = new GlideAjax('HelloWorld'); // Script Include class
ga.addParam('sysparm_name', 'helloWorld'); // method name
ga.addParam('sysparm_user_name', 'Bob');
ga.getXML(HelloWorldParse);

function HelloWorldParse(response) {
    var answer = response.responseXML.documentElement.getAttribute('answer');
    alert(answer);
}
```

### Exercise — Client-callable Script Include extending GlideAjax

Requirement: Retrieve the Requested for user's email address from the User table.

1. Add two fields to the Incident table: `Requested for` (reference) and `Requested for email` (string).
2. Create the Script Include: **System UI > Script Includes > New**.
   - Name: `getEmailAddress`.
   - Accessible from: `This application scope only`.
   - Active: `true`.
   - Client callable: `true`.

```javascript
var getEmailAddress = Class.create();
getEmailAddress.prototype = Object.extendsObject(global.AbstractAjaxProcessor, {
    getEmail: function () {
        var userRecord = new GlideRecord('sys_user');
        userRecord.get(this.getParameter('sysparm_userID'));
        return userRecord.email + '';
    },
    type: 'GetEmailAddress'
});
```

3. Create the Client Script: **System Definition > Client Scripts > New**.
   - Name: `Get Email Address Through Script Include`.
   - Table: `Incident`. UI Type: `All`. Type: `OnChange`. Active: `true`.

```javascript
function onChange(control, oldValue, newValue, isLoading, isTemplate) {
    if (isLoading || newValue === '') {
        return;
    }
    var getEmailAddr = new GlideAjax('GetEmailAddress');
    getEmailAddr.addParam('sysparm_name', 'getEmail');
    getEmailAddr.addParam('sysparm_userID', g_form.getValue('u_requested_for'));
    getEmailAddr.getXML(populateEmailField);

    function populateEmailField(response) {
        var emailFromScriptInclude = response.responseXML.documentElement.getAttribute('answer');
        g_form.clearValue('u_requested_for_email');
        g_form.setValue('u_requested_for_email', emailFromScriptInclude);
        g_form.setDisabled('u_requested_for_email', true);
    }
}
```

> **How does ServiceNow know which Script Include and method to call?** Pass the Script Include name when instantiating GlideAjax. `addParam('sysparm_name', ...)` selects the method.

### Core concepts recap

- Server-side scripts execute on the ServiceNow server and have database access.
- Business Rules are triggered by database operations: query, update, insert, delete.
- Server-side APIs include GlideRecord, GlideSystem, GlideSession, GlideDate, GlideDateTime, and GlideAggregate.
- Business Rule logic executes relative to the database operation: before, after, async, display.
- Debug Business Rules with the JavaScript Debugger, Debug Business Rule (Details), the application log, and the Script Tracer.
- Script Includes are reusable server-side logic: on-demand (single function, not client-callable), extend a class (inherit properties, commonly GlideAjax), or create a new class (often a Utils Script Include with an `initialize` function).

### Interview questions

**Q1. Which classes are part of the server-side API?**
`GlideSystem (gs)`, `GlideDateTime`, and `GlideDate`. The server-side GlideUser class does not use the `g_user` object.

**Q2. When do before Business Rules execute?**
Before records are written to the database.

**Q3. Difference between after and async Business Rules?**
Both run after records are written. After runs immediately; async creates scheduled jobs that run soon after.

**Q4. Which are NOT GlideRecord methods?**
`addOrQuery()` and `addAndQuery()`. Multiple `addQuery()` calls are ANDed; to explicitly AND/OR, use GlideQueryCondition.

**Q5. Which statements about the `current` object are NOT true?**
Its property values never change; `current` and `previous` are always identical; its properties are the same for all Business Rules. (Values can change, they are sometimes identical, and properties depend on the table.)

**Q6. What does an empty Business Rule Condition field return?**
`true` — the script only runs if the Condition returns true.

**Q7. Valid dot-walking syntax?**
`current.u_requested_for.userID` — the form is `object.related_object.field_name`.

**Q8. Which statements about Script Includes are true?**
All of them: reusable server-side logic; can extend a class; can define a new class or function; can be client callable; execute only when explicitly called.

---

## Next steps

- Continue to [Flow Designer and Knowledge Management](flow-designer-and-knowledge.md).
- Review [Glide APIs](glide-apis.md) for the server-side classes used here.
- Review [Client-Side Scripting](client-side-scripting.md) for the client half of these patterns.
