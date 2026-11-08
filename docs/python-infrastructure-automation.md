# Python for Infrastructure Automation

This guide builds on [Python Basics](python-basics.md) and focuses on using Python for infrastructure operations, REST APIs, AWX jobs, cloud tasks, and troubleshooting.

The examples follow common learning-lab exercises: system summaries, process inventories, CSV/HTML reports, JSON input, API calls, and error handling. Each example uses generic values and should be adapted to a test environment before operational use.

## Learning objective

For each topic, aim to explain the concept, write a small program, trace its execution, handle errors, and describe where it fits in an infrastructure workflow.

## Core Python concepts

### Variables and data types

Variables are names that refer to values. Common types include `str`, `int`, `float`, `bool`, `list`, `tuple`, `set`, `dict`, and `None`.

```python
server = {
    "name": "web-01",
    "ip": "192.0.2.10",
    "environment": "dev",
    "port": 8080,
    "healthy": True,
}

print(server["name"])
print(type(server["port"]))
print(server.get("owner", "unassigned"))
```

Lists and dictionaries are mutable. Strings, integers, and tuples are immutable. Use a dictionary when values have named fields; use a list for an ordered collection; use a set when uniqueness matters.

### Conditions, loops, and functions

```python
servers = [
    {"name": "web-01", "environment": "prod", "healthy": True},
    {"name": "web-02", "environment": "dev", "healthy": False},
]

def unhealthy_production_hosts(items):
    return [
        item["name"]
        for item in items
        if item.get("environment") == "prod" and not item.get("healthy", False)
    ]

print(unhealthy_production_hosts(servers))
```

Use `for` when iterating over a collection. Use `while` when repetition depends on a condition, and ensure the condition can eventually become false. `break` exits a loop, `continue` skips to its next iteration, and `pass` is a placeholder statement.

Functions package reusable work. A **parameter** is named in a function definition; an **argument** is passed when calling it. `return` sends a value back to the caller; `print()` writes text for a person to read.

### Exceptions and validation

Catch errors that you can handle. Avoid a bare `except`, which can hide programming errors and interrupts.

```python
def read_port(config):
    try:
        port = int(config["port"])
    except KeyError as exc:
        raise ValueError("configuration is missing 'port'") from exc
    except (TypeError, ValueError) as exc:
        raise ValueError("port must be an integer") from exc

    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    return port
```

Automation should validate inputs, fail with useful messages, and return an accurate failure status. Do not report success after catching and ignoring an unexpected exception.

## Files, JSON, and configuration

Use context managers so files are closed even when an exception occurs. JSON is a text format; loading JSON produces Python values such as dictionaries and lists.

```python
import json
from pathlib import Path

config_path = Path("servers.json")
with config_path.open(encoding="utf-8") as file:
    servers = json.load(file)

for server in servers:
    print(server["name"])
```

Keep credentials out of source files and repositories. Load secrets from an approved secret store or environment provided by the runtime, and avoid printing them in logs.

## REST APIs with Python

An API client should set timeouts, check HTTP status, handle network/JSON errors, and keep credentials secure. Install third-party libraries in a virtual environment and pin dependencies where appropriate.

```python
import os
import requests

api_url = os.environ["INVENTORY_API_URL"]
token = os.environ["INVENTORY_API_TOKEN"]

response = requests.get(
    f"{api_url}/servers",
    headers={"Authorization": f"Bearer {token}"},
    timeout=(3, 15),
)
response.raise_for_status()
servers = response.json()
print(f"Received {len(servers)} server records")
```

The tuple passed to `timeout` sets connection and response timeouts. Keep TLS certificate validation enabled. Add pagination, retries with backoff for transient errors, rate-limit handling, and request identifiers when the API requires them. Do not retry non-idempotent operations blindly.

For a read-only health endpoint, wrap network and response parsing errors so the script exits with a useful failure rather than a traceback alone:

```python
import logging
import os

import requests

logger = logging.getLogger(__name__)


def get_health():
    url = os.environ.get("SERVICE_HEALTH_URL", "https://api.example.test/health")
    token = os.environ.get("SERVICE_API_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    try:
        response = requests.get(url, headers=headers, timeout=(3, 10))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout as exc:
        logger.error("Health request timed out")
        raise RuntimeError("health endpoint timed out") from exc
    except requests.exceptions.RequestException as exc:
        logger.error("Health request failed: %s", exc.__class__.__name__)
        raise RuntimeError("could not query health endpoint") from exc
    except ValueError as exc:
        logger.error("Health endpoint returned invalid JSON")
        raise RuntimeError("invalid health response") from exc
```

Set endpoint values and credentials in the runtime environment or an approved secret store. Do not log the URL if it contains sensitive query parameters, and never print the token.

## System information report

The lab includes system-summary exercises. Python's standard library can report basic runtime and operating-system details; the optional `psutil` package adds CPU, memory, disk, and process metrics.

```python
import os
import platform


def basic_system_summary():
    details = platform.uname()
    return {
        "system": details.system,
        "release": details.release,
        "architecture": details.machine,
        "logical_cpu_count": os.cpu_count(),
    }


if __name__ == "__main__":
    for key, value in basic_system_summary().items():
        print(f"{key}: {value}")
```

For optional metrics, install `psutil` in the project's virtual environment:

```bash
python -m pip install psutil
```

```python
import psutil

memory = psutil.virtual_memory()
print(f"Available memory: {memory.available} bytes")
print(f"Memory used: {memory.percent}%")
```

Treat system reports as potentially sensitive: they can reveal hostnames, usernames, process names, mount paths, and software versions. Keep reports local unless sharing is approved, and remove fields that the recipient does not need.

## Exporting a process inventory to CSV

`psutil.process_iter` safely iterates over processes, but permissions and process lifetimes can change while the report is being collected. Handle those cases and write only fields needed for the task.

```python
import csv
from pathlib import Path

import psutil


def export_processes(destination):
    output_path = Path(destination)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []

    for process in psutil.process_iter(attrs=["pid", "name", "memory_percent"]):
        try:
            info = process.info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

        rows.append({
            "pid": info.get("pid"),
            "name": info.get("name") or "unknown",
            "memory_percent": round(info.get("memory_percent") or 0, 2),
        })

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["pid", "name", "memory_percent"],
        )
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


if __name__ == "__main__":
    count = export_processes(Path.home() / "reports" / "process-inventory.csv")
    print(f"Wrote {count} process records")
```

This report is read-only, but process names can still expose private activity. Review and sanitize reports before sharing them.

## Build a small HTML report

If a report needs to be viewed in a browser, escape dynamic values before inserting them into HTML. For more complex reports, use a maintained template library rather than concatenating large HTML strings.

```python
from html import escape
from pathlib import Path

rows = [
    {"name": "web-01", "status": "healthy"},
    {"name": "web-02", "status": "unknown"},
]

table_rows = "\n".join(
    f"<tr><td>{escape(str(row['name']))}</td>"
    f"<td>{escape(str(row['status']))}</td></tr>"
    for row in rows
)
report_html = (
    "<!doctype html><html lang='en'><meta charset='utf-8'>"
    "<title>Sample health report</title><table>"
    "<thead><tr><th>System</th><th>Status</th></tr></thead>"
    f"<tbody>{table_rows}</tbody></table></html>"
)

Path("health-report.html").write_text(report_html, encoding="utf-8")
```

HTML escaping prevents data values from being interpreted as markup. Do not publish reports containing real host, process, or user information without reviewing and sanitizing them.

## CSV input and data validation

Validate each record before using it. Skip or report bad rows rather than assuming that a file is complete and well-formed.

```python
import csv
from pathlib import Path


def load_servers(path):
    servers = []
    with Path(path).open(newline="", encoding="utf-8") as file:
        for row_number, row in enumerate(csv.DictReader(file), start=2):
            name = (row.get("name") or "").strip()
            environment = (row.get("environment") or "").strip().lower()
            if not name or environment not in {"dev", "test", "prod"}:
                raise ValueError(f"invalid inventory row {row_number}")
            servers.append({"name": name, "environment": environment})
    return servers
```

## Infrastructure integrations

### IT service-management or ticketing system

A typical integration reads an approved request, validates required fields, maps the request to an allowlisted operation, starts a job, tracks its result, verifies the target state, and updates the request with accurate status. Apply authorization and approval checks before changing infrastructure.

### AWX / Ansible Automation Platform

Python can call the supported AWX/AAP API to launch an approved job template and poll job status. A safe workflow should:

1. Authenticate using a protected credential.
2. Validate the incoming request and permitted parameters.
3. Launch only an approved job template.
4. Record the job ID and poll until a terminal state or timeout.
5. Verify the actual target service or configuration independently.
6. Report failures and evidence accurately.

Exact endpoints and authentication options depend on the deployed AWX/AAP version; consult its API schema and documentation.

### Cloud and operations automation

Use the cloud provider's supported SDK or API. Scope credentials to the minimum required permissions, make operations idempotent where possible, and include dry-run or plan steps for changes that can affect production resources.

## Project structure and dependencies

- A **module** is a Python file that can be imported.
- A **package** groups related modules.
- A **virtual environment** isolates project dependencies from other Python projects.
- `requirements.txt` records Python packages needed by a project.

```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Use a clear separation between API clients, business logic, configuration, and command-line entry points as a project grows.

## Testing and troubleshooting

Unit tests should cover input validation, success paths, expected API errors, timeouts, malformed responses, and retry behavior. Mock external services when testing locally so that tests do not modify production data. Add integration tests against a disposable or explicitly designated environment.

When an automation fails, capture the operation, sanitized request context, status code, and correlation/job ID. Do not log tokens, passwords, or sensitive response bodies. Check connectivity, authentication, permissions, input values, API limits, and the remote job's own output.

## Practice exercises

1. Read a JSON list of server records and report those marked unhealthy.
2. Validate a server name, environment, and port before continuing.
3. Call a test API with a timeout and handle a non-success status.
4. Add pagination and a bounded retry for temporary failures.
5. Design a flow that launches an approved AWX job and verifies the result.
6. Write tests for invalid input, a timeout, and a successful API response.
7. Create a read-only system summary and mark which fields should be sanitized before sharing.
8. Export a local process inventory to CSV and handle processes that disappear during collection.

## Further reading

- [Python tutorial](https://docs.python.org/3/tutorial/)
- [Python `venv` documentation](https://docs.python.org/3/library/venv.html)
- [Requests documentation](https://requests.readthedocs.io/)
- [Ansible Automation Platform documentation](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/)
