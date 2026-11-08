# Python Basics

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

## Modules and virtual environments

A module is a Python file containing reusable code. A package organizes related modules. A virtual environment keeps one project’s dependencies separate from other Python projects.

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\\Scripts\\Activate.ps1  # Windows PowerShell
python -m pip install requests
```

Record project dependencies in `requirements.txt` so the environment can be recreated. Review and pin dependency versions for shared or production projects.

## Practice

1. Create a list of server dictionaries with a name, environment, and health status.
2. Print only production servers and count them.
3. Write a function that returns unhealthy servers.
4. Read a server list from a JSON file and handle a missing key.

Next: [Python for Infrastructure Automation](python-infrastructure-automation.md) covers APIs, error handling, logging, AWX and ServiceNow workflows, and testing.
