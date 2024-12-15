import subprocess
import re

def run_command(command):
    try:
        return subprocess.check_output(command, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return ""

def parse_brightness(output):
    match = re.search(r"current value\s*=\s*(\d+)", output)
    return int(match.group(1)) if match else 0