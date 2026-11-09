# Bash and Shell Scripting

Bash is a command shell commonly used on Linux and macOS. A shell script combines command-line tools into a repeatable workflow. The learning lab uses shell scripts for environment checks, offline validation, and linting; the examples here generalize those patterns and use placeholder data.

These notes target Bash. POSIX `sh` is a smaller standard shell with different syntax; do not assume Bash arrays or `[[ ... ]]` work in every shell.

## 1. Everyday commands and pipelines

```bash
pwd                              # current directory
ls -lah                          # list files, including hidden entries
find . -type f -name '*.log'     # search files by name
grep -Rni 'error' ./logs         # find matching text recursively
df -h                            # filesystem capacity
ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head
```

See [Linux Administration Notes](../devops/cloud/linux-notes.md) for more command examples and troubleshooting workflows.

The pipe (`|`) passes one command's standard output to the next command. Redirect with `>` to replace a file, `>>` to append, and `2>` to redirect error output. Check exit status with `$?`, or use `if command; then ...; fi` when the outcome controls the next step.

## 2. Start scripts safely

```bash
#!/usr/bin/env bash
set -euo pipefail

if (($# != 1)); then
  printf 'Usage: %s DIRECTORY\n' "$0" >&2
  exit 2
fi

target_dir=$1

if [[ ! -d "$target_dir" ]]; then
  printf 'Directory does not exist: %s\n' "$target_dir" >&2
  exit 2
fi

# Prefix relative paths so a name beginning with a dash is not parsed as an option.
case "$target_dir" in
  /*) ;;
  *) target_dir="./$target_dir" ;;
esac

find "$target_dir" -type f -name '*.log' -print
```

Quote variable expansions to prevent unexpected word splitting and wildcard expansion. Validate arguments, use meaningful exit codes, and send errors to standard error. Use `--` to end option parsing for commands that support it.

`set -euo pipefail` helps surface many common script errors, but it does not replace careful error handling. Understand its behavior in conditionals, command substitutions, and pipelines before relying on it.

## 3. Variables, arrays, conditions, and loops

```bash
report_dir="${HOME}/reports"
servers=(web-01 web-02 db-01)

for server in "${servers[@]}"; do
  if [[ "$server" == web-* ]]; then
    printf 'Web server: %s\n' "$server"
  fi
done

mkdir -p -- "$report_dir"
```

Use `${array[@]}` to preserve array elements as separate arguments. Use `[[ ... ]]` for Bash conditions and `(( ... ))` for integer arithmetic.

## 4. Functions and return codes

```bash
is_readable_file() {
  local path=$1
  [[ -f "$path" && -r "$path" ]]
}

if is_readable_file "./sample.txt"; then
  printf 'Sample file is ready\n'
else
  printf 'Sample file is missing or unreadable\n' >&2
  exit 1
fi
```

Functions return an exit status from 0 (success) to 255 (failure); they do not return arbitrary strings. Print data to standard output or set a clearly scoped variable. Use `local` for function-only values.

## 5. Files, temporary data, and reports

Use a temporary directory for intermediate output and remove only that directory when the script exits. Never build a deletion path from unchecked user input.

```bash
tmp_dir=$(mktemp -d)
cleanup() {
  rm -rf -- "$tmp_dir"
}
trap cleanup EXIT

find ./sample-data -type f -name '*.txt' -print0 |
  while IFS= read -r -d '' file; do
    printf '%s\n' "$file"
  done
```

The example expects a `sample-data` directory. NUL-delimited paths (`-print0` and `read -d ''`) safely handle spaces and unusual filename characters.

To create a tabular report, use a tool such as `awk`, Python, or `jq` where appropriate. Avoid inventing CSV escaping with `printf` when values may contain commas, quotes, or newlines.

## 6. Environment and offline validation

Before a workflow, check that required commands exist and that the project files are present. Fail early with a clear message.

```bash
require_command() {
  command -v "$1" >/dev/null 2>&1 || {
    printf 'Required command is missing: %s\n' "$1" >&2
    return 1
  }
}

require_command python3
require_command git

if [[ ! -f "requirements.txt" ]]; then
  printf 'requirements.txt is missing\n' >&2
  exit 1
fi

python3 -m pip check
```

For offline checks, validate local files and installed tool versions without downloading packages or contacting remote services. Keep setup steps separate from validation steps so a check does not unexpectedly change the environment.

## 7. Calling an API

`curl` can check an HTTP endpoint. Include connection and total timeouts, fail on HTTP error responses, and avoid printing authorization headers or tokens.

```bash
health_url="${SERVICE_HEALTH_URL:-https://api.example.test/health}"
curl --fail --silent --show-error \
  --connect-timeout 5 \
  --max-time 15 \
  "$health_url"
```

Use `jq` to parse JSON when installed:

```bash
curl --fail --silent --show-error --max-time 15 "$health_url" |
  jq -r '.status // "unknown"'
```

Do not put secrets in command-line arguments, shell history, or output logs. Prefer an approved credential helper or secret store. Verify that a command's response is safe to print before sending it to shared logs.

## 8. Logging and scheduling

Use consistent messages and send errors to standard error. Scheduled jobs should use absolute paths, explicitly set required environment values, and capture output in an approved log location.

```bash
log_info() { printf '%s INFO %s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$*"; }
log_error() { printf '%s ERROR %s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$*" >&2; }

log_info "Starting read-only report"
```

Cron and systemd timers are common scheduling options on Linux. See [Linux Administration Notes](../devops/cloud/linux-notes.md#7-logs-and-scheduled-work) for cron basics.

## 9. Linting and debugging

```bash
bash -n ./script.sh       # syntax check without running the script
shellcheck ./script.sh    # static checks, if ShellCheck is installed
bash -x ./script.sh arg   # trace commands while debugging; avoid with secrets
```

Use sample data and a disposable directory for practice. Check `bash -x` output before sharing it; tracing can expose environment values and command arguments.

## 10. Safe automation habits

- Inspect targets before using commands that modify or delete files.
- Use a temporary directory for practice and test with sample data.
- Avoid running scripts as root unless the operation requires it.
- Keep credentials out of scripts and logs.
- Avoid `eval`; pass arguments as arrays instead of assembling commands as strings.
- Use ShellCheck to identify common quoting and portability mistakes.

## Practice project: local health summary

Create a read-only report that displays filesystem usage, load average, and the status of one named service. Validate the service name, handle unavailable commands, and write output to a temporary file before saving a final report. Do not add automatic restarts until the script has tests, authorization checks, and an explicit review step.

## Further reading

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [ShellCheck](https://www.shellcheck.net/)
