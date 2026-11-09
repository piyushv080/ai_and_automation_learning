# Ansible Guide

Ansible is an open-source automation engine for configuration management, application deployment, service orchestration, cloud provisioning, and other repeatable IT work. It uses human-readable YAML playbooks and connects to managed hosts without installing a persistent Ansible agent on them.

## What Ansible does

Ansible can:

- Install and configure software.
- Start, stop, and manage services.
- Copy files and render templates.
- Provision cloud infrastructure.
- Run one-off operational checks.
- Coordinate multi-tier deployments.
- Integrate with external systems through APIs.

Ansible is designed for multi-tier environments. Instead of managing one host at a time with separate scripts, you describe the desired state for groups of hosts and let Ansible apply it.

## Agentless architecture

Ansible normally connects to managed nodes over SSH. It copies small programs called **modules** to the target, executes them, and removes the temporary module files. This means:

- No Ansible daemon is required on managed nodes.
- No permanent agent or extra firewall port is required.
- The control node needs Ansible; managed nodes generally need a supported Python interpreter and a connection method.

Ansible can also use other connection plugins, but SSH is the default.

## How Ansible works

| Component | Role |
| --- | --- |
| Control node | The machine where Ansible is installed and playbooks are run. |
| Managed node | A target machine configured by Ansible. |
| Inventory | A file listing hosts and groups. |
| Module | A reusable unit of work, such as installing a package or managing a service. |
| Task | A call to a module with arguments. |
| Play | A mapping of hosts to tasks. |
| Playbook | A YAML file containing one or more plays. |
| Role | A reusable collection of tasks, variables, files, templates, and handlers. |
| `ansible.cfg` | Configuration for Ansible behavior, inventory, privileges, and plugins. |

A typical run:

```text
Control node -> inventory -> SSH connection -> module copied/executed -> result returned
```

Ansible usually reports `ok`, `changed`, `failed`, `skipped`, or `unreachable` for each task.

## Configuration management

Configuration management means maintaining a reliable record of system state and applying changes consistently. That includes package versions, service configuration, users, permissions, network settings, and files.

For example, installing the same application version on many servers manually is slow and error-prone. With Ansible:

1. List the target hosts in an inventory.
2. Write a playbook that installs and configures the application.
3. Run the playbook from the control node.
4. Review the result and verify the actual service state.

Ansible playbooks should be **idempotent**: running the same playbook twice should not make unintended changes on the second run.

## Control node and managed node requirements

- Install Ansible on a Linux or Unix-like control node. Native Windows control nodes are not supported; use WSL, a Linux VM, or a container if your workstation is Windows.
- Use a currently supported `ansible-core` release. Do not follow old Python 2.6/2.7 examples; those versions are obsolete.
- Managed nodes usually need a supported Python interpreter and SSH access.
- Use a dedicated automation account instead of sharing a personal account or logging in as `root` directly.
- Keep host-key checking enabled for real systems.

## Install Ansible

Use the package manager or an isolated Python environment. Examples:

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install -y ansible

# RHEL family
sudo dnf install -y ansible

# Python virtual environment
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install ansible
```

Verify the installation:

```bash
ansible --version
ansible-playbook --version
```

For a lab, create a dedicated user and configure SSH trust between the control node and managed nodes:

```bash
ssh-keygen -t ed25519 -C "automation@example.test"
ssh-copy-id automation@192.0.2.10
ssh automation@192.0.2.10
```

Test connectivity:

```bash
ansible all -i inventory.ini -m ansible.builtin.ping
```

## Inventory

An inventory lists managed hosts and groups. A small INI inventory:

```ini
[web]
web01.example.test
web02.example.test

[db]
db01.example.test

[web:vars]
ansible_user=automation
ansible_ssh_private_key_file=~/.ssh/id_ed25519
```

A YAML inventory can represent the same structure:

```yaml
all:
  children:
    web:
      hosts:
        web01.example.test:
        web02.example.test:
      vars:
        ansible_user: automation
    db:
      hosts:
        db01.example.test:
```

Inspect inventory targets:

```bash
ansible all -i inventory.ini --list-hosts
ansible-inventory -i inventory.ini --graph
ansible-inventory -i inventory.ini --host web01.example.test
```

Keep real inventories out of public repositories if they contain internal hostnames, addresses, or credentials. Use `group_vars/` and `host_vars/` for structured variables.

An example `ansible.cfg`:

```ini
[defaults]
inventory = ./inventory.ini
remote_user = automation
host_key_checking = True
interpreter_python = auto_silent
callbacks_enabled = profile_tasks
```

Older material uses `callback_whitelist`; current Ansible uses `callbacks_enabled`.

## YAML basics

Ansible uses YAML because it is readable and well suited to configuration data. Important rules:

- Use spaces, not tabs, for indentation.
- Put a space after `:` in a mapping.
- Start list items with `- `.
- Quote ambiguous values such as version strings and values beginning with special characters.
- Validate files before execution.

### Key-value mappings

```yaml
---
student:
  name: james john
  roll_no: 34
  division: B
  active: true
```

Abbreviated mapping:

```yaml
student: {name: james john, roll_no: 34, division: B, active: true}
```

### Lists

```yaml
---
countries:
  - America
  - China
  - Canada
  - Iceland
```

Abbreviated list:

```yaml
countries: [America, China, Canada, Iceland]
```

### Lists inside mappings

```yaml
---
student:
  name: james john
  likes:
    - maths
    - physics
    - English
```

### List of mappings

```yaml
---
- name: james john
  roll_no: 34
  likes:
    - maths
    - physics
- name: robert richardson
  roll_no: 53
  likes:
    - biology
    - chemistry
```

### Multiline strings and booleans

`|` preserves line breaks. `>` folds newlines into spaces.

```yaml
---
result:
  passed: true
  message_preserve_lines: |
    Congratulations.
    You passed with 79%.
  message_fold_lines: >
    Congratulations.
    You passed with 79%.
```

Booleans are case-insensitive in YAML, but lowercase `true` and `false` are the clearest choice.

## Ad-hoc commands

Ad-hoc commands are for quick, one-off operations. They are not a replacement for repeatable configuration management and deployment playbooks.

General form:

```bash
ansible <pattern> -i <inventory> -m <module> -a "<arguments>" [options]
```

Test connectivity:

```bash
ansible all -i inventory.ini -m ansible.builtin.ping
```

Run a read-only command:

```bash
ansible web -i inventory.ini -m ansible.builtin.command -a "uptime"
```

Gather facts:

```bash
ansible all -i inventory.ini -m ansible.builtin.setup
ansible all -i inventory.ini -m ansible.builtin.setup -a "filter=ansible_os_family"
```

### Parallelism and privilege escalation

```bash
ssh-agent bash
ssh-add ~/.ssh/id_ed25519

ansible web -i inventory.ini -a "/sbin/reboot" -f 12 --become -u automation
```

`-f 12` sets the number of parallel forks. `--become` enables privilege escalation. Use reboot modules and maintenance procedures carefully; a raw reboot can interrupt the connection.

### Copy files and manage directories

```bash
ansible web -i inventory.ini -m ansible.builtin.copy \
  -a "src=/etc/sample/app.conf dest=/tmp/app.conf mode=0644"

ansible web -i inventory.ini -m ansible.builtin.file \
  -a "path=/srv/app state=directory mode=0755 owner=automation group=automation"

ansible web -i inventory.ini -m ansible.builtin.file \
  -a "path=/srv/app state=absent"
```

### Manage packages

```bash
ansible web -i inventory.ini -m ansible.builtin.package \
  -a "name=nginx state=present" --become

ansible web -i inventory.ini -m ansible.builtin.dnf \
  -a "name=nginx state=latest" --become

ansible debian -i inventory.ini -m ansible.builtin.apt \
  -a "name=nginx state=present update_cache=true" --become
```

Prefer `state: present` with a pinned version for repeatable systems. `state: latest` intentionally changes packages whenever a newer version is available.

## Playbooks

A playbook is a YAML file containing one or more plays. Each play selects hosts and runs tasks.

```yaml
---
- name: Install and configure the sample application
  hosts: web
  become: true
  vars:
    app_port: 8080
  tasks:
    - name: Install the application package
      ansible.builtin.package:
        name: sample-app
        state: present

    - name: Enable and start the application service
      ansible.builtin.service:
        name: sample-app
        state: started
        enabled: true

    - name: Deploy the application configuration
      ansible.builtin.template:
        src: templates/app.conf.j2
        dest: /etc/sample/app.conf
        mode: "0644"
      notify: Restart sample application

  handlers:
    - name: Restart sample application
      ansible.builtin.service:
        name: sample-app
        state: restarted
```

Playbook tags:

- `name` documents the play or task.
- `hosts` selects an inventory group or host pattern.
- `become` enables privilege escalation.
- `vars` defines play variables.
- `tasks` lists actions.
- `handlers` run when notified by a changed task.

Validate and run:

```bash
ansible-playbook -i inventory.ini site.yml --syntax-check
ansible-playbook -i inventory.ini site.yml --check --diff
ansible-playbook -i inventory.ini site.yml
```

Check mode is useful but not a guaranteed dry run for every module. Review modules that manage cloud resources, external APIs, or destructive operations carefully.

## Variables and registered results

Variables make playbooks reusable:

```yaml
---
- name: Report application settings
  hosts: web
  vars:
    app_port: 8080
  tasks:
    - name: Show the configured port
      ansible.builtin.debug:
        msg: "The application listens on port {{ app_port }}"
```

Register output from a task:

```yaml
---
- name: Check application status
  hosts: web
  tasks:
    - name: Read the service status
      ansible.builtin.command:
        cmd: systemctl is-active sample-app
      register: service_status
      changed_when: false
      failed_when: false

    - name: Show the result
      ansible.builtin.debug:
        msg: "Service state: {{ service_status.stdout }}"
```

Useful result properties include `changed`, `stdout`, `stderr`, `rc`, and `stdout_lines`. Use `var` when you want to inspect the whole registered object:

```yaml
- name: Inspect the registered result
  ansible.builtin.debug:
    var: service_status
```

Do not print secrets. Use `no_log: true` for tasks that handle sensitive values.

## Blocks, rescue, and always

`block`, `rescue`, and `always` provide structured error handling:

```yaml
---
- name: Run a checked operation
  hosts: web
  tasks:
    - name: Attempt the operation and recover from failure
      block:
        - name: Run the application check
          ansible.builtin.command:
            cmd: /usr/local/bin/sample-check
          register: check_result
          changed_when: false
      rescue:
        - name: Report the failure
          ansible.builtin.debug:
            msg: "The application check failed."
      always:
        - name: Record completion
          ansible.builtin.debug:
            msg: "This task always runs."
```

This is similar to `try`, `catch`, and `finally` in other languages:

- `block`: the main work.
- `rescue`: runs when a task in the block fails.
- `always`: runs regardless of success or failure.

Use explicit `failed_when` and `changed_when` instead of hiding errors with `ignore_errors`.

## Loops

Use `loop` for repeated tasks:

```yaml
---
- name: Install required packages
  hosts: web
  become: true
  vars:
    packages:
      - nginx
      - git
      - curl
  tasks:
    - name: Install each package
      ansible.builtin.package:
        name: "{{ item }}"
        state: present
      loop: "{{ packages }}"
```

Loop over command output:

```yaml
---
- name: Link application artifacts
  hosts: web
  vars:
    artifact_dir: /opt/sample-app/webapps
    target_dir: /srv/sample-app
  tasks:
    - name: Find application artifacts
      ansible.builtin.find:
        paths: "{{ artifact_dir }}"
        patterns: "*.war"
      register: artifacts

    - name: Create links for each artifact
      ansible.builtin.file:
        src: "{{ item }}"
        dest: "{{ target_dir }}/{{ item | basename }}"
        state: link
      loop: "{{ artifacts.files | map(attribute='path') | list }}"
```

Older examples use `with_items`; `loop` is the preferred modern syntax for most cases.

## Conditionals

Use `when` to run a task only when a condition is true:

```yaml
---
- name: Configure the production environment
  hosts: web
  vars:
    environment_name: production
  tasks:
    - name: Show the production message
      ansible.builtin.debug:
        msg: "Production configuration selected."
      when: environment_name == "production"
```

Conditions can combine expressions:

```yaml
when:
  - ansible_facts['os_family'] == "RedHat"
  - app_port | int > 1024
```

Use `and`, `or`, and parentheses carefully. Prefer a list of conditions when every condition must be true.

## Roles

Roles break playbooks into reusable components. A role can contain tasks, defaults, variables, files, templates, handlers, tests, and metadata.

Role structure:

```text
roles/
└── sample_app/
    ├── defaults/main.yml
    ├── files/
    ├── handlers/main.yml
    ├── meta/main.yml
    ├── tasks/main.yml
    ├── templates/
    ├── tests/
    │   ├── inventory
    │   └── test.yml
    └── vars/main.yml
```

Create a role:

```bash
ansible-galaxy role init --offline sample_app
```

Older notes use `ansible-galaxy init`; `ansible-galaxy role init` is clearer. The `--offline` option avoids depending on Galaxy connectivity when the local scaffold is all you need.

Example `tasks/main.yml`:

```yaml
---
- name: Install the sample application package
  ansible.builtin.package:
    name: sample-app
    state: present
  register: install_result

- name: Report whether the package changed
  ansible.builtin.debug:
    msg: "Package changed: {{ install_result.changed }}"
```

Use roles in a playbook:

```yaml
---
- name: Deploy the sample application
  hosts: web
  become: true
  roles:
    - role: sample_app_install
      tags: [install]
    - role: sample_app_start
      tags: [start]
```

Roles are not standalone playbooks. They are applied by plays that select the target hosts. Use `defaults/main.yml` for values callers may override, and `vars/main.yml` for values that should not be casually overridden.

Install external collections and roles with `ansible-galaxy` when needed:

```bash
ansible-galaxy collection install community.general
ansible-galaxy role install geerlingguy.nginx
```

Pin versions in a requirements file for reproducible automation.

## Limit execution with tags and hosts

Tags allow selected tasks or roles to run without executing the entire playbook:

```yaml
roles:
  - role: sample_app_install
    tags: [install]
  - role: sample_app_start
    tags: [start]
```

List and run tags:

```bash
ansible-playbook -i inventory.ini site.yml --list-tags
ansible-playbook -i inventory.ini site.yml --tags install
ansible-playbook -i inventory.ini site.yml --skip-tags start
```

Tags are case-sensitive. Use names that are stable and easy to understand.

Limit execution to hosts:

```bash
ansible-playbook -i inventory.ini site.yml --limit web01.example.test
ansible-playbook -i inventory.ini site.yml --limit web
```

Use a parameterized play when the target must be supplied at runtime:

```yaml
---
- name: Run operations against a selected target
  hosts: "{{ target | default('web') }}"
  tasks:
    - name: Show the target host
      ansible.builtin.debug:
        var: inventory_hostname
```

Run it with an extra variable:

```bash
ansible-playbook -i inventory.ini site.yml -e "target=web"
```

Extra variables are visible in process listings and shell history. Do not pass passwords or tokens with `-e` on a shared system.

## Troubleshooting

Increase verbosity when you need more detail:

```bash
ansible-playbook -i inventory.ini site.yml -v
ansible-playbook -i inventory.ini site.yml -vv
ansible-playbook -i inventory.ini site.yml -vvv
ansible-playbook -i inventory.ini site.yml -vvvv
```

Higher levels can expose connection details and sensitive values. Treat verbose logs as sensitive.

Useful checks:

```bash
ansible-playbook -i inventory.ini site.yml --syntax-check
ansible-playbook -i inventory.ini site.yml --list-hosts
ansible-playbook -i inventory.ini site.yml --list-tasks
ansible-inventory -i inventory.ini --graph
ansible-doc ansible.builtin.service
ansible-lint site.yml
```

Common problems:

| Problem | Likely cause | Fix |
| --- | --- | --- |
| `unreachable` host | SSH, DNS, firewall, or credentials | Test with `ssh` and `ansible -m ping`. |
| `Permission denied` | Wrong user, key, or missing `become` | Confirm `ansible_user`, key path, and privilege needs. |
| Undefined variable | Fact gathering disabled, wrong scope, or typo | Check variable source and `gather_facts`. |
| YAML syntax error | Tabs, bad indentation, or missing space after `:` | Use spaces and a YAML-aware editor. |
| Value starting with `{{` fails | YAML/types or quoting issue | Quote the whole value: `"{{ app.name }}/demo/"`. |
| Module not found | Missing collection or wrong name | Install the collection or use the correct FQCN. |
| Python interpreter error | Managed node lacks a supported Python | Install Python or set `ansible_python_interpreter`. |
| Task reports changed every run | Shell command or non-idempotent task | Use a module or set `changed_when` correctly. |

YAML does not allow tab-based indentation. Use spaces consistently. Avoid validating Ansible playbooks with generic JSON/OpenAPI editors; use `ansible-playbook --syntax-check` and `ansible-lint`.

## Legacy source notes

The original training material is useful conceptually but contains outdated assumptions:

- Python 2.6/2.7 is no longer supported by current Ansible.
- `yum` examples should generally be replaced with `ansible.builtin.package`, `dnf`, or `apt`.
- `callback_whitelist` is now `callbacks_enabled`.
- `with_items` is still seen in older playbooks; prefer `loop`.
- `ansible-galaxy init` is clearer as `ansible-galaxy role init`.
- `state: latest` can cause unexpected changes; pin versions where repeatability matters.
- Native Windows control nodes are not supported; use WSL, Linux, or a container.
- Old sample names, paths, addresses, and credentials must not be copied into new environments.

## Best practices

- Use a dedicated automation account and least-privilege access.
- Keep host-key checking enabled outside disposable labs.
- Prefer modules over `shell` and `command`.
- Make tasks idempotent and set `changed_when` or `failed_when` deliberately.
- Use `no_log: true` for secrets and avoid printing sensitive values.
- Store secrets in Ansible Vault, AWX/AAP credentials, or an approved secret manager.
- Validate with `--syntax-check`, `--check --diff`, and `ansible-lint`.
- Use roles and collections for reuse; pin their versions.
- Tag destructive operations and require approval where appropriate.
- Add rollback, verification, and cleanup steps.
- Test in a disposable lab before production.

See [Ansible Best Practices](automation/ansible-best-practices.md) for a deeper production checklist.

## Quick reference

| Task | Command |
| --- | --- |
| Test connectivity | `ansible all -i inventory.ini -m ansible.builtin.ping` |
| List hosts | `ansible all -i inventory.ini --list-hosts` |
| Show inventory graph | `ansible-inventory -i inventory.ini --graph` |
| Gather facts | `ansible all -i inventory.ini -m ansible.builtin.setup` |
| Run a command | `ansible web -i inventory.ini -a "uptime"` |
| Install a package | `ansible web -i inventory.ini -m ansible.builtin.package -a "name=nginx state=present" --become` |
| Syntax check | `ansible-playbook -i inventory.ini site.yml --syntax-check` |
| Dry run with diff | `ansible-playbook -i inventory.ini site.yml --check --diff` |
| Run a playbook | `ansible-playbook -i inventory.ini site.yml` |
| Run selected tags | `ansible-playbook -i inventory.ini site.yml --tags install` |
| Limit hosts | `ansible-playbook -i inventory.ini site.yml --limit web01.example.test` |
| List tasks | `ansible-playbook -i inventory.ini site.yml --list-tasks` |
| Lint | `ansible-lint site.yml` |
| Create a role | `ansible-galaxy role init --offline sample_app` |
| Show module docs | `ansible-doc ansible.builtin.service` |

## Further reading

- [Ansible documentation](https://docs.ansible.com/)
- [Ansible playbook guide](https://docs.ansible.com/ansible/latest/playbook_guide/)
- [Ansible collections index](https://docs.ansible.com/ansible/latest/collections/index.html)
- [Ansible Galaxy](https://galaxy.ansible.com/)
- [Ansible lint](https://ansible.readthedocs.io/projects/lint/)
- [Ansible Automation Platform documentation](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/)
