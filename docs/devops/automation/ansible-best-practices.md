# Ansible Best Practices

These practices are based on the same Ansible learning repository used for [Ansible Automation Notes](ansible_automation.md). The source contains useful lab exercises, but it also shows several patterns that should not be copied into production. For fundamentals and command examples, see the [Ansible Guide](../ansible-guide.md).

## 1. Sanitize before publishing or sharing

Lab notes often contain real hostnames, public addresses, usernames, passwords, ticket records, and employee data. Remove or replace all of it before publishing notes, examples, screenshots, or repositories.

Replace sensitive values with obvious placeholders:

```text
web01.example.test
192.0.2.10
automation-user
<approved-secret-store-reference>
platform-team
```

Do not reproduce legacy credentials in documentation. If a credential was ever committed, revoke or rotate it and review access logs.

Add local and generated data to `.gitignore`:

```gitignore
.venv/
site/
*.log
*.pem
*.key
artifacts/
reports/
inventory.local
group_vars/*/vault.yml
```

Keep real inventories, vault files, private keys, generated reports, and service credentials out of public repositories.

## 2. Use a dedicated automation account

Avoid logging in as `root` and avoid sharing a personal SSH key. Create a dedicated automation account with only the privileges it needs.

```ini
[web]
web01.example.test
web02.example.test

[web:vars]
ansible_user=automation
ansible_ssh_private_key_file=~/.ssh/id_ed25519
```

- Keep host-key checking enabled for real systems.
- Use `become: true` only for tasks that need privilege escalation.
- Put group-level values in `group_vars/` and host-specific values in `host_vars/`.
- Keep inventory paths relative to the project where possible.
- Use a dynamic inventory plugin or an approved source of truth for large environments.

The practice repository used `host_key_checking = false` and a root-owned private key. Those settings are acceptable only in a disposable lab and should be removed before any shared use.

## 3. Protect secrets

Never put passwords, access keys, tokens, or private keys directly in playbooks, `vars/main.yml`, inventories, or command-line arguments.

Use one of these instead:

- Ansible Vault for encrypted variables.
- An approved external secret manager.
- AWX/AAP credentials.
- Environment variables injected by a controlled runner.
- Cloud workload identity or IAM roles.

```yaml
vars:
  snow_user: "{{ lookup('env', 'SN_USERNAME') }}"
```

Do not log the secret value. Redact sensitive output, and remember that `debug`, failed task output, and playbook artifacts can still expose values. Use `no_log: true` for tasks that handle secrets.

```yaml
- name: Update an API token
  ansible.builtin.uri:
    url: "https://api.example.test/token"
    method: POST
    body_format: json
    body:
      token: "{{ api_token }}"
  no_log: true
```

## 4. Prefer modules over shell commands

Modules are usually idempotent, validate inputs, and return structured results. Use `shell` or `command` only when no module covers the operation.

| Avoid | Prefer |
| --- | --- |
| `shell: yum install -y httpd` | `ansible.builtin.package` or `ansible.builtin.dnf` |
| `shell: systemctl restart httpd` | `ansible.builtin.service` or `ansible.builtin.systemd_service` |
| `shell: useradd automation` | `ansible.builtin.user` |
| `shell: mkdir /srv/app` | `ansible.builtin.file` with `state: directory` |
| `shell: cp file /etc/app/` | `ansible.builtin.copy` or `ansible.builtin.template` |
| `shell: df -h` | `ansible.builtin.setup` facts or a read-only command with `changed_when: false` |

Use FQCNs so the module source is explicit:

```yaml
- name: Install a package
  ansible.builtin.package:
    name: httpd
    state: present
```

Avoid `state: latest` unless you intentionally want every run to change the system. Pin versions or use `state: present` for repeatable builds.

## 5. Make playbooks idempotent

A second run with no intended change should report no changes. Use module state, avoid unconditional `shell` mutations, and mark read-only commands correctly.

```yaml
- name: Read the process table
  ansible.builtin.command:
    cmd: "ps -eo pid,comm,%cpu,%mem --sort=-%cpu"
  register: process_table
  changed_when: false
```

Avoid tasks that append the same line on every run, create duplicate records, or rewrite files with timestamps unless that behavior is required.

## 6. Write clear playbooks

- Give every play and task a meaningful `name`.
- Keep one play focused on one outcome.
- Use `become` only where needed.
- Use handlers for restarting services after a change.
- Use tags for optional or destructive sections.
- Use variables for paths, package names, ports, and record identifiers.
- Use `gather_facts: false` only when the play does not use facts.
- Use `serial` when a rolling change is required.
- Use `any_errors_fatal` when a failure should stop the whole play.

```yaml
---
- name: Configure the web tier
  hosts: web
  become: true
  serial: "25%"
  tasks:
    - name: Install the web package
      ansible.builtin.package:
        name: "{{ web_package }}"
        state: present
      notify: Restart web service

  handlers:
    - name: Restart web service
      ansible.builtin.service:
        name: "{{ web_service }}"
        state: restarted
```

## 7. Handle failures deliberately

`ignore_errors: true` hides failures and makes later output misleading. Prefer `failed_when`, `changed_when`, `block`/`rescue`, and explicit assertions.

```yaml
- name: Validate required variables
  ansible.builtin.assert:
    that:
      - app_name is defined
      - app_name | length > 0
      - target_environment in ['dev', 'test', 'prod']
    fail_msg: "Missing or invalid deployment variables."
```

Use `block` and `rescue` for multi-step operations that need cleanup or a fallback. Use `always` for cleanup that must run regardless of the result.

## 8. Structure roles carefully

```text
roles/
└── web_baseline/
    ├── defaults/main.yml
    ├── files/
    ├── handlers/main.yml
    ├── meta/main.yml
    ├── tasks/main.yml
    ├── templates/
    ├── tests/
    └── vars/main.yml
```

- Give roles descriptive names, not names like `roles` or `test-roles`.
- Put overrideable values in `defaults/main.yml`.
- Reserve `vars/main.yml` for values that should not be casually overridden.
- Document required inputs and supported platforms in `meta/main.yml` and the role README.
- Add role tests with a disposable inventory.
- Use `import_role` for static composition and `include_role` when the role must be conditional or dynamic.
- Keep handlers idempotent and narrowly scoped.

## 9. Validate and test before execution

At a minimum:

```bash
ansible-playbook -i inventory.ini playbook.yml --syntax-check
ansible-playbook -i inventory.ini playbook.yml --check --diff
ansible-lint playbook.yml
```

Check mode is not a guaranteed dry run for every module. Some modules still make changes or cannot predict their result. Review modules that manage cloud resources, records, keys, and external APIs especially carefully.

Use a disposable lab, test data, and a non-production account. Verify the real target state after execution rather than trusting a task's success message alone.

## 10. Cloud automation practices

The AWS VPC example demonstrates the building blocks, but production use requires stronger controls.

- Use IAM roles, workload identity, or temporary credentials. Do not store access keys in `vars/main.yml`.
- Use `amazon.aws` collection modules and pin collection versions.
- Restrict security-group ingress to approved networks. Do not expose SSH to `0.0.0.0/0`.
- Prefer AWS Systems Manager Session Manager over open SSH where possible.
- Do not write generated private keys to a shared or unencrypted directory.
- Tag every resource with owner, environment, purpose, and cost center.
- Pin AMIs and instance types, and confirm region and account before every run.
- Add a cleanup or destroy playbook for every learning resource.
- Review plans and use a sandbox account for experiments.

For state-changing cloud resources, use an approval step in AWX/AAP or require an explicit extra variable before apply or destroy.

## 11. ServiceNow and ITSM automation

- Test against a non-production ServiceNow instance first.
- Query existing records before creating or updating them.
- Use environment variables, credentials, or a secret store for `SN_HOST`, `SN_USERNAME`, and `SN_PASSWORD`.
- Confirm the exact table, class, field names, and allowed state values for your instance.
- Avoid hard-coded numeric state codes unless the collection version and instance require them.
- Treat `state: absent` and record-closing tasks as destructive operations.
- Separate record creation, update, attachment, and cleanup playbooks.
- Add output that reports the created or updated record number without exposing sensitive fields.
- Review CMDB naming and duplicate-detection rules before running bulk updates.
- Keep playbook artifacts and logs free of passwords and personal data.

## 12. AWX and Ansible Automation Platform

- Store credentials in AWX/AAP, not in project files.
- Use execution environments to pin Ansible, collections, and Python dependencies.
- Apply least-privilege RBAC to projects, inventories, credentials, and job templates.
- Use job templates for a single repeatable unit of work and workflows for multi-step processes.
- Require approval for destructive jobs.
- Enable logging and retention appropriate to the environment.
- Keep inventories and execution environments under version control; keep secrets out.
- Test job templates against a lab inventory before production use.

## 13. Version control and CI

- Commit playbooks, roles, templates, and documentation.
- Do not commit vault passwords, private keys, reports with personal data, or generated artifacts.
- Run YAML lint, `ansible-lint`, syntax checks, and role tests in CI.
- Pin collection and execution-environment versions.
- Review changes to inventories, credentials, and destructive tasks carefully.
- Keep a changelog or learning record for significant automation changes.

## 14. Common issues found in the practice code

| Observed pattern | Risk | Better approach |
| --- | --- | --- |
| Credentials and access keys in `vars/main.yml` | Secret exposure | Vault, environment, IAM role, or AWX credential |
| `host_key_checking = false` | Man-in-the-middle risk | Enable host-key checking for real systems |
| Shared root SSH key | Excess privilege and weak accountability | Dedicated automation user and key |
| Public IPs and passwords in text notes | Credential and infrastructure exposure | Remove and rotate; use placeholders in notes |
| Personal names and payroll-like CSV data | Privacy exposure | Use synthetic, non-personal sample data |
| `shell` used for `df`, `top`, and `ps` | Poor idempotency and parsing | Facts or read-only commands with `changed_when: false` |
| `ignore_errors: true` | Hidden failures | `failed_when`, `block`/`rescue`, assertions |
| `gather_facts: false` while using facts | Undefined variables | Enable fact gathering or define the values explicitly |
| Service task with no `hosts` or malformed indentation | Syntax or scope failure | Validate with `--syntax-check` and use clear play structure |
| `state: latest` for packages | Unpredictable changes | `state: present` with a pinned version |
| Hard-coded `/root/...` paths | Fragile and privilege-heavy | Variables and project-relative paths |
| CSV delimiter mismatch | Empty or incorrect parsed data | Match the delimiter to the file and validate columns |
| Role directory named `roles` | Confusing imports | Descriptive role name such as `web_baseline` |
| AWS security group open to `0.0.0.0/0` on SSH | Unrestricted management access | Restrict to approved networks or use Session Manager |
| Hard-coded AMI and instance type | Account or region mismatch | Variables with validation and documented defaults |
| Key pair written to a local directory | Key leakage | Approved key management or Session Manager |
| Numeric ITSM state codes | Fragile across versions/instances | Confirm field values and use documented states |
| Destructive cleanup without approval | Accidental data or record loss | Tags, extra-variable gate, or AWX approval |
| Generated reports and artifacts in the repo | Data leakage | Write to a gitignored directory and review retention |

## 15. Final checklist

- [ ] No secrets, private keys, public IPs, or real personal data in the repository.
- [ ] Inventory targets a safe lab and uses a dedicated automation account.
- [ ] Playbooks pass `--syntax-check` and `ansible-lint`.
- [ ] Read-only discovery runs before any change.
- [ ] Check mode and diff are reviewed where supported.
- [ ] Destructive actions require explicit approval or an extra variable.
- [ ] Tasks are idempotent and use modules where possible.
- [ ] Roles have descriptive names, defaults, tests, and documentation.
- [ ] Cloud resources have tags, restricted access, and a cleanup path.
- [ ] ITSM operations are tested against a non-production instance.
- [ ] Outputs and logs do not expose secrets or sensitive records.
- [ ] The final target state is verified independently of task output.

## Further reading

- [Ansible best practices](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_best_practices.html)
- [Ansible Vault](https://docs.ansible.com/ansible/latest/vault_guide/)
- [Ansible lint](https://ansible.readthedocs.io/projects/lint/)
- [Ansible Automation Platform documentation](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/)
