# Flow Designer and Knowledge Management

Study notes for low-code process automation and knowledge management. This page covers Flow Designer (Lesson 13) and Knowledge Management (Lesson 14) from the ServiceNow Live book.

---

## Lesson 13: Flow Designer

Flow Designer is an application within the ServiceNow platform (introduced in the Kingston release). It lets business owners use natural language to automate business processes, approvals, notifications, record operations, and task executions. It lowers risk for automation and accelerates development.

Flow Designer provides rich capabilities for automating processes, reducing repetitive tasks, and focusing on high-value work — including record operations without writing a single line of code. With Integration Hub, the platform integrates third-party applications and services for more comprehensive workflows. Out-of-the-box core actions and ServiceNow spokes (scoped applications with Flow Designer content) accelerate flow creation.

### Workflow Engine vs Flow Designer

**Workflow Engine** is the tried-and-true method that requires a more advanced developer and allows more complex scenarios, including many scripting blocks. It has many core activities for automating business processes.

**Flow Designer** lets users use natural language to automate tasks, record operations, notifications, and approvals without writing code. It consolidates process automation in one design environment. You build multi-step processes by dragging, dropping, and connecting steps.

If you are a beginner or not technical enough to build processes in code, Flow Designer is easier. It reduces scripting so it can be understood and created by non-technical users. Both can achieve the same end functionality, but Flow Designer is generally easier to use.

### Architecture of Flow Designer

A flow may contain various triggers, actions, subflows, and flow logic:

- **Trigger** — defines when to start the flow: record-based, schedule-based, or application-based.
- **Record-based triggers** run a flow after a record is created, updated, or deleted, and can use the triggering record as input.
- **Schedule-based triggers** run a flow at a specified date and time.
- **Application triggers** are added when the associated application is activated (for example, the MetricBase trigger when MetricBase is active).

### Sequence of a flow process

1. When the trigger conditions occur or an API directly calls the flow, the system creates an event queue entry to start the flow.
2. The scheduler processes the event and starts the flow in the background.
3. The system builds a process plan from the flow.
4. The system runs the process plan using the record that triggered the flow.
5. The system stores execution details in a context record.

### Flow states

| State | Meaning |
| --- | --- |
| Complete | The flow completed successfully |
| In Progress | The flow is running (a transaction quota rule prevents flows running longer than an hour by default) |
| Waiting | The flow is waiting for another event |
| Cancelled | The flow was cancelled by a user |
| Error | The flow encountered an error and stopped |

### Features and advantages

- Natural-language platform.
- Less coding.
- Handles complex data.
- Non-technical people can understand and use it.
- Create reusable actions.
- Can call Script Include code snippets.
- Schedule jobs for automating business processes.
- Includes Integration Hub.
- Connects third-party applications.
- Spokes feasibility.
- Decouples business policy from processes.
- Out-of-the-box flow triggers and actions.
- Reusable actions.
- Reduces development costs through a library of reusable flow components.
- Natural language assists no-code users configuring flow components.
- Process owners and developers can create, operate, and troubleshoot flows from a single interface.

### What is a flow?

A flow is a sequence of actions for automating a business process. A flow contains triggers and one or more actions.

### What is a trigger?

A trigger defines the conditions that start the flow. When the trigger condition is true, the system starts the flow. There are three types:

**Record triggers**

| Trigger | Description |
| --- | --- |
| Created | Starts the flow when a record is created in a specific table |
| Updated | Starts the flow when a record is updated in a specific table |
| Created or Updated | Starts when a record is either created or updated; requires selecting when to run |

Considerations for record triggers:

1. Trigger conditions should be unique on the same table.
2. Ignore records inserted or updated by import sets or update sets.
3. Replace record triggers on Service Catalog tables with Service Catalog application triggers.

**Date (schedule) triggers**

| Trigger | Description |
| --- | --- |
| Daily | Runs at a specific time every day |
| Weekly | Runs at a specific time every week |
| Monthly | Runs at a specific time every month |
| Run Once | Runs once at a specific time, not repeated |
| Repeat | Runs at regular intervals you define |

> Because flows are processed asynchronously, a flow with a date trigger may not run at the exact scheduled time. If triggered during core business hours, the system may process other queued events first.

**Application triggers**

| Trigger | Description |
| --- | --- |
| SLA Task | Starts a flow when a MetricBase trigger is met (requires MetricBase) |
| Metric Base | Starts a flow from a Service Catalog item request |
| Service Catalog | Starts a flow from an SLA definition record |
| Inbound Email | Starts a flow when the instance receives email |

### Flow Designer workspace and components

The Flow Designer user interface is used to create new flows and manage or modify existing flows.

### What is an action?

Actions define the work a flow performs. The platform includes many system actions:

- Create Record
- Update Record
- Delete Record
- Create Task
- Lookup Record
- Log
- Send Email
- Create Catalog Task
- Copy Attachment
- Delete Attachment
- Lookup Attachment
- Move Attachment
- Create Attachment
- Get Catalog Variable
- Ask for Approval
- Create or Update
- Wait For Condition

### Adding actions to a flow

1. Click **Select to add an Action, Flow Logic, or Subflow**.
2. Use the action selection pane. Actions are grouped by application and then by category (for example, ITSM has Assignment, Change, Incident, Problem, Request, and Miscellaneous).
3. Hover over an action to see details.

Every action has a different set of configuration fields depending on what it does. For example, Delete Record needs to know the table and field values. An annotation identifies the purpose of an action.

### Defining actions in order

As actions are added, they appear in numbered order. To add an action between two actions, hover over the transition line and click **Add Action, Flow Logic, or Subflow**. The tooltip shows where the action will be added.

### Flow Designer roles

| Role | Capability |
| --- | --- |
| `flow_designer` | Create new flows and modify existing flows |
| `flow_operator` | View flow execution details, dashboards, and logs |
| `action_designer` | Create and edit custom actions |

### Exercise 1 — Run a predefined flow (VTB Sample Flow)

Requirement: See the Visual Task Boards (VTB) owned by Beth Anglin. When a critical (Priority 1) incident is created, the VTB Sample Flow creates a Freeform VTB and creates a card for the incident in the To Do lane.

1. Navigate to **Flow Designer > Designer**.
2. Open **VTB Sample Flow**.
3. Identify the trigger (Incident created) and the conditions.
4. Review the actions.
5. Impersonate Fred Luddy and create a new Incident (Caller: Abel Tuter, Short Description: Network Issue, Priority: 1 - Critical, Assigned to: Fred Luddy).
6. In the flow tab, click **Test**, set the created Incident record, and click **Run Test**.
7. Check results: impersonate Fred Luddy, open **Self-Service > Visual Task Board**, open `P1-Icident`, and confirm the card is in the To Do lane.

### Exercise 2 — Critical-1 Incident Flow

Requirement: When a Priority 1 incident is created (priority 1 - Critical and active true):

1. If the Short Description contains "Issue with networking" (If condition).
2. Set Assignment Group to Network and add the Caller's Manager as a Watch List (Update Record).
3. Add a work note link to context.
4. Send an email to the Caller (CC the Caller's Manager) with the P1 reference, assignment group, and assigned to.
5. Add assigned group users to the task conversation.

Procedure:

1. **Flow Designer > Designer > Flow**.
2. Name: `Critical-1 Incident Flow`. Application: `Global`.
3. Add a trigger: `Created`, Table `incident`, Condition: `Active is true and Priority is 1 - Critical`.
4. Add Flow Logic **If** — Short Description contains "Issue with networking".
5. Add action **Update Record** — Record: Trigger → Incident Record; Assignment Group: Network; Watch List: Trigger → Incident Record → Caller → Manager → Name.
6. Add action **Add work note link to context** — Table: Incident; Record: Trigger → Incident Record; Journal Field: Work notes; Additional Comment: New P1 Incident created by Caller Name.
7. Add action **Send Email** — Target Record: Trigger → Incident Record; To: Caller → Email; CC: Caller → Manager → Email; Subject/Body with data pills.
8. Add action **Group Users to Task Conversation** — Task Record: Trigger → Incident; Group: Trigger → Incident → Assignment Group.
9. Save and **Activate** the flow, then test.

### Exercise 3 — Incident on hold with reason Awaiting Change

Requirement: When an Incident updates to On Hold with On Hold Reason Awaiting Change:

1. Ask for CAB approval.
2. If approved by at least 2 members, create a change request with Configuration Item, State, Short Description, Assignment Group, Assigned To, and Category.
3. Update the Incident (state Closed, work notes, resolution code, resolution notes).
4. Log an action.
5. Send an email to the assigned group (CC assigned to).
6. Post a Slack message.
7. Post an incident-details message to Microsoft Teams.

Trigger: Incident updated where state changes to 3 (On Hold) and On Hold Reason is Awaiting Change. Then add the approval, create-record, update-record, log, email, Slack, and Teams actions in order.

### Exercise 4 — Flow with a Service Catalog item

> Activate the Flow Designer support for the Service Catalog plugin (`com.glideapp.servicecatalog.flow_designer`). This plugin activates related plugins if needed.

Requirement: When a customer requests a role for a user through a Service Catalog item, the flow runs.

1. Create a catalog item (**Service Catalog > Catalog Definition > Maintain Items > New**) with two variables.
2. Create a flow: **Flow Designer > Designer > New flow**.
3. Add a trigger: Service Catalog.
4. Add **Get Catalog Variables** to get catalog item variables.
5. Add **Ask for Approval** for the requester's manager.
6. Add **If** — if the manager approved, continue.
7. Add **Create User Role Record** in `sys_user_has_role`.
8. Add **Else** — if rejected, log the reject reason.
9. Attach the flow to the catalog item: open the item, go to the **Process Engine** tab, add the flow, and save.
10. Test via **Try it**, then check **Executions** in Flow Designer.

### Interview questions (Flow Designer)

1. To include an SLA timer in your process, use — **Workflow**.
2. For a new business process to automate — **Flow Designer**.
3. On Kingston or newer, use — **Flow Designer**.
4. To modify existing logic already developed using Workflow — **Workflow**.
5. If you don't want to use script — **Flow Designer**.
6. Automated sequence of actions that run each time conditions are met — **Flow**.
7. Must evaluate true for a flow to execute — **Trigger Condition**.
8. Reusable operations provided in the base system — **Core Actions**.
9. Role granting access to flow operations information — **flow_operator**.
10. Role granting access to Flow Designer — **flow_designer**.
11. View runtime information in the design environment — **Execution Details**.
12. Created every time an action is added; stores variables the action generates — **Data Pills**.
13. Sequence of reusable actions started from a flow, subflow, or script — **Subflow**.
14. Required by a flow but not a subflow — **Trigger**.
15. Good practice: create subflows with this type of application — **Scoped Application**.
16. Passes data between a subflow and a flow/subflow/script — **Input and Output**.
17. Stores available data from each section for the subflow — **Data Panel**.
18. Section that can include actions, flow logic, or other subflows — **Actions**.
19. Flow logic that populates the output with data — **Assign Subflow Output**.
20. Controls if and when an action or subflow executes — **Flow Logic**.
21. Executes actions below when conditions are met — **If**.
22. Optional conditional to execute actions when an If is false — **Else if / Else**.
23. Executes actions on every record in a list — **For Each**.
24. Repeats actions until a condition is met — **Do the following until**.
25. Executes multiple actions at the same time — **Do the following parallel**.
26. Compares inputs to a decision table to pick actions — **Make a decision**.
27. Pauses the flow; requires duration and schedule — **Wait for a duration of time**.
28. Active and published workflows can be called from Flow Designer — **Call a Workflow**.
29. Used within If/Else if/Else to stop a flow/subflow — **End**.
30. Specifies what is returned in a subflow's output — **Assign Subflow Output**.
31. Role enabling a user to create and edit actions — **action_designer**.
32. Reusable operation enabling analysts to automate platform features — **Action**.
33. Container for actions, flow logic, and subflows — **Action Section**.
34. Default number of actions per flow — **50 Actions**.
35. ServiceNow-provided action available to any flow/subflow — **Core Action**.
36. Provides functionality not available in the base instance — **Custom Action**.
37. Roles required to use Action Designer — **action_designer or Admin**.
38. Grouping of reusable operations for easier discovery — **Spokes**.
39. Single reusable operation in Action Designer that carries out work — **Action Step**.
40. Three characteristics of a flow — performs the same predefined process each time; automates business logic; automated sequence of actions run when conditions are met.
41. A trigger specifies when a flow should execute — **True**.
42. Two benefits of testing flows in the design environment — triggers are simulated and automatically begin execution; multiple tests can run against the same test record.
43. Three characteristics of an action — reusable operations for automating system features; automates processes outside an instance; enables execution of third-party communication APIs.
44. Three trigger types — **Record-based, Schedule-based, Application**.
45. What subflow inputs do — specify the data available to the subflow when it launches.
46. When a flow is processed, execution details are stored in `syslog` — **False**.
47. Two roles granting full access to all Flow Designer features in every scope — **flow_designer, admin**.
48. A single reusable operation within an action — **Action Step**.
49. Two reasons to create Flow Designer content in a scoped app vs Global — scoped content is categorized and easier to maintain and release; scope protects an application and its artifacts.
50. Three components of an action — **Step, Output, Input**.
51. Run trigger option to execute every time the trigger condition is met — **For each unique change**.
52. If you repeatedly configure actions with the same settings — create a custom action preset with the required configuration.
53. Three benefits of Flow Designer — reusable component library reduces cost; natural language assists no-code users; owners and developers create, operate, and troubleshoot from one interface.
54. For a flow to be available for execution, it must be — **Published**.
55. What action outputs are — data variables used within the action.
56. An action specifies what the flow should execute — **True**.
57. What happens every time an action is added — data pills are created to capture runtime variables.
58. What Action Designer is used for — launch the design environment to create and edit actions.
59. Two characteristics of a subflow — contains input and output that pass data; sequences reusable actions started from a flow, subflow, or script.
60. Main purpose of flow logic — the programming structure to make decisions, branch, and make logical choices based on user input.
61. Why subflow properties are important — they set a protection policy and specify run-as settings.

---

## Lesson 14: Knowledge Management

Knowledge Management is an application within ServiceNow used to share information as a knowledge base. Knowledge bases may contain many knowledge articles. Information becomes knowledge once it is documented, actionable, and can be shared and consumed. The Knowledge Management Service Portal gives users a portal view of knowledge bases and articles.

Knowledge Management lets you create and categorize articles by business requirement. It can be classified into:

- User criteria for a knowledge base.
- Troubleshooting tips.
- Company rules and policies.
- Process documents.
- FAQs.
- Questions and answers.
- Technical solutions.
- Categorized articles.
- Feedback on each article.
- Self-service opportunities.
- Workflow for publishing and retiring articles.
- All users can search knowledge on the Service Portal.
- Articles provided on the Incident form.
- Articles organized by category.

### Knowledge Management roles

| Role | Responsibility |
| --- | --- |
| `knowledge_manager` | Administrative functions for knowledge bases they manage: defining categories, pinning important articles |
| `knowledge_admin` | Create new knowledge bases and manage all knowledge base administration |
| `admin` | Configure knowledge workflows, set knowledge properties, manage knowledge forms and homepages |
| Knowledge coach (team) | Review link quality, perform AQI surveys, leverage AQI coach |

### Usage and benefits

- Saves time and money.
- Reduces the time employees spend searching for documents and information.
- Minimizes resolution times and increases incident deflection.
- Reduces repeated services through knowledge articles.
- Supports self-service through articles, communications, and automated support.
- Helps users find answers fast.
- Helps help-desk agents and customers fulfill self-service opportunities.
- Increases user satisfaction.
- Promotes knowledge sharing.
- Drives continuous improvement.
- Tracks usage and governance.

### Knowledge Management life cycle

A knowledge article moves through these states. To be searchable and findable, an article must be in the **Published** state. ServiceNow includes four baseline stages:

| Stage | Description |
| --- | --- |
| Draft | Contributors create draft articles independently (or from existing task records) |
| Review | Subject Matter Experts (SMEs) and/or knowledge managers review for accuracy and formatting |
| Publish | Once reviewed and approved, the article is published to the knowledge base |
| Retire | The knowledge manager retires the article at its valid-to date or re-engages SMEs to publish a new version |

### Scope and requirements

Before starting, define your knowledge scope and requirements:

1. What are the objectives (quick wins and long-term goals)?
2. Who are the knowledge consumer groups (external customers, internal end users, service desk members, HR employees, regional users)? These define user criteria.
3. How should knowledge bases be structured? Visibility can be restricted at the knowledge base, article, and field level. Determine:
   - The categorization schema.
   - Knowledge base authors, owner, and managers.
   - Publish and retire workflows.
   - When knowledge can be created.
   - What notifications are needed and who receives them.
   - Whether consumers can provide feedback and how it is managed.
   - Organizational risks (weak documentation, key-person dependencies).
   - Whether to use knowledge templates and their key attributes.
   - Where knowledge sits today and whether to migrate, create new, or integrate.

### What is a knowledge base?

1. A knowledge base is a container of knowledge articles.
2. Knowledge bases are the highest level of organization and access control for articles.
3. Each knowledge base can have its own owner, manager, publish workflow, and retire workflow.
4. A knowledge base can enable or disable commenting, suggesting, category editing, and social Q&A.

### Exercise 1 — Create a knowledge base

1. Navigate to **Knowledge > Administration > Knowledge Bases**.
2. Click **New**.
3. Provide a unique name (for example, `HR Knowledge Base`).
4. Publish Workflow: `Knowledge - Instant Publish`.
5. Retire Workflow: `Knowledge - Instant Retire`.
6. Submit.

> Once created and saved, additional configurations can be set for the knowledge base.

### Exercise 2 — Create a knowledge base category

1. Navigate to **HR Knowledge Base > Knowledge Categories**.
2. Click **New**.
3. Label: `Payroll`, Value: `Payroll`.
4. Submit. Create another category such as `On-Boarding`.

### Exercise 3 — Create a knowledge article

1. Navigate to **HR Knowledge Base > Knowledge**.
2. Click **New**.
3. Knowledge base: `HR Knowledge Base`.
4. Category: `On-Boarding`.
5. Valid to: `2022-02-18`.
6. Article type: `Wiki`.
7. Wikitext: add content.
8. Submit. New articles default to the Draft state.

### Exercise 4 — Publish a knowledge article

1. Click **Publish** (no approval, because Instant Publish is selected).
2. Verify the article appears: navigate to **Incident > Create New**, type `Employee On-Boarding` in Short Description, and find the article.

### Exercise 5 — Retire a knowledge article

Retiring the latest published article does not create a new version; it marks the article as Retired.

1. Navigate to **HR Knowledge Base > On-Boarding > Employee On-Boarding**.
2. Retire the article by its valid-to date or forcefully.
3. Click **Retire** (no approval with Instant Retire).

> Once retired, an article is not visible to customers until it is republished.

### User criteria

User criteria restrict which users can read and contribute to a knowledge base. You can assign criteria to control read or contribute access. For example, enable all users in the Support department to contribute by creating a user criteria record with Department = Support and including it in the Can Contribute list.

**Exercise 6 — Configure user criteria**

Requirement: Visible only to HR Department people whose company is ACME China.

1. Navigate to **Knowledge > Administration > User Criteria**.
2. Click **New Criteria Record**.
3. Name: `HR Knowledge User Criteria`.
4. Companies: `ACME China`. Department: `HR`.
5. Submit.
6. Open the HR Knowledge Base record, open the **Can Read** tab, click **Edit**, and add the criteria.
7. Verify the criteria works as expected.

Related list meanings:

| Related list | Description |
| --- | --- |
| Can Read | Users can read articles in the knowledge base |
| Cannot Read | Users cannot read articles in the knowledge base |
| Can Contribute | Users can create, modify, and retire articles (also grants read access) |
| Cannot Contribute | Users cannot create, modify, retire, or read articles |

### Knowledge-Centered Service (KCS)

Knowledge-Centered Service (KCS) is a method for creating and continuously improving knowledge based on agent experience and the patterns observed through knowledge reuse. Knowledge Management provides features for article quality reviews, in-context knowledge capture, feedback management, the Article Quality Index (AQI), and knowledge demand insights.

KCS supports the **Solve & Evolve Loop** through reward learning (positive reinforcement), collaboration, and sharing and improving knowledge — letting agents and end users flag, fix, update, and create knowledge.

- The **Solve Loop** captures and reuses resolution steps.
- The **Evolve Loop** focuses on assessment and improvement.
- Together they form a self-correcting system.

Leveraging Knowledge Management in ServiceNow will:

- Reduce documentation search time.
- Increase incident and case deflection.
- Reduce resolution and fulfillment time.
- Enhance resolution collaboration across teams.
- Improve customer productivity and user experience.
- Improve resolution quality and consistency.
- Support the Solve & Evolve Loops.

### Knowledge Management workflows

ServiceNow uses workflow automation to publish and retire knowledge articles. There are two baseline workflows for publishing and two for retiring, which can be used as-is or customized.

**Publishing** — The Publish workflow moves an article between Draft and Publish, defines approvals, and defines notifications.

- One workflow publishes articles without approval (Instant Publish).
- The other requests approval before publishing.

**Retiring** — The Retire workflow moves an article between Publish and Retire, defines approvals, and defines notifications.

- One workflow retires articles without approval (Instant Retire).
- The other requests approval from the manager(s) and owner of the knowledge base before retiring.

---

## Next steps

- Review [Server-Side Scripting](server-side-scripting.md) for the Business Rules and Script Includes that Flow Designer can call.
- Review [Glide APIs](glide-apis.md) for the server-side classes used throughout.
