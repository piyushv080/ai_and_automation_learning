# DevOps Engineering

DevOps engineering connects software development and operations through shared ownership, automation, fast feedback, and reliable delivery. Tools help, but clear processes and measurable outcomes matter just as much.

## Main areas

1. **Source control:** branches, commits, reviews, and versioned automation.
2. **Continuous integration:** build, lint, test, and scan changes automatically.
3. **Continuous delivery:** package and promote tested changes through environments with appropriate approvals.
4. **Infrastructure as code:** review and reproduce infrastructure changes.
5. **Containers and orchestration:** package applications consistently and manage their lifecycle.
6. **Observability and reliability:** use metrics, logs, traces, service indicators, and runbooks to understand service health.
7. **Security:** include dependency, code, and configuration checks in the delivery path.

## Suggested progression

- Start with [Bash and shell](../scripting/bash.md), [Python](../python-basics.md), Git, and [Linux](../linux-notes.md).
- Add [networking](../networking-notes.md), containers, and cloud foundations.
- Create a CI pipeline that runs formatting, static checks, tests, and dependency scanning.
- Deploy through an approved automation workflow and verify the service after deployment.
- Add dashboards, alerts, a rollback plan, and a runbook.

## Existing site topics

- [Automation technologies](../automation/index.md)
- [Security and observability](../security-observability.md)
- [Project catalog](../projects/index.md)
- [Runbook template](../documentation/runbook-template.md)

## Practice project

Choose a small application or script. Store it in Git, add a pipeline for linting and tests, package it reproducibly, deploy it to a safe test environment, and document verification and rollback steps.
