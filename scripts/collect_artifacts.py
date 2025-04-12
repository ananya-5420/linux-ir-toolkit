import os
import shutil
import subprocess
import hashlib
import tarfile
from datetime import datetime
from pathlib import Path

# Check for root privileges
if os.geteuid() != 0:
    print("This script must be run as root!")
    exit(1)

# Timestamp and output directory
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = Path(f"/tmp/incident-response-{timestamp}")
output_dir.mkdir(parents=True, exist_ok=True)

print("[*] Collecting system info...")
with open(output_dir / "system-info.txt", "w") as f:
    f.write(subprocess.getoutput("uname -a") + "\n")
    f.write(subprocess.getoutput("uptime") + "\n")

print("[*] Collecting process list...")
with open(output_dir / "process-list.txt", "w") as f:
    f.write(subprocess.getoutput("ps aux"))

print("[*] Collecting logged-in users...")
with open(output_dir / "logged-in-users.txt", "w") as f:
    f.write(subprocess.getoutput("who") + "\n")
    f.write(subprocess.getoutput("w"))

print("[*] Collecting open network ports...")
ports_output = subprocess.getoutput("ss -tulnp 2>/dev/null") or subprocess.getoutput("netstat -tulnp")
with open(output_dir / "open-ports.txt", "w") as f:
    f.write(ports_output)

print("[*] Collecting last login sessions...")
with open(output_dir / "last-logins.txt", "w") as f:
    f.write(subprocess.getoutput("last"))
with open(output_dir / "lastlog.txt", "w") as f:
    f.write(subprocess.getoutput("lastlog"))

print("[*] Collecting log files...")
logs_dir = output_dir / "logs"
logs_dir.mkdir(exist_ok=True)

for log_file in ["/var/log/auth.log", "/var/log/syslog"]:
    try:
        shutil.copy(log_file, logs_dir)
    except FileNotFoundError:
        pass

print("[*] Generating SHA256 hashes...")
hashes_file = output_dir / "hashes.txt"
with open(hashes_file, "w") as hf:
    for filepath in output_dir.rglob("*"):
        if filepath.is_file() and filepath.name != "hashes.txt":
            with open(filepath, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            relative_path = filepath.relative_to(output_dir)
            hf.write(f"{file_hash}  {relative_path}\n")

print("[*] Creating compressed archive...")
tarball_path = Path("/tmp") / f"{output_dir.name}.tar.gz"
with tarfile.open(tarball_path, "w:gz") as tar:
    tar.add(output_dir, arcname=output_dir.name)

print(f"[+] Archive created: {tarball_path}")
