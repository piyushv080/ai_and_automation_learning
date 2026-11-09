# Ansible, AWX, and Automation Platform

Study notes for configuration management, reusable playbooks, AWX/AAP job execution, troubleshooting, and secure infrastructure workflows.

## Learning objective

Understand how Ansible components work together. For each concept, be ready to explain its purpose, show a small example, describe failure handling, and identify security considerations.

## Ansible architecture

- **Control node:** the environment where Ansible commands or automation jobs run.
- **Managed node:** a system Ansible configures or queries.
- **Inventory:** hosts and groups that Ansible can target, optionally with variables.
- **Module:** a unit of work, such as managing a package, file, or service.
- **Playbook:** YAML automation describing one or more plays and their tasks.
- **Role:** a reusable, organized collection of tasks, handlers, defaults, templates, and files.
- **Facts:** information gathered about managed nodes.
- **Handler:** a task triggered by a notification, commonly after a configuration change.

YAML is a data serialization format. An Ansible playbook is a YAML document that follows Ansible's playbook structure and uses Ansible keywords and modules.

## Inventory and playbooks

An inventory groups target hosts. Avoid committing secrets in inventory files; use approved credential management.

```ini
[web]
web01.example.test
web02.example.test

[web:vars]
http_port=8080
```

Example playbook to ensure an existing service is enabled and running. Review the inventory and target before executing on real systems.

```yaml
---
- name: Ensure the web service is running
  hosts: web
  become: true
  tasks:
    - name: Ensure nginx is enabled and started
      ansible.builtin.service:
        name: nginx
        enabled: true
        state: started
```

Useful playbook elements include:

- `hosts`: target inventory pattern.
- `tasks`: ordered operations.
- `vars`: configurable values.
- `when`: condition for a task.
- `loop`: apply a task to multiple values.
- `register`: save a task result for later use.
- `notify` and `handlers`: run follow-up actions when a task changes something.

## Idempotency and reliability

An idempotent task brings a system to a desired state and generally makes no additional change on later runs. Prefer purpose-built modules, validate inputs, use clear variables, handle expected failures, choose sensible timeouts, and verify the final state.

Use `ansible.builtin.command` when executing a command without shell features. Use `ansible.builtin.shell` only when shell parsing (such as pipes or redirection) is required; avoid interpolating untrusted input into shell commands.

### Variables, conditions, loops, and results

```yaml
vars:
  app_directories:
    - /opt/demo/app1
    - /opt/demo/app2

tasks:
  - name: Create application directories
    ansible.builtin.file:
      path: "{{ item }}"
      state: directory
      mode: "0750"
    loop: "{{ app_directories }}"

  - name: Gather service facts
    ansible.builtin.service_facts:

  - name: Display a diagnostic message
    ansible.builtin.debug:
      msg: "Service facts were collected"
    when: ansible_facts.services is defined
```

Variable precedence determines which value wins when a variable is defined in multiple places. Keep configuration predictable and avoid using precedence as a substitute for clear design.

### Handlers and execution controls

Handlers run when notified, typically once at the end of a play if a notifying task reports a change. They are useful for restarting a service only when its configuration changes. Check mode (`--check`) predicts changes for supported tasks; not every module fully supports check mode, so it is not proof that a real run will succeed. Tags select tasks, but should not bypass required safety checks.

### Error handling

Ansible offers `failed_when`, `changed_when`, `block`, `rescue`, and `always`, along with registered task results and conditions. Use these to handle expected outcomes while preserving genuine failures. Do not suppress errors just to produce a successful job status.

## Modules and roles

Common module families include:

- Packages: `ansible.builtin.package`, or distribution-specific modules such as `apt` and `dnf`.
- Files: `ansible.builtin.file`, `copy`, `template`, and `lineinfile`.
- Services: `ansible.builtin.service` and `systemd_service`.
- Diagnostics: `ansible.builtin.debug`, `setup`, and `service_facts`.

Prefer modules over ad-hoc shell commands because modules can express desired state and report whether a change occurred.

A role typically contains `tasks/`, `handlers/`, `defaults/`, `vars/`, `templates/`, and `files/`. Roles make repeated work easier to review and reuse.

## Ad-hoc commands and secrets

An ad-hoc command is a one-off Ansible operation, useful for simple checks or small tasks. Use an inventory that targets only the intended hosts and choose a suitable module. Avoid using broad inventories or privileged commands casually.

Use Ansible Vault or the automation platform's credential store and approved secret integrations. Do not commit secrets to source control or expose them in job output. Apply least privilege to accounts and credentials.

## AWX and Ansible Automation Platform

AWX is the upstream open-source automation web interface and API project. Ansible Automation Platform (AAP) is Red Hat's supported enterprise automation offering. They are related, but supported components and operational details depend on the product and version.

| AWX/AAP concept | Purpose |
| --- | --- |
| Project | Synchronizes automation content, commonly from source control. |
| Inventory | Defines the hosts and groups a job can target. |
| Credential | Provides protected authentication material to jobs. |
| Execution environment | Packages Ansible, collections, and Python dependencies for consistent job execution. |
| Job template | Connects a project, inventory, playbook, credentials, execution environment, and launch options. |
| RBAC | Assigns permissions so users can access or manage only the resources and actions they need. |

Restrict target inventories, job templates, launch-time variables, and credentials to authorized users and use cases.

## Integrations and troubleshooting

An external application can trigger a job through the supported AWX/AAP API:

1. Authenticate securely.
2. Validate the incoming request and required approvals.
3. Map it to an approved job template and permitted parameters.
4. Launch the job and record its job ID.
5. Track it until a terminal state or timeout.
6. Verify the target system independently.
7. Return an accurate result and useful audit evidence.

For ServiceNow, a workflow might be: catalog request → approval → integration → approved job template → Ansible execution → verification → request update. For event-driven remediation, filter duplicate/noisy alerts, authorize the action, run only safe remediation, verify recovery, and preserve an audit trail.

When a job fails, inspect the failing task and output, then check inventory selection, connectivity, credentials, permissions, dependencies, and execution-environment requirements. If the job reports success but the application is unavailable, perform an independent health check and report that verification failure accurately.

## Interview practice

For each answer, cover the definition, purpose, how it works, a practical example, failure handling, and security considerations. Practice explaining:

- Ansible inventory, playbooks, tasks, modules, roles, facts, and handlers.
- Idempotency and the difference between `command` and `shell`.
- Variables, conditions, loops, registered results, and error handling.
- Check mode, tags, and safe verification.
- AWX projects, inventories, credentials, job templates, execution environments, and RBAC.
- API-triggered jobs, ServiceNow integration, event-driven remediation, and independent health checks.
- Secret handling, least privilege, approvals, and safe test environments.

## Further reading

- [Ansible documentation](https://docs.ansible.com/)
- [Ansible playbooks](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html)
- [Ansible best practices](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_best_practices.html)
- [AWX documentation](https://ansible.readthedocs.io/projects/awx/en/latest/)
- [Red Hat Ansible Automation Platform documentation](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/)
