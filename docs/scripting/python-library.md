# Python Library Master Guide

## A practical reference for infrastructure automation engineers

**Purpose:** Learn Python libraries by understanding their purpose,
functions, inputs, processing logic, return values, errors, and real
infrastructure use cases.

This guide is designed for a learner who can understand existing Python
examples but wants to become confident writing programs independently.

------------------------------------------------------------------------

# 1. How to study any Python library

Do not memorize every function. For each library, use this learning
sequence:

1.  **Purpose:** What problem does this library solve?
2.  **When to use it:** What kind of task needs this library?
3.  **Import:** How is it made available in a Python program?
4.  **Object model:** What objects, classes, or data types does it work
    with?
5.  **Common functions:** What are the most useful functions and
    methods?
6.  **Input:** What arguments, files, objects, or values does each
    function accept?
7.  **Processing:** What does the function do with that input?
8.  **Return value:** What does it return, modify, or create?
9.  **Exceptions:** What can fail, and which exceptions should be
    handled?
10. **Practical example:** How does it help with infrastructure
    automation?
11. **Independent exercise:** Can you recreate the solution without
    looking?
12. **Verification:** How will you prove the result is correct?

## The Input → Processing → Output pattern

For every function, document:

  --------------------------------------------------------------------------
  Element                 Meaning                 Example
  ----------------------- ----------------------- --------------------------
  Input                   Arguments or data       `Path("inventory.json")`
                          supplied                

  Processing              Operation performed     Check whether the file
                                                  exists

  Output                  Return value or side    `True` or `False`
                          effect                  

  Error                   Failure condition       Permission denied

  Verification            How to check the result Test with existing and
                                                  missing paths
  --------------------------------------------------------------------------

**Important distinction:** A Python function may return a value, modify
an object, write a file, perform a network operation, or do several of
these. Always check the function's documentation rather than assuming it
returns something useful.

------------------------------------------------------------------------

# 2. Python Standard Library

The standard library is included with Python. These modules normally do
not require a separate package installation.

## 2.1 `os` --- Operating system interfaces

**Purpose:** Interact with operating-system features such as environment
variables, directories, paths, and process-related information.

**Import**

``` python
import os
```

**Important functions**

  ------------------------------------------------------------------------------------------
  Function / attribute                 Input             What it does      Output
  ------------------------------------ ----------------- ----------------- -----------------
  `os.getcwd()`                        None              Gets current      Path string
                                                         working directory 

  `os.chdir(path)`                     Directory path    Changes current   None
                                                         directory         

  `os.listdir(path)`                   Directory path    Lists directory   List of names
                                                         entries           

  `os.mkdir(path)`                     New directory     Creates one       None
                                       path              directory         

  `os.makedirs(path, exist_ok=True)`   Directory path    Creates nested    None
                                                         directories       

  `os.remove(path)`                    File path         Removes a file    None

  `os.rename(src, dst)`                Source and        Renames/moves a   None
                                       destination       filesystem entry  

  `os.getenv(key, default)`            Variable name,    Reads environment String or default
                                       optional default  variable          

  `os.environ`                         Environment       Reads/updates     Mapping
                                       mapping           process           
                                                         environment       

  `os.path.exists(path)`               Path              Checks whether a  Boolean
                                                         path exists       

  `os.path.isfile(path)`               Path              Checks for        Boolean
                                                         regular file      

  `os.path.isdir(path)`                Path              Checks for        Boolean
                                                         directory         

  `os.path.getsize(path)`              Path              Gets file size in Integer
                                                         bytes             
  ------------------------------------------------------------------------------------------

**Example:**

``` python
import os

folder = "server_reports"

if not os.path.exists(folder):
    os.makedirs(folder)

print("Working directory:", os.getcwd())
print("Report directory exists:", os.path.isdir(folder))
```

**Input:** Folder name.

**Logic:** Check whether the directory exists; create it if missing.

**Output:** Directory created if necessary, plus status information.

**Common errors:** `FileNotFoundError`, `PermissionError`, `OSError`.

**Infrastructure use:** Read environment-based configuration, prepare
report directories, inspect files, and manage local automation
workspaces.

**Safety:** Never use a destructive file operation on a path supplied by
an untrusted user without validation. Do not store secrets in source
code.

**Exercises** 1. Print the current working directory. 2. List all files
in a given directory. 3. Create a report directory if it does not exist.
4. Read an environment variable named `ENVIRONMENT`. 5. Check whether a
given inventory file exists.

------------------------------------------------------------------------

## 2.2 `sys` --- Python runtime and interpreter interface

**Purpose:** Interact with the Python interpreter and current process.

``` python
import sys
```

  ------------------------------------------------------------------------
  Function /         Input             Processing        Output
  attribute                                              
  ------------------ ----------------- ----------------- -----------------
  `sys.argv`         Command-line      Exposes arguments List of strings
                     arguments         passed to script  

  `sys.exit(code)`   Exit code/message Terminates        Raises
                                       program           `SystemExit`

  `sys.version`      None              Reads Python      Version string
                                       version           

  `sys.platform`     None              Identifies        Platform
                                       platform          identifier

  `sys.executable`   None              Finds Python      Path string
                                       executable        

  `sys.path`         None              Shows module      List of paths
                                       search paths      

  `sys.stdin`        Standard input    Reads input       Text stream
                     stream            stream            

  `sys.stdout`       Standard output   Writes normal     Text stream
                     stream            output            

  `sys.stderr`       Error output      Writes diagnostic Text stream
                     stream            output            
  ------------------------------------------------------------------------

**Example:**

``` python
import sys

print("Python:", sys.version)
print("Platform:", sys.platform)

if len(sys.argv) < 2:
    print("Usage: python check.py <environment>")
    sys.exit(2)

environment = sys.argv[1]
print("Environment:", environment)
```

**Input:** Command-line argument.

**Output:** Environment name or usage error and exit code.

**Infrastructure use:** Build scripts that accept environment,
inventory, or report-path options. Return meaningful exit codes to
schedulers and CI/CD pipelines.

**Exercises** 1. Print Python version and executable path. 2. Accept a
hostname from command-line arguments. 3. Require an environment
argument. 4. Exit with a non-zero code when required input is missing.

------------------------------------------------------------------------

## 2.3 `pathlib` --- Object-oriented filesystem paths

**Purpose:** Work with paths in a readable, cross-platform way.

``` python
from pathlib import Path
```

  Method / property   Input         Processing                   Output
  ------------------- ------------- ---------------------------- -----------------
  `Path(path)`        Path string   Creates path object          `Path` object
  `.exists()`         None          Checks existence             Boolean
  `.is_file()`        None          Checks regular file          Boolean
  `.is_dir()`         None          Checks directory             Boolean
  `.name`             None          Gets final path component    String
  `.suffix`           None          Gets extension               String
  `.parent`           None          Gets parent path             `Path` object
  `.mkdir()`          Options       Creates directory            None
  `.iterdir()`        None          Iterates directory entries   Iterator
  `.read_text()`      Encoding      Reads text                   String
  `.write_text()`     Text          Writes text                  Character count
  `.read_bytes()`     None          Reads binary data            Bytes
  `.glob(pattern)`    Pattern       Finds matching paths         Iterator

**Example:**

``` python
from pathlib import Path

inventory = Path("data/servers.json")

if inventory.is_file():
    content = inventory.read_text(encoding="utf-8")
    print(content)
else:
    print("Inventory file not found")
```

**Infrastructure use:** Build cross-platform paths for inventories,
logs, backups, and configuration files.

**Exercises** 1. Create `reports/`. 2. Find all `.log` files in a
directory. 3. Read a JSON file as text. 4. Check whether a backup file
exists. 5. Build a path using `Path` rather than manually joining
strings.

------------------------------------------------------------------------

## 2.4 `shutil` --- High-level file operations

**Purpose:** Copy, move, archive, and inspect filesystem usage.

``` python
import shutil
```

  -----------------------------------------------------------------------------------
  Function                      Input             Processing        Output
  ----------------------------- ----------------- ----------------- -----------------
  `shutil.copy(src, dst)`       Source and        Copies file       Destination path
                                destination                         

  `shutil.copy2(src, dst)`      Source and        Copies file and   Destination path
                                destination       metadata          

  `shutil.copytree(src, dst)`   Directories       Copies directory  Destination path
                                                  tree              

  `shutil.move(src, dst)`       Source and        Moves             Destination path
                                destination       file/directory    

  `shutil.rmtree(path)`         Directory path    Recursively       None
                                                  removes directory 

  `shutil.make_archive(...)`    Base name,        Creates archive   Archive path
                                format, root                        

  `shutil.disk_usage(path)`     Filesystem path   Reads capacity    Named tuple:
                                                  usage             total, used, free
  -----------------------------------------------------------------------------------

**Example:**

``` python
import shutil

usage = shutil.disk_usage(".")

print("Total GB:", round(usage.total / (1024 ** 3), 2))
print("Used GB:", round(usage.used / (1024 ** 3), 2))
print("Free GB:", round(usage.free / (1024 ** 3), 2))
```

**Infrastructure use:** Backup files, package reports, archive logs, and
check local disk capacity.

**Safety:** `rmtree()` is destructive. Do not practise it on important
directories.

**Exercises** 1. Copy a sample configuration file. 2. Create an archive
of a test folder. 3. Print disk usage in GB. 4. Move an old test report
into an archive directory.

------------------------------------------------------------------------

## 2.5 `subprocess` --- Run external commands

**Purpose:** Execute programs such as Git, Ansible, system tools, and
PowerShell.

``` python
import subprocess
```

  --------------------------------------------------------------------------------
  Function / option       Input             Processing        Output
  ----------------------- ----------------- ----------------- --------------------
  `subprocess.run()`      Command and       Runs a process    `CompletedProcess`
                          options           and waits         

  `capture_output=True`   Run option        Captures stdout   Available on result
                                            and stderr        

  `text=True`             Run option        Decodes streams   String streams
                                            as text           

  `check=True`            Run option        Raises on         Result or exception
                                            non-zero exit     

  `timeout=seconds`       Run option        Limits execution  Result or timeout
                                            time              error

  `result.returncode`     Completed process Reads exit status Integer

  `result.stdout`         Completed process Reads captured    String/bytes
                                            standard output   

  `result.stderr`         Completed process Reads captured    String/bytes
                                            error output      
  --------------------------------------------------------------------------------

**Example:**

``` python
import subprocess

result = subprocess.run(
    ["python", "--version"],
    capture_output=True,
    text=True,
    timeout=10
)

print("Exit code:", result.returncode)
print("Output:", result.stdout or result.stderr)
```

**Input:** Executable and argument list.

**Logic:** Start process, wait, collect status and output.

**Output:** Exit code, standard output, standard error.

**Infrastructure use:** Run approved Ansible commands, Git commands,
PowerShell scripts, and system utilities.

**Safety rules** - Prefer a list of arguments instead of `shell=True`. -
Do not concatenate untrusted input into shell commands. - Set a
timeout. - Capture and inspect the return code. - Run with least
privilege.

**Exercises** 1. Run `python --version`. 2. Run `git --version`. 3.
Capture stdout and stderr. 4. Handle a command that returns a non-zero
exit code. 5. Add a timeout.

------------------------------------------------------------------------

## 2.6 `json` --- JSON data processing

**Purpose:** Convert between JSON text and Python data structures.

``` python
import json
```

  ------------------------------------------------------------------------------
  Function                 Input             Processing        Output
  ------------------------ ----------------- ----------------- -----------------
  `json.loads(text)`       JSON string       Parses JSON       Python object

  `json.load(file)`        Open file object  Parses JSON file  Python object

  `json.dumps(obj)`        Python object     Serializes to     String
                                             JSON string       

  `json.dump(obj, file)`   Python object and Writes JSON       None
                           file                                

  `indent=4`               Serialization     Formats output    Readable JSON
                           option                              

  `sort_keys=True`         Serialization     Sorts object keys Ordered JSON text
                           option                              
  ------------------------------------------------------------------------------

**Example:**

``` python
import json

server = {
    "name": "web01",
    "environment": "test",
    "status": "running"
}

json_text = json.dumps(server, indent=4)
print(json_text)

parsed = json.loads(json_text)
print(parsed["name"])
```

**Infrastructure use:** Inventory files, REST API request bodies, API
responses, and configuration exchange.

**Exercises** 1. Parse a JSON string. 2. Read a server inventory JSON
file. 3. Extract all hostnames. 4. Find records with status `stopped`.
5. Write filtered records into a new JSON file.

------------------------------------------------------------------------

## 2.7 `csv` --- CSV file processing

**Purpose:** Read and write tabular data.

``` python
import csv
```

  ------------------------------------------------------------------------------------------
  Function                             Input             Processing        Output
  ------------------------------------ ----------------- ----------------- -----------------
  `csv.reader(file)`                   File object       Reads rows as     Reader iterator
                                                         lists             

  `csv.DictReader(file)`               File object       Maps columns to   Dictionary rows
                                                         values            

  `csv.writer(file)`                   File object       Creates row       Writer object
                                                         writer            

  `csv.DictWriter(file, fieldnames)`   File and column   Writes dictionary Writer object
                                       names             rows              

  `.writerow(row)`                     One row           Writes one record None

  `.writerows(rows)`                   Multiple rows     Writes records    None
  ------------------------------------------------------------------------------------------

**Example:**

``` python
import csv

servers = [
    {"name": "web01", "status": "running"},
    {"name": "db01", "status": "stopped"}
]

with open("servers.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["name", "status"]
    )
    writer.writeheader()
    writer.writerows(servers)
```

**Infrastructure use:** Server inventory, patch reports, compliance
exports, and health summaries.

**Exercises** 1. Read CSV rows. 2. Filter stopped servers. 3. Count
records by environment. 4. Write unhealthy servers to a separate CSV.

------------------------------------------------------------------------

## 2.8 `datetime` and `time`

**Purpose:** Work with dates, timestamps, durations, and delays.

``` python
from datetime import datetime, timezone, timedelta
import time
```

  --------------------------------------------------------------------------------------
  Function                         Input             Processing        Output
  -------------------------------- ----------------- ----------------- -----------------
  `datetime.now(timezone.utc)`     Optional timezone Gets current      `datetime`
                                                     aware time        

  `datetime.fromisoformat(text)`   ISO timestamp     Parses date/time  `datetime`

  `.strftime(format)`              Format string     Formats date/time String

  `.isoformat()`                   None              Formats ISO       String
                                                     timestamp         

  `timedelta(...)`                 Duration          Represents time   `timedelta`
                                   components        difference        

  `time.time()`                    None              Reads epoch time  Float

  `time.sleep(seconds)`            Delay             Pauses execution  None

  `time.perf_counter()`            None              Reads             Float
                                                     high-resolution   
                                                     timer             
  --------------------------------------------------------------------------------------

**Infrastructure use:** Maintenance windows, log timestamps, report
names, polling intervals, and execution duration.

Prefer timezone-aware UTC timestamps when exchanging timestamps between
systems.

**Exercises** 1. Print current UTC time. 2. Format a timestamp for a
report filename. 3. Calculate how old a backup is. 4. Measure script
execution duration.

------------------------------------------------------------------------

## 2.9 `logging` --- Application logging

**Purpose:** Record program events and diagnostic details.

``` python
import logging
```

  ----------------------------------------------------------------------------------
  Function                     Input             Processing        Output
  ---------------------------- ----------------- ----------------- -----------------
  `logging.basicConfig(...)`   Level, format,    Configures root   Configuration
                               filename          logging           

  `logging.debug(msg)`         Message           Records debug     Log record
                                                 event             

  `logging.info(msg)`          Message           Records normal    Log record
                                                 event             

  `logging.warning(msg)`       Message           Records warning   Log record

  `logging.error(msg)`         Message           Records error     Log record

  `logging.exception(msg)`     Message inside    Records error and Log record
                               exception handler traceback         

  `logging.critical(msg)`      Message           Records critical  Log record
                                                 event             
  ----------------------------------------------------------------------------------

**Example:**

``` python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filename="automation.log"
)

logging.info("Health check started")
logging.warning("CPU usage exceeded threshold")
```

**Infrastructure use:** Record job starts, target names, outcomes,
timings, and safe error context.

Never log passwords, tokens, private keys, or sensitive payloads.

**Exercises** 1. Write INFO and ERROR events. 2. Log an exception with
traceback. 3. Log to a file. 4. Include hostname and execution ID in
messages.

------------------------------------------------------------------------

## 2.10 `argparse` --- Command-line interfaces

**Purpose:** Create scripts that accept named command-line options.

``` python
import argparse
```

  ------------------------------------------------------------------------------
  Method               Input                 Processing        Output
  -------------------- --------------------- ----------------- -----------------
  `ArgumentParser()`   Description/options   Creates parser    Parser object

  `.add_argument()`    Option name and rules Defines accepted  Updated parser
                                             input             

  `.parse_args()`      Usually process CLI   Parses and        Namespace
                       arguments             validates         
                                             arguments         

  `type=`              Conversion function   Converts supplied Typed value
                                             text              

  `choices=`           Allowed values        Restricts input   Validated
                                                               selection

  `required=True`      Option setting        Requires argument Parser error if
                                                               missing
  ------------------------------------------------------------------------------

**Example:**

``` python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--environment", required=True,
                    choices=["dev", "test", "prod"])
parser.add_argument("--threshold", type=int, default=80)

args = parser.parse_args()

print(args.environment)
print(args.threshold)
```

Run:

``` bash
python health.py --environment test --threshold 85
```

**Infrastructure use:** Reusable scripts that accept environment,
inventory path, threshold, or report destination.

**Exercises** 1. Accept a hostname. 2. Accept an environment with
allowed choices. 3. Accept a CPU threshold as an integer. 4. Reject
missing or invalid arguments.

------------------------------------------------------------------------

## 2.11 `socket` --- Network programming basics

**Purpose:** Work with network addresses and low-level connections.

``` python
import socket
```

  ------------------------------------------------------------------------------------------------------------------
  Function                                                Input                  Processing        Output
  ------------------------------------------------------- ---------------------- ----------------- -----------------
  `socket.gethostname()`                                  None                   Reads local       String
                                                                                 hostname          

  `socket.gethostbyname(host)`                            Hostname               Resolves IPv4     IP string
                                                                                 address           

  `socket.getaddrinfo(...)`                               Host/service/options   Resolves address  Address tuples
                                                                                 details           

  `socket.create_connection((host, port), timeout=...)`   Host, port and timeout Attempts TCP      Socket object or
                                                                                 connection        error

  `.close()`                                              None                   Closes socket     None
  ------------------------------------------------------------------------------------------------------------------

**Example:**

``` python
import socket

host = "example.com"
port = 443

try:
    with socket.create_connection((host, port), timeout=3):
        print("TCP connection successful")
except OSError as error:
    print("Connection failed:", error)
```

**Infrastructure use:** Test DNS resolution and TCP reachability.

A successful TCP connection does not prove that an application is
healthy. Use an application-level HTTP check when appropriate.

**Exercises** 1. Print local hostname. 2. Resolve a hostname. 3. Test a
TCP port with a timeout. 4. Report reachable and unreachable lab
endpoints.

------------------------------------------------------------------------

## 2.12 `platform`, `getpass`, `configparser`, `tempfile`, `hashlib`, `secrets`

  --------------------------------------------------------------------------------
  Module            Useful functions          Input              Output / use
  ----------------- ------------------------- ------------------ -----------------
  `platform`        `system()`, `release()`,  Current runtime    OS and
                    `machine()`,                                 architecture
                    `python_version()`                           details

  `getpass`         `getpass()`               Prompt             Hidden terminal
                                                                 input

  `configparser`    `ConfigParser()`,         INI                Configuration
                    `read()`, `get()`         file/section/key   value

  `tempfile`        `TemporaryDirectory()`,   Options/prefix     Temporary
                    `NamedTemporaryFile()`                       path/file

  `hashlib`         `sha256()`, `.update()`,  Bytes              Digest for
                    `.hexdigest()`                               integrity checks

  `secrets`         `token_hex()`,            Token length       Secure random
                    `token_urlsafe()`                            token
  --------------------------------------------------------------------------------

**Exercises** 1. Detect the OS platform. 2. Read a test INI
configuration. 3. Create and clean up a temporary directory. 4.
Calculate a SHA-256 digest for a sample file. 5. Generate a random test
token without printing production secrets.

------------------------------------------------------------------------

# 3. Advanced standard-library modules

## 3.1 `collections`

Useful types:

  ------------------------------------------------------------------------------
  Type                     Input             Processing        Output
  ------------------------ ----------------- ----------------- -----------------
  `Counter(items)`         Iterable          Counts            Frequency mapping
                                             occurrences       

  `defaultdict(factory)`   Factory and keys  Supplies default  Dictionary-like
                                             values            object

  `deque(items)`           Iterable          Efficient         Double-ended
                                             append/pop at     queue
                                             both ends         

  `namedtuple(...)`        Field names       Creates tuple     Named tuple
                                             record type       instances
  ------------------------------------------------------------------------------

Infrastructure example: count incidents by priority or group servers by
environment.

## 3.2 `itertools`

Useful functions:

-   `chain(iterables)` --- combine iterables.
-   `islice(iterable, start, stop)` --- select a portion.
-   `groupby(iterable, key=...)` --- group adjacent equal keys; sort
    first if required.
-   `product(...)` --- Cartesian product.
-   `combinations(items, r)` --- combinations.

Use it for efficient iteration and data combinations. Be aware that many
functions return iterators, not lists.

## 3.3 `functools`

Useful functions:

-   `lru_cache` / `cache` --- cache function results.
-   `partial` --- pre-fill some function arguments.
-   `wraps` --- preserve wrapped function metadata.
-   `reduce` --- accumulate iterable values.

Learn decorators and caching after you are comfortable with normal
functions.

## 3.4 `dataclasses`

**Purpose:** Define classes mainly used to hold structured data.

``` python
from dataclasses import dataclass

@dataclass
class Server:
    name: str
    environment: str
    status: str

server = Server("web01", "test", "running")
print(server.name)
```

Input: field values. Processing: generated initializer and data-class
methods. Output: structured object.

Use it for typed inventory records and configuration models.

## 3.5 `typing`

Useful annotations:

-   `list[str]`
-   `dict[str, str]`
-   `Optional[str]` or `str | None`
-   `Union[...]` or `|`
-   `TypedDict`
-   `Protocol`
-   `Callable`

Type hints help readers, editors, and static type checkers. Python does
not automatically enforce most annotations at runtime.

## 3.6 `unittest`

Core concepts:

-   `TestCase`
-   `setUp()` and `tearDown()`
-   `assertEqual()`
-   `assertTrue()`
-   `assertRaises()`
-   `unittest.mock`

Input: test fixtures and function arguments. Processing: execute test
cases and compare expectations. Output: test report.

## 3.7 Concurrency modules

  ----------------------------------------------------------------------------
  Module                 Best suited to    Key concepts      Output
  ---------------------- ----------------- ----------------- -----------------
  `threading`            I/O-bound work    Thread, Lock,     Concurrent task
                                           Event             results

  `multiprocessing`      CPU-bound work    Process, Pool,    Parallel
                                           Queue             computation
                                                             results

  `asyncio`              Async I/O         `async`, `await`, Awaited coroutine
                                           Task, gather      results

  `concurrent.futures`   Managed           Executor, Future, Results or task
                         thread/process    `submit`, `map`   exceptions
                         pools                               
  ----------------------------------------------------------------------------

For infrastructure checks that wait on network responses, thread pools
or asynchronous I/O can help. Start with sequential code first, then add
concurrency. Set timeouts and limit concurrency to avoid overwhelming
systems.

------------------------------------------------------------------------

# 4. Third-party packages

Third-party packages are installed separately. Use a virtual environment
for each project.

## 4.1 Create a virtual environment

``` bash
python -m venv .venv
```

Activate on Windows PowerShell:

``` powershell
.venv\Scripts\Activate.ps1
```

Activate on Linux/macOS Bash:

``` bash
source .venv/bin/activate
```

Install a package:

``` bash
python -m pip install requests
```

Record dependencies:

``` bash
python -m pip freeze > requirements.txt
```

Install dependencies later:

``` bash
python -m pip install -r requirements.txt
```

## 4.2 `requests` --- HTTP and REST APIs

Install:

``` bash
python -m pip install requests
```

Import:

``` python
import requests
```

  -------------------------------------------------------------------------------------
  Function / property             Input             Processing        Output
  ------------------------------- ----------------- ----------------- -----------------
  `requests.get(url, ...)`        URL, params,      Sends GET         Response
                                  headers, timeout                    

  `requests.post(url, ...)`       URL, JSON/data,   Sends POST        Response
                                  headers, timeout                    

  `requests.put(url, ...)`        URL and           Sends PUT         Response
                                  replacement                         
                                  payload                             

  `requests.patch(url, ...)`      URL and partial   Sends PATCH       Response
                                  payload                             

  `requests.delete(url, ...)`     URL               Sends DELETE      Response

  `response.status_code`          Response          Reads HTTP status Integer

  `response.json()`               JSON response     Parses JSON       Python object
                                  body                                

  `response.text`                 Response          Decodes text body String

  `response.raise_for_status()`   Response          Raises for HTTP   None or exception
                                                    4xx/5xx           

  `response.headers`              Response          Reads headers     Mapping
  -------------------------------------------------------------------------------------

**Example:**

``` python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    print("Title:", data["title"])

except requests.Timeout:
    print("Request timed out")
except requests.HTTPError as error:
    print("HTTP error:", error)
except requests.RequestException as error:
    print("Request failed:", error)
```

**Input:** URL and optional query parameters, headers, authentication,
and timeout.

**Logic:** Send HTTP request, receive response, inspect status, parse
body.

**Output:** Response object and, where applicable, parsed JSON.

**Infrastructure use:** ServiceNow, cloud APIs, AWX, monitoring
endpoints, and internal service integrations.

Always use HTTPS, timeouts, safe credential handling, and certificate
verification. Do not disable TLS verification as a routine workaround.

**Exercises** 1. Call a public test API with GET. 2. Print status code
and response headers. 3. Extract selected JSON fields. 4. Handle timeout
and non-success HTTP status. 5. Send a POST request to a test API. 6.
Save selected response data to JSON.

## 4.3 `PyYAML` --- YAML parsing

Install:

``` bash
python -m pip install PyYAML
```

Import:

``` python
import yaml
```

  --------------------------------------------------------------------------------------
  Function                         Input             Processing        Output
  -------------------------------- ----------------- ----------------- -----------------
  `yaml.safe_load(stream)`         YAML text/file    Parses safe basic Python objects
                                   stream            YAML values       

  `yaml.safe_dump(data, stream)`   Python object and Serializes YAML   YAML text or
                                   optional stream                     written file
  --------------------------------------------------------------------------------------

**Example:**

``` python
import yaml

text = """
servers:
  - name: web01
    environment: test
  - name: db01
    environment: dev
"""

data = yaml.safe_load(text)

for server in data["servers"]:
    print(server["name"])
```

Use `safe_load` for untrusted YAML. Avoid unsafe object construction.

**Infrastructure use:** Read Ansible inventory data, configuration
files, and structured deployment settings.

**Exercises** 1. Parse a YAML inventory. 2. Validate that every server
has a name. 3. Filter servers by environment. 4. Write selected records
to another YAML file.

## 4.4 `psutil` --- System and process monitoring

Install:

``` bash
python -m pip install psutil
```

Import:

``` python
import psutil
```

  ------------------------------------------------------------------------------------------
  Function                             Input             Processing        Output
  ------------------------------------ ----------------- ----------------- -----------------
  `psutil.cpu_percent(interval=...)`   Optional sampling Measures CPU      Float
                                       interval          percentage        

  `psutil.virtual_memory()`            None              Reads memory      Named tuple
                                                         statistics        

  `psutil.disk_usage(path)`            Filesystem path   Reads disk        Named tuple
                                                         statistics        

  `psutil.net_io_counters()`           None              Reads network I/O Named tuple
                                                         counters          

  `psutil.pids()`                      None              Lists process IDs List of integers

  `psutil.process_iter(attrs=...)`     Optional          Iterates          Process objects
                                       attributes        processes         
  ------------------------------------------------------------------------------------------

**Example:**

``` python
import psutil

cpu = psutil.cpu_percent(interval=1)
memory = psutil.virtual_memory()
disk = psutil.disk_usage("/")

print("CPU:", cpu)
print("Memory:", memory.percent)
print("Disk:", disk.percent)
```

Use `disk_usage("/")` on Linux/macOS; select an appropriate existing
drive path on Windows.

**Infrastructure use:** Local health reports and process inventory.

**Exercises** 1. Print CPU usage. 2. Print total and available memory.
3. Check disk usage. 4. Identify processes above a chosen memory
threshold. 5. Save a health report to CSV.

## 4.5 `paramiko` --- SSH client automation

Install:

``` bash
python -m pip install paramiko
```

Purpose: Connect to SSH servers and execute approved remote operations.

Key concepts: - `SSHClient` - `load_system_host_keys()` -
`set_missing_host_key_policy()` - `connect()` - `exec_command()` -
Channel stdout, stderr and exit status - `close()`

Input: host, port, approved identity/credential, and command.
Processing: establish authenticated SSH session and execute command.
Output: stdout, stderr, exit status.

**Security:** Verify server host keys. Do not automatically trust
unknown host keys in production. Prefer keys or an approved secrets
mechanism over hard-coded passwords. Use a lab host.

**Exercises** 1. Connect to a disposable Linux VM. 2. Run a read-only
command such as `hostname`. 3. Capture stdout and stderr. 4. Check the
remote exit status. 5. Handle connection timeout and authentication
failure.

## 4.6 `netmiko` --- Network device CLI automation

Install:

``` bash
python -m pip install netmiko
```

Purpose: Simplify SSH connections to supported network devices.

Key concepts: - Device type and connection parameters -
`ConnectHandler` - `send_command()` - `send_config_set()` -
`disconnect()`

Input: device platform, host, credentials, and command. Processing:
connect and execute device CLI operation. Output: command text or error.

Begin with read-only commands in a lab. Configuration changes require
authorization, change control, and rollback planning.

## 4.7 `pandas` --- Tabular data analysis

Install:

``` bash
python -m pip install pandas
```

Useful functions: - `pd.read_csv()` - `pd.read_json()` - `DataFrame()` -
`.loc[]` - `.groupby()` - `.value_counts()` - `.to_csv()` -
`.to_excel()`

Input: CSV/JSON or Python records. Processing: filter, group, join,
transform. Output: DataFrame or exported report.

Infrastructure use: Large inventories, compliance reports, and incident
analysis. Learn standard `csv` first for small/simple tasks.

## 4.8 `openpyxl` --- Excel workbook automation

Install:

``` bash
python -m pip install openpyxl
```

Useful API: - `load_workbook()` - `Workbook()` - `.active` -
`.sheetnames` - `.cell()` - `.append()` - `.save()`

Input: workbook path and cell/row data. Processing: read or update
workbook. Output: workbook object and saved `.xlsx` file.

Exercise: Read a server CSV and create an Excel report with a summary
sheet.

## 4.9 `pytest` --- Testing

Install:

``` bash
python -m pip install pytest
```

Core concepts: - Test functions named `test_...` - `assert` - Fixtures -
Parametrization - Exception tests - Mocking external APIs

Input: code under test and test data. Processing: execute tests and
compare results. Output: pass/fail report.

Exercise: Test a function that classifies a server as healthy or
unhealthy.

## 4.10 `Jinja2` --- Templates

Install:

``` bash
python -m pip install Jinja2
```

Useful concepts: - `Environment` - `FileSystemLoader` - `Template` -
`.render()`

Input: template and variables. Processing: substitute values and
evaluate template expressions. Output: rendered text, configuration, or
HTML.

Infrastructure use: Generate configuration files or reports. Validate
rendered output before deploying it.

## 4.11 Cloud and configuration packages

  -------------------------------------------------------------------------------------------------------------
  Package                Install                                      Main purpose      Input → output
  ---------------------- -------------------------------------------- ----------------- -----------------------
  `boto3`                `python -m pip install boto3`                AWS SDK           AWS request → service
                                                                                        response/resource

  `azure-identity`       `python -m pip install azure-identity`       Azure             Credential
                                                                      authentication    configuration → token
                                                                                        credential

  `azure-mgmt-compute`   `python -m pip install azure-mgmt-compute`   Azure VM          Subscription/resource
                                                                      management        request → VM
                                                                                        operation/result

  `python-dotenv`        `python -m pip install python-dotenv`        Load local `.env` Environment file →
                                                                      settings          environment variables

  `pysnow`               `python -m pip install pysnow`               ServiceNow client Instance/query/record
                                                                      library           data → API
                                                                                        operation/result
  -------------------------------------------------------------------------------------------------------------

Cloud SDKs require correct identity, role permissions,
subscription/account context, and cost awareness. For ServiceNow,
compare a convenience library with the official REST API and current
platform guidance before selecting an integration approach.

------------------------------------------------------------------------

# 5. Infrastructure integration patterns

## 5.1 Python + Ansible

Typical flow:

1.  Python reads an approved inventory or request.
2.  Python validates host groups and allowed variables.
3.  Python invokes `ansible-playbook` with a controlled argument list,
    or calls AWX API.
4.  Automation runs under approved credentials.
5.  Python captures job status and logs.
6.  Python verifies the resulting state and produces a report.

Useful Python modules: `json`, `yaml`, `subprocess`, `argparse`,
`logging`, `requests`, `pathlib`.

## 5.2 Python + ServiceNow

Typical flow:

1.  Receive an approved incident/change request.
2.  Validate mandatory fields and allowed values.
3.  Map fields into the ServiceNow API schema.
4.  Authenticate using an approved integration identity.
5.  Send request with a timeout.
6.  Check HTTP status and parse the response.
7.  Capture the record identifier.
8.  Verify the record and log a safe execution summary.

Useful Python modules/packages: `requests`, `json`, `logging`,
`argparse`, `datetime`, `pytest`.

## 5.3 Python + GitHub

Typical flow:

1.  Store source code and tests in a repository.
2.  Use branches and pull requests for changes.
3.  Run tests and lint checks in CI.
4.  Store secrets in the approved CI secret store.
5.  Publish a build/report only after successful checks.

Useful tools: Git, GitHub Actions, `pytest`, `subprocess`, and
optionally GitHub APIs.

## 5.4 Python + monitoring

Typical flow:

1.  Query metrics or a health endpoint.
2.  Validate the response.
3.  Compare values with defined thresholds.
4.  Create a report or alert event.
5.  Link the event to a runbook or incident process.
6.  Verify recovery after approved remediation.

Useful modules: `requests`, `json`, `datetime`, `logging`,
`concurrent.futures`.

------------------------------------------------------------------------

# 6. How to read a function's documentation

When you see a function such as:

``` python
requests.get(url, params=None, **kwargs)
```

Ask:

-   What is `url`? Required endpoint string.
-   What is `params`? Optional query-parameter mapping.
-   What is `**kwargs`? Additional supported request options such as
    headers, authentication, and timeout.
-   What is returned? A `Response` object.
-   What can fail? Connection errors, timeouts, invalid URL, HTTP errors
    after status checking.
-   What should I inspect? `status_code`, `headers`, `text`, and
    possibly `json()`.

Use the official documentation to confirm exact behavior and supported
arguments. Function signatures and package APIs can change between
versions.

------------------------------------------------------------------------

# 7. Independent coding exercise format

For every library, complete these five tasks before reading a full
solution:

1.  **Identify:** Name the problem the library solves.
2.  **Predict:** Write down the expected input and output.
3.  **Implement:** Create a small program from a blank file.
4.  **Break:** Test missing input, invalid data, permission failure, and
    timeout where applicable.
5.  **Explain:** Describe each function call and its return value.

## Example challenge: server inventory validator

**Input file:** `servers.json`

``` json
[
  {"name": "web01", "environment": "prod", "status": "running"},
  {"name": "db01", "environment": "dev", "status": "stopped"}
]
```

**Requirements:** - Read the JSON file. - Confirm the top-level data is
a list. - Confirm each record has `name`, `environment`, and `status`. -
Find duplicate server names. - Count servers by environment. - Identify
stopped servers. - Write a summary JSON report. - Log validation errors.

**Libraries to use:** `pathlib`, `json`, `collections`, `logging`,
`argparse`.

**Do not copy a solution.** Build it in small steps and test each step.

------------------------------------------------------------------------

# 8. Suggested learning order for infrastructure automation

  -----------------------------------------------------------------------
  Stage                   Modules/packages        Target outcome
  ----------------------- ----------------------- -----------------------
  1                       `os`, `sys`, `pathlib`, Filesystem and runtime
                          `shutil`                scripts

  2                       `json`, `csv`,          Inventory and reporting
                          `datetime`, `logging`   

  3                       `argparse`,             Reusable system and
                          `subprocess`, `socket`  network tools

  4                       `requests`, `PyYAML`    REST API and
                                                  configuration
                                                  automation

  5                       `psutil`, `pytest`,     Monitoring, testing and
                          `Jinja2`                templating

  6                       `concurrent.futures`,   Controlled concurrent
                          `asyncio`               checks

  7                       `paramiko`, `netmiko`   Authorized remote
                                                  administration

  8                       `boto3`, Azure SDK,     Platform integrations
                          ServiceNow APIs         
  -----------------------------------------------------------------------

With 30 minutes a day, learn one module at a time. For a small module,
spend one or two sessions; for a package such as `requests`,
`subprocess`, or `psutil`, spend several sessions and complete a
project.

------------------------------------------------------------------------

# 9. Safety and production-readiness rules

-   Use a virtual environment and pin/test dependencies for projects.
-   Read package documentation and check supported Python versions.
-   Never hard-code credentials or commit `.env` files.
-   Verify TLS certificates for HTTPS.
-   Set network and process timeouts.
-   Validate external data before using it.
-   Avoid shell command construction from untrusted input.
-   Use least privilege and explicit authorization.
-   Start with read-only checks in a disposable lab.
-   Require approval for production changes.
-   Log useful context while redacting secrets.
-   Verify the actual resulting state after an operation.
-   Test failure paths, not just successful paths.

------------------------------------------------------------------------

# 10. Official documentation index

  -----------------------------------------------------------------------------------------------------------
  Library                             Official documentation
  ----------------------------------- -----------------------------------------------------------------------
  Python standard library             https://docs.python.org/3/library/

  `os`                                https://docs.python.org/3/library/os.html

  `sys`                               https://docs.python.org/3/library/sys.html

  `pathlib`                           https://docs.python.org/3/library/pathlib.html

  `shutil`                            https://docs.python.org/3/library/shutil.html

  `subprocess`                        https://docs.python.org/3/library/subprocess.html

  `json`                              https://docs.python.org/3/library/json.html

  `csv`                               https://docs.python.org/3/library/csv.html

  `datetime`                          https://docs.python.org/3/library/datetime.html

  `logging`                           https://docs.python.org/3/library/logging.html

  `argparse`                          https://docs.python.org/3/library/argparse.html

  `socket`                            https://docs.python.org/3/library/socket.html

  Requests                            https://requests.readthedocs.io/

  PyYAML                              https://pyyaml.org/wiki/PyYAMLDocumentation

  psutil                              https://psutil.readthedocs.io/

  Paramiko                            https://docs.paramiko.org/

  Netmiko                             https://ktbyers.github.io/netmiko/

  pandas                              https://pandas.pydata.org/docs/

  openpyxl                            https://openpyxl.readthedocs.io/

  pytest                              https://docs.pytest.org/

  Jinja2                              https://jinja.palletsprojects.com/

  boto3                               https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

  Azure Identity                      https://learn.microsoft.com/python/api/overview/azure/identity-readme

  python-dotenv                       https://saurabh-kumar.com/python-dotenv/

  ServiceNow Developer                https://developer.servicenow.com/
  -----------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

## Completion standard

You understand a library well enough to use it when you can:

-   Explain what problem it solves.
-   Choose the right function for a task.
-   Identify its required and optional inputs.
-   Explain its return value and side effects.
-   Handle expected errors.
-   Write a small program without copying an example.
-   Test normal and failure cases.
-   Apply it safely to an infrastructure scenario.

**The goal is not to memorize the Python library. The goal is to know
how to use it to solve a real problem.**