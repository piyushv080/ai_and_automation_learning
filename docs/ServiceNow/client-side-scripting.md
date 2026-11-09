# Client-Side Scripting — Client Scripts and UI Actions

Study notes for configuring forms and user interactions on the client side. This page covers Client Scripts (Lesson 9) and UI Actions (Lesson 10) from the ServiceNow Live book.

## Client-side and server-side components

Understanding where a script runs helps you choose the right tool.

**Client-side components**

- Client Scripts
- UI Policy
- UI Scripts
- Catalog Client Script
- Catalog UI Policy
- Widget client script
- UI Pages — client script

**Server-side components**

- Business Rules
- Script Includes
- Script Actions
- Scheduled Jobs
- Fix Scripts
- Workflow run script
- Email Scripts
- Installation Exits
- ACL scripts
- Transform map scripts
- Field map scripts
- UI Actions
- UI Pages — processing script
- UI Macros

---

## Lesson 9: Client Scripts

Client Scripts run JavaScript on the client side (the browser) when client-based events occur — for example, when a form loads, is submitted, or a field value changes, or when a cell value is edited in a list view. They configure forms, form fields, and field values while a user works with a form.

Client Scripts can:

1. Make a field mandatory or optional.
2. Display a message based on field values.
3. Make a field read-only or writable.
4. Make a field visible or invisible.
5. Add and modify choice list options based on the user's role.
6. Show info and error messages to the customer.
7. Add and remove choice values.
8. Set and get values from fields.
9. Display flash messages.
10. Add informational messages.

### Types of Client Scripts

| Type | Runs when | Typical use |
| --- | --- | --- |
| `onLoad()` | When the form first loads, before the user can enter data | Set default values, apply field rules |
| `onChange()` | When a particular field value changes | React to field changes |
| `onSubmit()` | When the form is submitted | Validate the form; return `false` to cancel submission |
| `onCellEdit()` | When a user edits a cell value in a list view | Validate list edits |

### Why Client Scripts

Client Scripts can reduce the time it takes a user to complete a form. However, if you control field values with a Client Script on a form, you must use another method to control those field values in a list.

Client Scripts can:

1. Restrict list editing for a particular table.
2. Create Business Rules or Access Control rules for list editing.
3. Work with Data Policies and UI Policies.
4. Restrict users in list view with `onCellEdit()`.
5. Validate when a form is submitted.
6. Validate when a form is loaded.
7. Reduce the need for time-consuming server lookups.
8. Use `g_scratchpad` and asynchronous GlideAjax lookups to get information from the server; `g_form.getReference()` is also available but is no longer recommended due to performance impact. Prefer `g_scratchpad` and asynchronous GlideAjax.

### Where Client Scripts run

With the exception of `onCellEdit()`, Client Scripts (`onLoad()`, `onChange()`, `onSubmit()`) apply only to forms and search pages. If you need to control field values in a list, use one of these instead:

1. Access Control rules to restrict who can read and edit field values, plus Business Rules to validate content.
2. UI Policies and Data Policies to validate content.
3. An `onCellEdit()` Client Script to validate content in list view.
4. Disable list editing for the table.

### Use of g_scratchpad

`g_scratchpad` passes information from the server to the client when you need data that is not available on the form. It is populated by a **Display** Business Rule (see [Server-Side Scripting](server-side-scripting.md)).

### Client-side Glide API classes

- **GlideAjax** — execute server-side script from the client.
- **GlideForm** — customize forms.
- **GlideList2** — customize (v2) lists, including normal and related lists.
- **GlideUser** — session information about the current user and roles.
- **GlideMenu** — customize UI context menu items.
- **GlideDialogWindow** — display a dialog window.

### Client Script exercises

**Exercise 1 — OnLoad field rules**

Requirement: When the Incident form loads:

1. Number and Priority fields are read-only.
2. Caller and Short Description fields are mandatory.
3. Configuration Item field is not shown (invisible).
4. Display an information message at the top of the form if the record is new.

Procedure:

1. Navigate to **System Definition > Client Scripts**.
2. Click **New**.
3. Name: `Initial Form Validation`.
4. Table: `Incident`.
5. UI Type: `All`.
6. Type: `OnLoad`.
7. Add the script.
8. Open a new Incident form to verify.

```javascript
function onLoad() {
    g_form.setReadOnly('number', true);
    g_form.setReadOnly('priority', true);
    g_form.setMandatory('caller_id', true);
    g_form.setMandatory('short_description', true);
    g_form.setDisplay('cmdb_ci', false);
    if (g_form.isNewRecord()) {
        g_form.addInfoMessage('Please fill all mandatory fields');
    }
}
```

**Exercise 2 — OnChange: On-Hold reason**

Requirement: When Incident State is On-Hold, the On Hold Reason field is visible and mandatory, with a warning below the field: "Please select at least one hold reason".

```javascript
function onChange(control, oldValue, newValue, isLoading, isTemplate) {
    if (isLoading) {
        return;
    }
    if (newValue == '3') { // On Hold
        g_form.setDisplay('hold_reason', true);
        g_form.setMandatory('hold_reason', true);
        g_form.showFieldMsg('hold_reason', 'Please select at least one hold reason', 'warning');
    } else {
        g_form.setMandatory('hold_reason', false);
    }
}
```

**Exercise 3 — OnSubmit: confirm critical incident**

Requirement: After submitting a Priority 1 (Critical) incident, display an alert asking "Are you submitting Priority one ticket" with OK and Cancel buttons.

```javascript
function onSubmit() {
    if (g_form.getValue('priority') == '1') {
        return confirm('Are you submitting Priority one ticket?');
    }
}
```

**Exercise 4 — OnChange: Resolved state**

Requirement: When Incident state is Resolved, Resolution Code and Resolution Notes are mandatory, and Assigned to and Assignment Group are not shown.

```javascript
function onChange(control, oldValue, newValue, isLoading, isTemplate) {
    if (isLoading) {
        return;
    }
    if (newValue == '6') { // Resolved
        g_form.setMandatory('close_code', true);
        g_form.setMandatory('close_notes', true);
        g_form.setDisplay('assigned_to', false);
        g_form.setDisplay('assignment_group', false);
    }
}
```

**Exercise 5 — OnChange: VIP caller**

Requirement: If the selected Caller is VIP, set Impact and Urgency to High, set Priority to 1 - Critical automatically, make Impact and Urgency read-only, and show an alert "Caller is VIP!".

> Tip: Mark a caller (for example, Fred Luddy) as VIP on the user record.

```javascript
function onChange(control, oldValue, newValue, isLoading, isTemplate) {
    if (isLoading || newValue === '') {
        return;
    }
    var caller = g_form.getReference('caller_id', function(ref) {
        if (ref.vip == 'true') {
            g_form.setValue('impact', 1);
            g_form.setValue('urgency', 1);
            g_form.setValue('priority', 1);
            g_form.setReadOnly('impact', true);
            g_form.setReadOnly('urgency', true);
            alert('Caller is VIP!');
        }
    });
}
```

**Exercise 6 — OnChange: Inquiry/Help category**

Requirement: When Category is Inquiry/Help, hide Subcategory, remove the 1-High choice from Impact and Urgency, and show an error below Impact: "Low impact is not preferring high priority".

```javascript
function onChange(control, oldValue, newValue, isLoading, isTemplate) {
    if (isLoading) {
        return;
    }
    if (newValue == 'inquiry') {
        g_form.setDisplay('subcategory', false);
        g_form.removeOption('impact', 1);
        g_form.removeOption('urgency', 1);
        g_form.showFieldMsg('impact', 'Low impact is not preferring high priority', 'error');
    }
}
```

**Exercise 7 — OnLoad: state choice restrictions**

Requirement:

1. When state is New, remove In-Progress, On-Hold, Resolved, Closed, and Cancelled choices.
2. When state is In-Progress or On-Hold, remove New and Closed choices.
3. When state is Resolved, remove New, In-Progress, On-Hold, and Cancelled choices.
4. When state is Closed, make the State field read-only.

```javascript
function onLoad() {
    var state = g_form.getValue('state');
    if (state == '1') { // New
        g_form.removeOption('state', 2);
        g_form.removeOption('state', 3);
        g_form.removeOption('state', 6);
        g_form.removeOption('state', 7);
        g_form.removeOption('state', 8);
    } else if (state == '2' || state == '3') { // In Progress / On Hold
        g_form.removeOption('state', 1);
        g_form.removeOption('state', 7);
    } else if (state == '6') { // Resolved
        g_form.removeOption('state', 1);
        g_form.removeOption('state', 2);
        g_form.removeOption('state', 3);
        g_form.removeOption('state', 8);
    } else if (state == '7') { // Closed
        g_form.setReadOnly('state', true);
    }
}
```

**Exercise 8 — OnChange: lock a closed incident**

Requirement: When Incident state is Closed, make Assigned to, Assignment Group, Category, Subcategory, Impact, Urgency, Contact Type, Short Description, and Caller read-only; hide the attachment icon; hide all related lists.

```javascript
function onChange(control, oldValue, newValue, isLoading, isTemplate) {
    if (isLoading) {
        return;
    }
    if (newValue == '7') { // Closed
        var fields = ['assigned_to', 'assignment_group', 'category', 'subcategory',
                      'impact', 'urgency', 'contact_type', 'short_description', 'caller_id'];
        fields.forEach(function (field) {
            g_form.setReadOnly(field, true);
        });
        g_form.disableAttachments();
        g_form.hideRelatedLists();
    }
}
```

**Exercise 9 — OnChange: work notes mandatory on priority change**

Requirement: When Priority changes, make Work Notes mandatory. Do not require it when the record is new, the form is loading, or `oldValue == newValue`.

```javascript
function onChange(control, oldValue, newValue, isLoading, isTemplate) {
    if (isLoading || g_form.isNewRecord() || oldValue == newValue) {
        return;
    }
    if (newValue != '') {
        g_form.setMandatory('work_notes', true);
        g_form.addInfoMessage('Please fill work notes');
    }
}
```

**Exercise 10 — OnCellEdit: block list edit to Closed**

Requirement: Do not allow a user to change Incident state to 7 - Closed from the list view. Cancel the action and show the alert "System not allow user to update cell value".

```javascript
function onCellEdit(sysIDs, table, oldValues, newValue, callback) {
    if (newValue == '7') {
        alert('System not allow user to update cell value');
        callback(false); // cancel the change
    } else {
        callback(true);
    }
}
```

**Exercise 11 — OnSubmit: show assignee**

Requirement: When submitting an incident, display the Assigned to name as an alert and give a confirmation message.

```javascript
function onSubmit() {
    var assignee = g_form.getDisplayValue('assigned_to');
    alert('Assigned to: ' + assignee);
    return confirm('Do you want to submit this incident?');
}
```

**Exercise 12 — OnChange: auto-assign group by category**

Requirement: Auto-assign the Assignment Group based on Category: Network → Network group, Hardware → Hardware group, Database → Database group, Software → Software group.

```javascript
function onChange(control, oldValue, newValue, isLoading, isTemplate) {
    if (isLoading) {
        return;
    }
    var groupMap = {
        network: 'Network',
        hardware: 'Hardware',
        database: 'Database',
        software: 'Software'
    };
    if (groupMap[newValue]) {
        g_form.setValue('assignment_group', groupMap[newValue]);
    }
}
```

**Exercise 13 — OnLoad: set caller to current user**

Requirement: Auto-set the Caller field to the current logged-in user, display a "Hello" message with the user's full name, and make Caller read-only.

```javascript
function onLoad() {
    g_form.setValue('caller_id', g_user.userID);
    g_form.setReadOnly('caller_id', true);
    alert('Hello ' + g_user.fullName);
}
```

**Exercise 14 — OnChange: date validation**

Requirement: Create two custom fields (Start Date, End Date) on the Incident table. Start Date must be before End Date and must not equal End Date. Show an error below End Date.

```javascript
function onChange(control, oldValue, newValue, isLoading, isTemplate) {
    if (isLoading) {
        return;
    }
    var start = g_form.getValue('u_start_date');
    var end = g_form.getValue('u_end_date');
    if (start && end && start >= end) {
        g_form.showFieldMsg('u_end_date', 'End date must be after start date', 'error');
    } else {
        g_form.hideFieldMsg('u_end_date');
    }
}
```

**Exercise 15 — OnChange: hide Resolution Information section**

Requirement: Hide the Resolution Information section when state is not Resolved.

```javascript
function onChange(control, oldValue, newValue, isLoading, isTemplate) {
    if (isLoading) {
        return;
    }
    var sections = g_form.getSections();
    // Find the Resolution Information section by its caption
    sections.forEach(function (section) {
        if (section.caption == 'Resolution Information') {
            g_form.setSectionDisplay(section, newValue == '6');
        }
    });
}
```

---

## Lesson 10: UI Actions

UI Actions define buttons, hyperlinks, list menus, and form context menus. Configure UI Actions to make the UI more interactive, customized, and specific to user activities. Administrators and UI Action admins create UI Actions.

When you need logic to run on a record event (create/update/state change), use a Business Rule. When a user must initiate the work, use a UI Action — the interface elements a user interacts with on a form or list.

### Where UI Actions appear

- A button on a form view.
- A context menu item on a form (open the form context menu or right-click the form header).
- A related link on a form.
- A button in the banner on top of a list.
- A button at the bottom of a list.
- A context menu item on a list.
- A menu item in the action choice list at the bottom of a list.
- A related link at the bottom of a list.

### UI Action exercises

**Exercise 1 — Server-side button: assign to current user**

Procedure:

1. Navigate to **System Definition > UI Actions**.
2. Click **New**.
3. Name: `Assigned to CLU`.
4. Table: `Incident`.
5. Order: `100`.
6. Action Name: `Assigned_to_clu`.
7. Show Update: checked. List Context Menu: checked. Active: checked.

```javascript
current.assigned_to = gs.getUserID();
current.update();
```

**Exercise 2 — Client-side button: auto assignment**

Procedure: Name `Auto Assignment Incident`, Table `Incident`, Order `790`, Action Name `Auto_assignment`, Show Insert and Show Update checked, Client `true`, List v2/v3 Compatible `true`, Active `true`, Form Button `true`, Onclick `autoAssignment()`.

```javascript
function autoAssignment() {
    var user = g_user.userID;
    g_form.setValue('assigned_to', user);
    g_form.setValue('work_notes', 'assigning to me');
    g_form.save();
}
```

**Exercise 3 — Create a child incident**

Requirement: A button on the Incident form creates a new child incident from the parent and redirects to the child. Name `Create Child Incident`, Order `800`, Action Name `create_childIncident`, Show Update checked, Form Button checked.

```javascript
var inc = new GlideRecord('incident');
inc.initialize();
inc.short_description = current.short_description;
inc.category = current.category;
inc.subcategory = current.subcategory;
inc.caller_id = current.caller_id;
inc.opened_by = gs.getUserID();
inc.impact = current.impact;
inc.urgency = current.urgency;
inc.parent = current.sys_id;
var sysID = inc.insert();
gs.addInfoMessage('New Child Incident ' + inc.number + ' created');
action.setRedirectURL(inc);
action.setReturnURL(current);
```

**Exercise 4 — Create incident tasks**

Requirement: A UI Action on an incident creates three incident tasks associated with the incident.

```javascript
var shortDesc = ['Incident Task1', 'Incident Task2', 'Incident Task3'];
for (var i = 0; i < shortDesc.length; i++) {
    var gr = new GlideRecord('incident_task');
    gr.initialize();
    gr.short_description = shortDesc[i];
    gr.description = current.short_description;
    gr.incident = current.sys_id;
    gr.insert();
}
action.setRedirectURL(current);
```

**Exercise 5 — Open problem form**

```javascript
var url = '/problem.do?sys_id=-1';
action.setRedirectURL(url);
```

**Exercise 6 — Send a notification through a UI Action**

This uses an event registry, an email notification, and a UI Action.

1. **Event Registry** — **System Policy > Events > Registry > New**.
   - Event name: `send.notification.assignedto`.
   - Table: `Incident`.
   - Fired by: `UI Action`.
2. **Notification** — **System Notification > Email > Notification > New**.
   - Name: `State Change to In Progress`.
   - Table: `Incident`.
   - Send when: `Event is fired`, event name `send.notification.assignedto`.
   - Send event creator: `true`.
   - Subject: `State changes to inprogress state: ${state}`.
3. **UI Action** — Name `State set to inprogress`, Table `Incident`, Order `100`, Action Name `state_inprogress`, Show Update checked, Form Button checked.

```javascript
current.state = 2;
current.update();
gs.eventQueue('send.notification.assignedto', current, gs.getUserName());
```

**UI Action on client and server — resolve an incident**

```javascript
function resolveIncident() {
    // Set state values and display mandatory fields
    g_form.setValue('incident_state', 6);
    g_form.setValue('state', 6);
    g_form.setValue('resolved_by', g_user.userID);
    gsftSubmit(null, g_form.getFormElement(), 'resolve_incident'); // must match Action name
}

// Code that runs without onclick — ensure no browser errors
if (typeof window == 'undefined') {
    serverResolve();
}

function serverResolve() {
    current.incident_state = IncidentState.RESOLVED;
    current.state = IncidentState.RESOLVED;
    current.resolved_by = gs.getUserID();
    current.update();
}
```

---

## Next steps

- Continue to [Server-Side Scripting](server-side-scripting.md) for Scheduled Jobs, Business Rules, Script Includes, and GlideAjax.
- Review [Glide APIs](glide-apis.md) for the server-side classes used inside these scripts.
