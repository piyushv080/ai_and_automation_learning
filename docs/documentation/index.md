# Documentation

Good documentation helps someone understand, operate, and safely change a system. Keep it close to the code or service it describes, use plain language, and review it when behavior changes.

## Documentation types

| Document | Purpose |
| --- | --- |
| README | Explain what a project does and how to get started. |
| Tutorial | Teach a learner to complete a task step by step. |
| How-to guide | Help a reader solve a specific problem. |
| Reference | Record commands, options, interfaces, and expected values. |
| Runbook | Guide an operator through a routine task or incident. |
| Architecture note | Explain important components, boundaries, and tradeoffs. |

## Writing checklist

- Identify the audience, purpose, and expected outcome.
- State prerequisites and supported versions.
- Show commands and expected results; explain variables that need changing.
- Separate safe read-only checks from commands that make changes.
- Document permissions, secrets handling, error recovery, and cleanup.
- Link to authoritative references and assign an owner where useful.
- Review links and instructions after a change.

## Templates

- [Project README template](../examples/README.md)
- [Runbook template](runbook-template.md)

## Existing learning notes

- [Linux administration](../linux-notes.md)
- [Networking](../networking-notes.md)
- [Python basics](../python-basics.md)
- [Ansible, AWX, and Automation Platform](../ansible-awx.md)
