# Project Ideas

Choose a project small enough to finish and document. Start with read-only behavior, use test data, and add write operations only after validation and safety controls are in place.

## Beginner projects

### 1. Server inventory report

Use Python to read server records from JSON, validate fields, group by environment, and write a summary report. Practice: collections, functions, files, JSON, and tests.

### 2. Linux health summary

Use Bash to report disk capacity, load, and a service's status. Practice: shell variables, exit codes, input validation, and logs. Keep the first version read-only.

### 3. Windows service report

Use PowerShell to collect service states and export a CSV for review. Practice: objects, pipelines, filtering, and error handling.

### 4. API status checker

Use Python or Node.js to call a test endpoint with timeouts and report HTTP status. Practice: REST APIs, JSON, errors, and secrets handling.

## Intermediate projects

### 5. Ansible baseline role

Create a role that manages a harmless test configuration file and verifies the result on disposable Linux hosts. Practice: roles, templates, handlers, idempotency, and check mode.

### 6. Cloud sandbox with Terraform

Deploy a minimal resource in a sandbox account, review the plan, add tags and budget notes, then destroy it. Practice: state, variables, outputs, and cost awareness.

### 7. CI pipeline for automation content

Create a pipeline that checks formatting, lints Python or Ansible, runs unit tests, and scans dependencies. Practice: source control, continuous integration, and feedback.

### 8. Observability dashboard and runbook

Build a dashboard from sample metrics and write a runbook that explains what to check when a service is unhealthy. Practice: SLIs, alerts, and operational documentation.

## Project completion checklist

- [ ] State the problem and intended outcome.
- [ ] List prerequisites, assumptions, and a safe test environment.
- [ ] Keep credentials out of code and logs.
- [ ] Add validation, error handling, and tests where appropriate.
- [ ] Include verification and cleanup or rollback steps.
- [ ] Explain the design and limitations in a [project README](../examples/README.md).
