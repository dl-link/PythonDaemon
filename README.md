# Python Script Daemon

A lightweight Python-based daemon script to automatically restart a Python program if it crashes.  
Useful for ensuring important scripts run reliably with retry and delay mechanisms.

## 🔧 Features

- Automatically restart a Python script if it fails
- Configurable retry attempts and retry interval
- Supports custom Python interpreter (e.g. `python3`, `python3.11`)
- Logs each attempt with timestamps
- Cross-platform compatible (Windows, Linux, macOS)

## 📄 Usage

```bash
python daemon.py your_script.py [--retry RETRY] [--interval SECONDS] [--python PYTHON_EXEC]
```

### Required Argument

- `your_script.py` — the target Python script to run and monitor.

### Optional Arguments

| Argument        | Description                                             | Default   |
|-----------------|---------------------------------------------------------|-----------|
| `--retry`       | Number of retry attempts (use `0` for infinite retries) | `3`       |
| `--interval`    | Time in seconds to wait before restarting               | `30`      |
| `--python`      | Python interpreter to use (e.g. `python3`, `python3.11`) | `python`  |

### Example

```bash
python daemon.py my_script.py --retry 5 --interval 60 --python python3
```

This will:
- Run `my_script.py` using `python3`
- Retry up to 5 times if it crashes
- Wait 60 seconds between each retry

## 🖥️ Windows Setup

1. Save `daemon.py` in your working directory.
2. Create a batch file (e.g. `run_script.bat`):

```bat
@echo off
python daemon.py my_script.py --retry 3 --interval 30
```

3. Use Windows Task Scheduler to:
   - Launch this batch file at boot
   - Or run it at a scheduled time

## 🐧 Linux/macOS Setup

You can run the daemon directly or register it as a service.

### Cron Example

```cron
@reboot /usr/bin/python3 /home/username/daemon.py /home/username/my_script.py --retry 0
```

### Systemd Service Example

Create a file: `/etc/systemd/system/my_script_daemon.service`

```ini
[Unit]
Description=My Python Script Daemon
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/username/daemon.py /home/username/my_script.py --retry 0
Restart=always
User=yourusername
WorkingDirectory=/home/username
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Then run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable my_script_daemon
sudo systemctl start my_script_daemon
```

## ✅ Exit Behavior

- If the script finishes normally (exit code `0`), the daemon stops.
- If the script crashes (non-zero exit code), the daemon will wait and restart as configured.
- If the retry limit is reached (non-zero and `--retry` > 0), the daemon exits with a log.

