# Ansible Automation Notes

Practical notes from a hands-on Ansible learning repository. The source folder covers YAML fundamentals, ad-hoc commands, playbooks, facts, variables, roles, AWS VPC provisioning, and ServiceNow ITSM integration.

Related pages:

- [Ansible Guide](../ansible-guide.md)
- [Ansible, AWX, and Automation Platform](ansible-awx.md)
- [Ansible AWX Setup on Ubuntu](install-awx-ansible.md)
- [Ansible Best Practices](ansible-best-practices.md)

## 1. Learning map

| Source area | Topic | What to practice |
| --- | --- | --- |
| `00.basic_yaml_language` | YAML syntax | Mappings, lists, booleans, objects, multiline strings |
| `01.basic_ansible_setup_on_lab` | Controller and managed nodes | SSH trust, inventory, ad-hoc commands |
| `02.basic_playbook_practice` | Playbooks and modules | Facts, variables, packages, services, files, conditionals |
| `03.roles_with_simple_ping` | Role structure | Role directories, `include_role`, role vars |
| `04.roles_csv_html` | Reporting | Read structured data and generate HTML output |
| `05.role_aws_vpc_role` | Cloud automation | VPC, subnet, internet gateway, route table, security group, EC2 |
| `06.snow_integration_ansible` | ITSM automation | Incidents, problems, changes, CMDB configuration items |

## 2. YAML essentials

Ansible playbooks are YAML documents. The most important rules are consistent indentation, correct list and mapping syntax, and quoted strings when a value could be interpreted as another type.

```yaml
---
application:
  name: sample-app
  enabled: true
  ports:
    - 8080
    - 8443
  owners:
    - platform-team
    - operations-team
  description: |
    Multi-line values keep their line breaks.
    This is useful for configuration files and scripts.
```

Use lowercase `true` and `false` for booleans. Quote values that look like versions, dates, or other ambiguous types, for example `version: "1.0"`. Validate YAML before running a playbook.

```bash
ansible-playbook playbook.yml --syntax-check
```

## 3. Inventory and controller configuration

A small lab can use a static inventory. Keep the inventory in source control only when it contains no secrets or sensitive infrastructure details.

```ini
[web]
web01.example.test
web02.example.test

[web:vars]
ansible_user=automation
ansible_ssh_private_key_file=~/.ssh/id_ed25519
```

Example `ansible.cfg` for a local project:

```ini
[defaults]
inventory = ./hosts
remote_user = automation
host_key_checking = True
interpreter_python = auto_silent
```

The practice repository used lab-only settings such as a shared root SSH key and disabled host-key checking. For real systems, use a dedicated automation account, a managed key, and host-key verification.

Test connectivity before changing anything:

```bash
ansible all -m ansible.builtin.ping
ansible web -m ansible.builtin.command -a "uptime"
```

Prefer fully qualified collection names (FQCN), such as `ansible.builtin.ping`, so the module source is explicit.

## 4. Ad-hoc commands

Ad-hoc commands are useful for discovery and one-off checks.

```bash
ansible all -m ansible.builtin.setup -a "filter=ansible_os_family"
ansible web -m ansible.builtin.command -a "df -h"
ansible web -m ansible.builtin.dnf -a "name=httpd state=latest" --become
ansible debian -m ansible.builtin.apt -a "name=nginx state=latest" --become
```

Use read-only commands first. When a module exists for the operation, prefer it over `shell` or `command` because modules are usually idempotent and provide structured results.

## 5. Playbook anatomy

A playbook contains one or more plays. Each play selects hosts, optionally enables privilege escalation, and runs tasks.

```yaml
---
- name: Configure a web server
  hosts: web
  become: true
  tasks:
    - name: Install the web server package
      ansible.builtin.package:
        name: httpd
        state: present

    - name: Enable and start the web service
      ansible.builtin.service:
        name: httpd
        state: started
        enabled: true

    - name: Publish a simple index page
      ansible.builtin.copy:
        content: "<h1>Managed by Ansible</h1>\n"
        dest: /var/www/html/index.html
        owner: root
        group: root
        mode: "0644"
```

Run a safe validation sequence:

```bash
ansible-playbook -i hosts deploy_web.yml --syntax-check
ansible-playbook -i hosts deploy_web.yml --check --diff
ansible-playbook -i hosts deploy_web.yml
```

Check mode is a useful review step, but not every module supports it perfectly. Always inspect the planned changes.

## 6. Facts and variables

Facts describe the managed host, such as its operating system, memory, interfaces, and mounts. Use facts instead of hard-coding host-specific values.

```yaml
---
- name: Report host capacity
  hosts: web
  tasks:
    - name: Show memory and operating system
      ansible.builtin.debug:
        msg:
          - "Host: {{ ansible_facts['nodename'] }}"
          - "OS family: {{ ansible_facts['os_family'] }}"
          - "Memory MB: {{ ansible_facts['memtotal_mb'] }}"
```

Variables can be defined in playbooks, inventories, role defaults, role vars, or group and host variable files. Use role defaults for values that callers are expected to override.

```yaml
vars:
  web_root: /var/www/html
  service_name: httpd
```

Custom facts can be installed under `/etc/ansible/facts.d` and read with `ansible_local`. This is useful for environment-specific metadata, but avoid storing secrets in facts because facts may be logged or displayed.

## 7. Conditionals, loops, and blocks

Use conditionals to control whether a task runs. Use loops for a set of similar items. Use blocks to group tasks and handle failures.

```yaml
---
- name: Check an application mount
  hosts: all
  gather_facts: false
  vars:
    mount_path: /srv/application
  tasks:
    - name: Check whether the mount responds
      ansible.builtin.command:
        cmd: "timeout 30 stat {{ mount_path }}"
      register: mount_check
      changed_when: false
      failed_when: false

    - name: Attempt to repair mounts when the check fails
      when: mount_check.rc != 0
      block:
        - name: Remount file systems
          ansible.builtin.command:
            cmd: "timeout 30 mount -a"
          register: mount_repair
          changed_when: true

        - name: Verify the mount again
          ansible.builtin.command:
            cmd: "timeout 30 stat {{ mount_path }}"
          register: mount_verify
          changed_when: false
          failed_when: mount_verify.rc != 0

      rescue:
        - name: Report the failed repair
          ansible.builtin.fail:
            msg: "Mount repair failed for {{ mount_path }}"
```

Prefer `failed_when` and `changed_when` over `ignore_errors`. They make the intended behavior explicit and keep task results meaningful.

## 8. Roles

Roles organize tasks, defaults, variables, handlers, templates, files, and metadata into a reusable structure.

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

A role can be called from a playbook:

```yaml
---
- name: Apply the web baseline
  hosts: web
  become: true
  roles:
    - web_baseline
```

Or included conditionally:

```yaml
- name: Include the role only when required
  ansible.builtin.include_role:
    name: web_baseline
  when: apply_baseline | bool
```

Use `defaults/main.yml` for sensible defaults and `vars/main.yml` for values that should not be overridden casually. Put reusable files in `files/`, Jinja2 templates in `templates/`, and service restart logic in handlers.

The practice repository contained a role directory literally named `roles`. That works as a lab exercise, but a descriptive role name such as `web_baseline` or `ping_check` is easier to maintain.

## 9. Reporting with CSV and HTML

The reporting example reads tabular data and renders an HTML view. Treat sample reports as examples only and never publish real employee, payroll, or customer records.

A safer, sanitized pattern is to keep data and presentation separate:

```yaml
---
- name: Render an inventory report
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    report_csv: ./data/servers.csv
    report_html: ./reports/servers.html
  tasks:
    - name: Read the server inventory
      community.general.read_csv:
        path: "{{ report_csv }}"
        key: name
      register: server_rows

    - name: Render the HTML report
      ansible.builtin.template:
        src: templates/server-report.html.j2
        dest: "{{ report_html }}"
        mode: "0644"
```

Example sanitized CSV:

```csv
name,environment,owner,status
web01,test,platform-team,healthy
web02,test,platform-team,healthy
```

If a helper script is required, pass file paths as arguments and avoid hard-coding `/root` paths. Validate the script's inputs and keep generated reports out of source control when they contain sensitive data.

## 10. AWS VPC provisioning

The AWS role creates a VPC, subnet, internet gateway, route table, security group, key pair, and EC2 instance. In current collections, prefer the `amazon.aws` modules and an IAM role or short-lived credentials instead of access keys in `vars/main.yml`.

```yaml
---
- name: Create a learning VPC
  hosts: localhost
  connection: local
  gather_facts: false
  collections:
    - amazon.aws
  vars:
    aws_region: ap-south-1
    vpc_name: learning-vpc
    vpc_cidr: 10.10.0.0/24
    subnet_cidr: 10.10.0.0/26
  tasks:
    - name: Create the VPC
      amazon.aws.ec2_vpc_net:
        name: "{{ vpc_name }}"
        cidr_block: "{{ vpc_cidr }}"
        region: "{{ aws_region }}"
        state: present
        tags:
          Environment: learning
          Owner: platform-team
      register: vpc

    - name: Create a subnet
      amazon.aws.ec2_vpc_subnet:
        vpc_id: "{{ vpc.vpc.id }}"
        cidr: "{{ subnet_cidr }}"
        region: "{{ aws_region }}"
        state: present
        tags:
          Name: "{{ vpc_name }}-subnet"
      register: subnet
```

Important practices from this example:

- Use IAM roles, environment variables, or an approved credential helper. Do not commit access keys.
- Restrict SSH and management access to approved networks. Do not open port 22 to `0.0.0.0/0`.
- Do not write private keys to an unencrypted local path. Prefer AWS Systems Manager Session Manager or an approved key-management process.
- Use explicit tags for owner, environment, and purpose.
- Add a teardown playbook or documented cleanup step for every learning resource.
- Pin the AMI and instance type to values that are valid in the target account and region.

## 11. ServiceNow ITSM integration

The ServiceNow examples use the `servicenow.itsm` collection to create incidents, problems, change requests, and CMDB configuration items. Credentials are expected through environment variables or an execution environment, not literal YAML values.

```bash
export SN_HOST="https://instance.example.test"
export SN_USERNAME="automation-user"
export SN_PASSWORD="use-a-secret-store"
```

Create an incident:

```yaml
---
- name: Create a ServiceNow incident
  hosts: localhost
  connection: local
  gather_facts: false
  collections:
    - servicenow.itsm
  vars:
    snow_user: "{{ lookup('env', 'SN_USERNAME') }}"
  tasks:
    - name: Create the incident
      servicenow.itsm.incident:
        state: new
        caller: "{{ snow_user }}"
        short_description: "Automated check failed"
        description: "Created by an approved Ansible workflow."
        impact: low
        urgency: low
      register: new_incident

    - name: Show the incident number
      ansible.builtin.debug:
        msg: "Created incident {{ new_incident.record.number }}"
```

Collect node facts and publish them as CMDB data:

```yaml
---
- name: Collect node facts for CMDB
  hosts: nodes
  vars:
    node_info: []
  tasks:
    - name: Collect the inventory data
      ansible.builtin.set_stats:
        data:
          node_info: >-
            {{ node_info + [{
              'hostname': ansible_facts['nodename'],
              'default_ip': ansible_facts['default_ipv4']['address'],
              'default_mac': ansible_facts['default_ipv4']['macaddress']
            }] }}
```

Then use the collected data with `servicenow.itsm.configuration_item`. Confirm the exact class, field names, and required values for your ServiceNow instance before creating records.

The repository also includes an Ansible Navigator configuration that runs an execution environment with `podman` and passes `SN_HOST`, `SN_USERNAME`, and `SN_PASSWORD` into the container. Keep those values in an approved credential store and avoid writing them to logs or playbook artifacts.

Safety notes for ITSM automation:

- Test against a non-production instance first.
- Query records before updating or closing them.
- Confirm the record number, caller, assignment group, and target state.
- Keep destructive cleanup playbooks behind a separate tag, explicit extra variable, or approval step.
- Review whether `state: absent` truly matches the intended business action.

## 12. Execution environments and AWX/AAP

Ansible Navigator and execution environments package Ansible, collections, and Python dependencies into a reproducible container. AWX or Ansible Automation Platform can then run the same content through job templates and workflows.

For a lab installation, see [Ansible AWX Setup on Ubuntu](install-awx-ansible.md). For a broader explanation of inventories, credentials, job templates, and workflow jobs, see [Ansible, AWX, and Automation Platform](ansible-awx.md).

## 13. Validation checklist

Before running a playbook:

1. Run `ansible-playbook --syntax-check`.
2. Review the inventory and confirm the target host group.
3. Run `--check --diff` where the modules support it.
4. Confirm privilege escalation and credentials.
5. Check variable values and record identifiers.
6. Verify that the playbook leaves the system in a known, idempotent state.
7. Plan verification, rollback, and cleanup.

## Further reading

- [Ansible documentation](https://docs.ansible.com/)
- [Ansible playbook guide](https://docs.ansible.com/ansible/latest/playbook_guide/)
- [Ansible collections index](https://docs.ansible.com/ansible/latest/collections/index.html)
- [Ansible Navigator documentation](https://ansible.readthedocs.io/projects/navigator/)
- [ServiceNow ITSM collection](https://github.com/ansible-collections/servicenow.itsm)
