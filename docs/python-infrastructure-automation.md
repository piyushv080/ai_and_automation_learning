# Python for Infrastructure Automation

This guide builds on [Python Basics](python-basics.md) and focuses on using Python for infrastructure operations, REST APIs, AWX jobs, cloud tasks, and troubleshooting.

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

## Infrastructure integrations

### ServiceNow or another request system

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

## Further reading

- [Python tutorial](https://docs.python.org/3/tutorial/)
- [Python `venv` documentation](https://docs.python.org/3/library/venv.html)
- [Requests documentation](https://requests.readthedocs.io/)
- [Ansible Automation Platform documentation](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/)
