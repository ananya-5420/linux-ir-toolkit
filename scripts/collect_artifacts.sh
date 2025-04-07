#!/bin/bash

# Check for root privileges
if [[ "$EUID" -ne 0 ]]; then
  echo "This script must be run as root!"
  exit 1
fi

# Timestamp and output directory
timestamp=$(date +"%Y%m%d_%H%M%S")
output_dir="/tmp/incident-response-$timestamp"
mkdir -p "$output_dir"

echo "[*] Collecting system info..."
uname -a > "$output_dir/system-info.txt"
uptime >> "$output_dir/system-info.txt"

echo "[*] Collecting process list..."
ps aux > "$output_dir/process-list.txt"

echo "[*] Collecting logged-in users..."
who > "$output_dir/logged-in-users.txt"
w >> "$output_dir/logged-in-users.txt"

echo "[*] Done. Output saved in $output_dir"

echo "[*] Collecting open network ports..."
ss -tulnp > "$output_dir/open-ports.txt" 2>/dev/null || netstat -tulnp > "$output_dir/open-ports.txt"

echo "[*] Collecting last login sessions..."
last > "$output_dir/last-logins.txt"
lastlog > "$output_dir/lastlog.txt"

echo "[*] Collecting log files..."
mkdir "$output_dir/logs"
cp /var/log/auth.log "$output_dir/logs/" 2>/dev/null
cp /var/log/syslog "$output_dir/logs/" 2>/dev/null

echo "[*] Generating SHA256 hashes..."
cd "$output_dir"
find . -type f ! -name "hashes.txt" -exec sha256sum "{}" \; > hashes.txt
cd - > /dev/null

echo "[*] Creating compressed archive..."
tarball="/tmp/$(basename "$output_dir").tar.gz"
tar -czf "$tarball" -C /tmp "$(basename "$output_dir")"
echo "[+] Archive created: $tarball"
