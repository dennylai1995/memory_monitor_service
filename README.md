
# Memory monitor service
A systemd service to periodically (default: 2Hz) check system memory usage and record top 10 memory consumers (processes) & output of `free` command when a memory threshold (default: 80%) is exceeded.

## Dependencies
- Linux distro
- `systemd`
- `python3`
- `free`
- `grep`
- `echo`
- `ps`
- `head`
- `tail`

## Tested environment
- Ubuntu 20.04.6 LTS
- Raspbian GNU/Linux 11 (bullseye)

## Default settings
1. script folder: `/home/memory_monitor_scripts`
2. log folder: `/home/memory_monitor_scripts/log`
3. memory threshold(%): 80
4. prob (checking) interval (s): 0.5

## How to deploy
- just run `bash deploy.sh`
- may need root privilege (due to `sudo`)

## How to debug
1. journalctl -r -t memory_monitor  (-r means reverse, -t means tag)
2. log file in `home/memory_monitor_scripts/log`

## About log size
- journald will limit the log size to 15% of disk capacity or 4GB
(https://unix.stackexchange.com/questions/576999/will-a-systemd-service-automatically-manage-its-logs-do-log-rotation-etc)
- logs in `home/memory_monitor_scripts/log` will rotate automatically (10MB per file, max 5 files)