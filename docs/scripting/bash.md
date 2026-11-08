# Bash and Shell Scripting

Bash is a command shell commonly used on Linux. Shell scripts combine command-line tools to automate file, process, and system tasks.

## Everyday shell commands

```bash
pwd                         # current directory
ls -lah                     # list files, including hidden entries
find . -type f -name '*.log'
grep -Rni 'error' ./logs
df -h                       # filesystem capacity
ip address                  # interface addresses
```

See [Linux Administration Notes](../linux-notes.md) for more command examples and troubleshooting workflows.

## A safer script structure

```bash
#!/usr/bin/env bash
set -euo pipefail

target_dir="${1:-/var/log}"

if [[ ! -d "$target_dir" ]]; then
  printf 'Directory does not exist: %s\n' "$target_dir" >&2
  exit 2
fi

find "$target_dir" -maxdepth 1 -type f -name '*.log' -print
```

Quote variable expansions to prevent unexpected word splitting and glob expansion. Use `--` before user-controlled filenames when supported by a command. Validate inputs, return meaningful exit codes, and send errors to standard error.

`set -euo pipefail` helps surface many common script errors, but it does not replace careful error handling; understand its behavior in conditionals and pipelines.

## Variables, loops, and functions

```bash
servers=(web-01 web-02 db-01)

for server in "${servers[@]}"; do
  printf 'Checking %s\n' "$server"
done

check_file() {
  local path="$1"
  [[ -r "$path" ]]
}
```

Use `local` for function variables. Prefer arrays when a value contains multiple arguments, rather than storing a command line in one string and evaluating it.

## Scheduling and logs

Use cron or a systemd timer for scheduled work. Scheduled commands should use absolute paths and define required environment values. Capture output in a log or route it to the system journal so failures can be diagnosed.

## Safe automation habits

- Inspect targets before using commands that modify or delete files.
- Use a temporary directory for practice and test with sample data.
- Avoid running scripts as root unless the operation requires it.
- Do not store passwords or tokens directly in scripts.
- Use ShellCheck to identify common quoting and portability mistakes.

## Practice project

Write a read-only health summary that reports filesystem usage, load average, and the status of a named service. Add input validation and clear error messages; do not restart services automatically.

## Further reading

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [ShellCheck](https://www.shellcheck.net/)
