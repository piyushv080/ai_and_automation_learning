# Python Basic

Use this page to learn core Python syntax and data structures. The examples use server data so the concepts connect to infrastructure work.

## Variables

Variables are names that refer to values. Python values have types, including `str` (text), `int` (whole numbers), `float` (decimal numbers), `bool` (`True` or `False`), and `None` (no value).

```python
server_name = "web-01"
port = 8080
is_healthy = True

print(server_name)
print(type(port))
```

Use names that explain the value. Python is dynamically typed, but choosing and validating the expected type still matters. Use `snake_case` for variable and function names and `UPPER_SNAKE_CASE` for constants.

## Collections

Use a list for an ordered, changeable sequence; a tuple for a fixed sequence; a set for unique values; and a dictionary for named key-value data.

```python
servers = ["web-01", "web-02", "db-01"]
servers.append("web-03")
print(servers[0])

server_config = ("web-01", 8080)  # tuple
environments = {"dev", "test", "prod", "dev"}  # set: duplicates collapse

server = {
    "name": "web-01",
    "ip": "192.0.2.10",
    "environment": "dev",
}
print(server["name"])
print(server.get("owner", "unknown"))
```

Lists and dictionaries are mutable: they can be changed after creation. Strings, integers, and tuples are immutable. `dictionary[key]` raises `KeyError` if the key is missing; `dictionary.get(key, default)` lets you supply a fallback.

## Conditions

Use `if`, `elif`, and `else` to choose what a program does:

```python
status_code = 200

if status_code == 200:
    print("Request successful")
elif status_code >= 500:
    print("Server error")
else:
    print("Unexpected response")
```

## Loops

Use a `for` loop to repeat an action for each item in a collection:

```python
servers = [
    {"name": "web-01", "environment": "dev"},
    {"name": "web-02", "environment": "prod"},
    {"name": "db-01", "environment": "prod"},
]

for server in servers:
    if server["environment"] == "prod":
        print(server["name"])
```

`break` exits a loop, `continue` skips to the next iteration, and `pass` is a placeholder statement. A `while` loop repeats while a condition remains true; make sure its condition can eventually become false.

## Functions

Functions package reusable work. A parameter appears in a function definition; an argument is the value passed when the function is called. `return` sends a value back to the caller, while `print()` displays text.

```python
def is_healthy(status_code):
    return status_code == 200


result = is_healthy(200)
print(result)
```

Functions can accept multiple arguments and defaults. Keep one function focused on one operation so it can be understood and tested independently.

```python
def format_health_message(server_name, status="unknown"):
    return f"{server_name}: {status}"


print(format_health_message("web-01", "healthy"))
print(format_health_message("web-02"))
```

Avoid mutable default arguments such as `items=[]`; use `None` and create a fresh list inside the function instead.

## Strings

Strings are text. Common methods include `.strip()`, `.lower()`, `.upper()`, `.split()`, and `.replace()`. An f-string inserts values into text:

```python
server_name = "  WEB-01  "
clean_name = server_name.strip().lower()
status = "healthy"
print(f"Server {clean_name} is {status}")
```

## Handling errors

An exception is an error raised while a program runs. Catch specific exceptions that you can handle; avoid a bare `except`, which can hide bugs.

```python
try:
    port = int("8080")
except ValueError:
    print("Port must be a number")
else:
    print(f"Port: {port}")
finally:
    print("Validation finished")
```

`try` contains code that may fail, `except` handles the specified error, `else` runs when no error occurred, and `finally` runs either way.

## Files and JSON

Use `with` to open files; Python closes the file when the block ends. JSON is a text format commonly used to exchange data between applications. Loading JSON produces normal Python values such as dictionaries and lists.

```python
import json

with open("server.json", encoding="utf-8") as file:
    server = json.load(file)

print(server["name"])
```

Use `pathlib.Path` for portable paths. The CSV module can read and write tabular reports without manually joining values with commas.

```python
import csv
from pathlib import Path

report_path = Path("reports") / "server-status.csv"
report_path.parent.mkdir(parents=True, exist_ok=True)

rows = [
    {"name": "web-01", "status": "healthy"},
    {"name": "web-02", "status": "unknown"},
]

with report_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "status"])
    writer.writeheader()
    writer.writerows(rows)
```

Use only sample or approved data in reports. Review generated files before sharing them because logs and inventories can contain identifying system details.

## Modules and virtual environments

A module is a Python file containing reusable code. A package organizes related modules. A virtual environment keeps one project's dependencies separate from other Python projects.

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\Activate.ps1    # Windows PowerShell
python -m pip install requests
```

Record project dependencies in `requirements.txt` so the environment can be recreated. Review and pin dependency versions for shared or production projects.

The standard library includes modules for common tasks: `pathlib` for paths, `json` and `csv` for data files, `logging` for operational messages, `argparse` for command-line options, `platform` for operating-system details, and `subprocess` for invoking external programs. Prefer a standard-library solution when it meets the need.

## Command-line input and validation

For a tiny exercise, `input()` is convenient. For reusable scripts, `argparse` provides named options, help text, and type conversion.

```python
import argparse

parser = argparse.ArgumentParser(description="Summarize a sample inventory")
parser.add_argument("inventory", help="Path to an input JSON file")
parser.add_argument("--environment", default="dev")
args = parser.parse_args()

print(f"Read {args.inventory} for environment {args.environment}")
```

Validate values before using them in file paths, API calls, or infrastructure operations. Treat external input as untrusted.

## Logging

Use logging instead of relying on `print()` for scripts that need diagnostics. Never include credentials or sensitive response data in log messages.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logging.info("Starting inventory summary")
logging.warning("A sample record has no status field")
```

## Testing a function

Small functions are easier to test than scripts that perform all work at import time. Put executable behavior under a main guard so importing a module does not start an automation job.

```python
def is_success(status_code):
    return status_code == 200


def main():
    print(is_success(200))


if __name__ == "__main__":
    main()
```

## Practice

1. Create a list of server dictionaries with a name, environment, and health status.
2. Print only production servers and count them.
3. Write a function that returns unhealthy servers.
4. Read a server list from a JSON file and handle a missing key.
5. Export a filtered sample inventory to CSV.
6. Add command-line options, logging, and tests for a small validation function.

Next: continue with [Python Advanced](python-advanced.md) for REST APIs, system reports, integrations, and troubleshooting.
