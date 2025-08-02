import argparse
import subprocess
import time
import os
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def main():
    parser = argparse.ArgumentParser(
        prog='Python daemon',
        description='Restart a Python script automatically if it crashes.'
    )
    parser.add_argument('file', type=str, help='Python script to run')
    parser.add_argument('--retry', type=int, default=3, help='Number of retry attempts (0 = infinite)')
    parser.add_argument('--interval', type=int, default=30, help='Wait time (in seconds) between retries')
    parser.add_argument('--python', type=str, default='python', help='Python interpreter to use')

    args = parser.parse_args()
    script = args.file
    retry_limit = args.retry
    retry_interval = args.interval
    python_exec = args.python

    if not os.path.isfile(script):
        raise FileNotFoundError(f"Script '{script}' not found.")

    count = 0
    while retry_limit == 0 or count < retry_limit:
        count += 1
        log(f"Starting attempt #{count} - running '{script}'...")
        result = subprocess.run([python_exec, script])

        if result.returncode == 0:
            log(f"Script '{script}' exited normally.")
            break
        else:
            log(f"Script failed with return code {result.returncode}. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    else:
        log("Max retry limit reached. Exiting.")

if __name__ == '__main__':
    main()
