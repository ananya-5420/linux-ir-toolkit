## 🔒 Project Purpose

This project automates the process of collecting key forensic artifacts during a security incident on a Linux machine. It will help responders capture memory state, user sessions, logs, and system details, then bundles everything in a timestamped archive with hash validation for evidence integrity.



## ⚙️ Features

- 📌 Collects system and user session info
- 🔍 Captures active processes and open ports
- 🌐 Extracts login activity (`last`, `lastlog`)
- 🗃️ Copies important logs like `auth.log`, `syslog`
- 🔐 Generates `SHA256` hashes for all collected files
- 📦 Bundles everything in a `.tar.gz` archive



## 🛠️ Requirements

- Bash (default on most Linux distros)
- Core Linux tools: `ps`, `ss`, `last`, `who`, `sha256sum`, `tar`
- Root access to collect full system logs and ports

## 🚀 Usage

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/linux-ir-toolkit.git
   cd linux-ir-toolkit/scripts
   ```

2. **Clone the repository**
  ```bash
  sudo ./collect_artifacts.sh
```

3. **Find results in** ```/tmp/incident-response-YYYYMMDD_HHMMSS/```

   
