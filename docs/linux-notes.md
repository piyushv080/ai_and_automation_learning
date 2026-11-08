# Linux Administration Notes

A practical reference for everyday shell work, system administration, and troubleshooting. Commands and paths can vary by distribution and system configuration.

> **Use commands carefully.** Start with read-only checks. Commands such as `rm`, `mkfs`, partition editors, firewall changes, and service restarts can cause data loss or disconnect a remote session. Confirm the target and have a recovery plan before changing a system.

## Contents

- [Shell and files](#shell-and-files)
- [Permissions and ownership](#permissions-and-ownership)
- [Processes and services](#processes-and-services)
- [CPU and memory checks](#cpu-and-memory-checks)
- [Disks and filesystems](#disks-and-filesystems)
- [Networking](#networking)
- [Logs and scheduled work](#logs-and-scheduled-work)
- [Boot and directory layout](#boot-and-directory-layout)
- [Troubleshooting scenarios](#troubleshooting-scenarios)
- [Further reading](#further-reading)

## 1. Shell and files

Use `man command` or `command --help` to check options on the machine you are using.

| Task | Commands | Notes |
| --- | --- | --- |
| Identify the system | `uname -a`, `hostname`, `hostname -I` | Show kernel and machine details, the host name, and assigned IP addresses on many Linux distributions. |
| Navigate | `pwd`, `ls -lah`, `cd /path`, `cd ..` | Print the current path, list files including hidden entries, or change directory. |
| Read files | `cat file`, `less file`, `head -n 20 file`, `tail -n 50 file` | Use `less` for long files; press `q` to exit. |
| Copy, move, remove | `cp -i source destination`, `mv source destination`, `rm -i file` | `-i` asks before overwriting or removing. Use recursive deletion only after checking the exact path. |
| Create files and directories | `touch file`, `mkdir -p path/to/dir` | `-p` creates missing parent directories. |
| Search text and files | `grep -n "error" app.log`, `grep -Rni "pattern" ./dir`, `find . -type f -name '*.log'` | `-i` ignores case; `-v` excludes matching lines; quote wildcard patterns. |
| Redirect and combine output | `command > out.txt`, `command >> out.txt`, `command 2> errors.txt`, `command1 \| command2` | `>` replaces a file, `>>` appends, and `2>` redirects errors. |

### Archives and links

```bash
# Create and list a gzip-compressed tar archive
tar -czf backup.tar.gz ./project
tar -tzf backup.tar.gz

# Extract an archive into a chosen directory
tar -xzf backup.tar.gz -C /tmp/restore

# Create hard and symbolic links
ln original.txt hard-link.txt
ln -s /path/to/original.txt shortcut.txt
```

A hard link is another directory entry for the same file data and inode, normally within the same filesystem. A symbolic link stores a path; it can cross filesystems, but can become dangling if its target is moved or removed.

## 2. Permissions and ownership

For each file, Linux permissions are set for the owner, group, and others. Read, write, and execute have numeric values 4, 2, and 1. For a directory, execute permission allows traversal.

```bash
ls -l file
chmod u=rwx,g=rx,o= file       # symbolic form
chmod 750 file                 # owner rwx, group rx, others none
chown user:group file
chown -R user:group directory  # recursive: review the path first

# ACL: grant a named user read and traverse access
setfacl -m u:alice:rx /srv/shared
getfacl /srv/shared
```

Use `sudo` only for the specific administrative command that needs it. ACLs add access rules beyond the basic owner/group/other mode bits.

## 3. Processes and services

```bash
ps aux                         # process snapshot
pgrep -a nginx                 # find a process by name
top                            # live process and resource view; press q to quit
kill PID                       # request a process to stop
kill -TERM PID                 # graceful termination signal
kill -KILL PID                 # force termination; use only if needed
systemctl status nginx         # inspect a systemd service
sudo systemctl restart nginx   # restart it, if authorized and safe
```

Prefer the service manager for managed services. Check status and logs before restarting; a restart can interrupt users. A process ID (PID) identifies a running process. Avoid using `kill -9` as the first response because it prevents cleanup.

## 4. CPU and memory checks

| Area | Useful commands | What to look for |
| --- | --- | --- |
| Load and CPU | `uptime`, `top` | `uptime` shows load averages for 1, 5, and 15 minutes. Compare load with the number of CPU cores and inspect processes. |
| Memory and swap | `free -h`, `swapon --show` | Linux uses spare memory for cache, so the “available” column is usually more useful than “free”. |
| Disk capacity | `df -h`, `df -i`, `du -sh directory` | `df` shows filesystem capacity and inode use; `du` summarizes space used by files in a directory. |
| I/O and open files | `vmstat 1`, `iostat`, `lsof` | `iostat` may need to be installed. `lsof` lists open files and network sockets. |

High load alone does not identify a fault. Check CPU, memory pressure, disk I/O, and network symptoms together; tools such as `sar` may need to be installed and configured first.

## 5. Disks and filesystems

```bash
lsblk -f                       # block devices, filesystems, mount points
df -hT                         # mounted filesystem type and usage
findmnt                        # mounted filesystems
sudo mount /dev/sdb1 /mnt/data # mount a filesystem (verify device first)
sudo umount /mnt/data          # unmount it when no process is using it
```

`/etc/fstab` describes filesystems that should be mounted automatically. Use stable identifiers such as UUIDs where appropriate, and validate configuration before rebooting. Creating a filesystem with `mkfs` erases existing filesystem data on the selected device.

### Partition and filesystem tools

`fdisk -l` and `parted -l` can inspect partition tables. Partition edits and filesystem creation are high-impact changes: confirm the device name, backups, and maintenance plan before writing changes.

### Swap

Swap provides disk-backed memory support and is much slower than RAM. Check it with `swapon --show` or `free -h`. Appropriate swap size depends on workload, hibernation needs, and platform; fixed “twice RAM” rules are not universal.

## 6. Networking

```bash
ip address                     # interface addresses
ip route                       # routing table
ss -lntup                      # listening TCP/UDP sockets (permissions may limit details)
ping -c 4 example.com          # basic reachability check; ICMP may be filtered
dig example.com                # DNS lookup (install dnsutils/bind-utils if needed)
curl -I https://example.com    # inspect HTTP response headers
ssh -v user@host               # verbose SSH connection diagnostics
```

`ifconfig`, `route`, and `netstat` are older utilities; the `ip` and `ss` commands are preferred on most modern distributions. `tcpdump` can capture packets; use it only on networks and systems you are authorized to inspect.

### What happens when a website is requested?

1. The client resolves the domain name through DNS, using caches and DNS servers.
2. It connects to the destination IP and port. TCP is commonly used; HTTPS also negotiates TLS.
3. The browser sends an HTTP request with headers and possibly cookies.
4. The server returns an HTTP response; the browser renders the page and may request additional assets.

## 7. Logs and scheduled work

```bash
journalctl -u nginx --since today  # service logs on systemd systems
journalctl -p warning -b           # warnings and more severe since boot
tail -f /var/log/syslog            # follow a log (path varies by distro)
crontab -l                         # list current user's cron jobs
crontab -e                         # edit current user's cron jobs
```

A cron schedule has five time fields: minute, hour, day of month, month, and day of week.

```cron
# Run at 18:30 every day
30 18 * * * /usr/local/bin/report.sh
```

Use absolute paths in scheduled jobs, set needed environment variables explicitly, and send output to a log or monitoring system.

### Log rotation

`logrotate` rotates, compresses, and expires logs according to configuration, commonly under `/etc/logrotate.conf` and `/etc/logrotate.d/`. The schedule and directives depend on the system configuration.

## 8. Boot and directory layout

At a high level, firmware initializes the machine, a bootloader starts the Linux kernel, and the kernel starts the system’s init process (commonly systemd). The init system then starts configured services and reaches a target. Exact details vary by hardware and distribution.

| Path | Common purpose |
| --- | --- |
| `/etc` | System-wide configuration |
| `/home` | Regular users’ home directories |
| `/root` | Root user’s home directory |
| `/var/log` | Many system and service logs |
| `/var` | Variable data, including logs and caches |
| `/tmp` | Temporary files; contents may be cleaned automatically |
| `/usr` | Installed programs, libraries, and documentation on many systems |
| `/boot` | Bootloader files and kernel images, depending on layout |
| `/dev` | Device nodes |
| `/mnt`, `/media` | Common mount points for filesystems and removable media |

Modern systems use systemd targets rather than the traditional SysV runlevel model described in many older Linux guides.

## 9. Troubleshooting scenarios

### “Disk is full”

Check `df -h` and `df -i`. Compare with `du -xhd1 /path` (options vary). Deleted files can still use space while a process holds them open; inspect with `sudo lsof +L1`. Do not kill processes until you know their role.

### SSH connection fails

Check the hostname and route, port reachability, server-side SSH service, account permissions, key ownership and modes, and authentication logs. Use `ssh -v` to see client-side details.

### Service is unavailable

Check `systemctl status service`, recent service logs, process state, listening sockets, firewall rules, and application health. Verify the outcome after any fix.

### System is slow

Measure before changing anything: inspect load and CPU, available memory and swap, disk space and I/O, and network errors. Identify the constrained resource and affected process.

### Safe troubleshooting sequence

1. Clarify the symptom, scope, and time it began.
2. Gather read-only facts and relevant logs.
3. Form a hypothesis and check it against evidence.
4. Make one approved, reversible change at a time.
5. Verify service health and user impact; record what changed.

## 10. Further reading

- [Scenario-based Linux interview questions (GoLinuxHub)](https://www.golinuxhub.com/2018/06/scenario-based-interview-question-beginner-experience-linux.html)
- [Linux administrator interview questions (SVR Technologies)](https://svrtechnologies.com/linux-interview-questions/new-54-linux-admin-interview-questions-and-answers-pdf)
- For exact command behavior, prefer the local manual page (for example, `man find`) and documentation for your distribution.
