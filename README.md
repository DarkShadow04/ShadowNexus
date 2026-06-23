
<div align="center">🛡️ ShadowNexus v3.5
<br><br>

Self-Healing Website Management Framework for Termux

<img src="https://img.shields.io/badge/Python-3.0-blue?style=for-the-badge">
<img src="https://img.shields.io/badge/Platform-Linux-black?style=for-the-badge">
<img src="https://img.shields.io/badge/Version-v3.5-green?style=for-the-badge">
<img src="https://img.shields.io/badge/Status-Stable-success?style=for-the-badge"></div>

---

📖 Overview

ShadowNexus is a lightweight website deployment and management framework designed for Termux.

The project evolved through multiple internal releases and stability improvements before reaching the current v3.5 Stable Release.

ShadowNexus provides a centralized control matrix for:

- Website hosting
- Workspace management
- Tunnel management
- Diagnostics
- Auto-repair
- Environment recovery
- Runtime monitoring

The framework is built around reliability, allowing it to recover from missing folders, missing logs, missing dependencies and configuration issues automatically.

---

✨ Features

🖥️ Control Matrix Dashboard

- Real-time system monitoring
- Network status monitoring
- Workspace validation
- Server status tracking
- Tunnel status tracking
- Security health monitoring

🌐 Server Management

- Local HTTP server deployment
- Persistent website path storage
- Port management
- Server uptime tracking
- Runtime session tracking

☁️ Tunnel Support

- Cloudflared integration
- Public URL exposure
- Tunnel monitoring
- Status verification

🩺 System Doctor

- Dependency validation
- Folder validation
- Workspace validation
- Configuration validation
- Environment diagnostics
- Health scoring

🔧 Auto Repair Engine

Automatically restores:

- Missing folders
- Missing logs
- Missing configuration files
- Missing Python modules
- Missing Termux packages

📂 Workspace Management

- Workspace naming
- Persistent project paths
- Environment continuity

---

📁 Project Structure

ShadowNexus/

├── snx.py

└── core/

---

⚠️ Important Warning

The following components are the backbone of the framework:

snx.py

core/

Do NOT remove, rename, or modify these components unless you understand the internal workflow.

These files are responsible for:

- Auto repair
- Dashboard functionality
- Server management
- Configuration management
- Recovery operations
- System diagnostics

Removing them may prevent ShadowNexus from starting or recovering damaged components.

---

🛠 Self-Healing Recovery

ShadowNexus can automatically recreate:

config/
templates/
workspaces/
reports/
server.log

if they are missing.

This allows the framework to recover from accidental deletion of generated files and folders.

---

🔐 Security Health Notes

The Security Health indicator is currently tied to:

- Dependency availability
- Required folders
- Required files
- Configuration integrity
- Workspace Root validation

A Security Issue warning does NOT necessarily indicate a vulnerability.

It usually means one or more required components are missing or invalid.

---

📂 Workspace Root

Workspace Root is automatically used when hosting a website.

If Workspace Root is empty:

Security Health → Warning

To fix it:

1. Start the local server.
2. Provide your website directory path.
3. ShadowNexus automatically stores the path.
4. Workspace Root becomes valid.

---

🌐 Network Requirement

ShadowNexus relies on active network connectivity.

If:

- Mobile data is disabled
- Wi-Fi is disconnected
- Internet access is unavailable

the dashboard may report:

NETWORK OFFLINE

SERVER OFFLINE

TUNNEL OFFLINE

This is expected behavior.

---

📊 Current Release

ShadowNexus v3.5

Major Improvements:

- Dashboard logic fixes
- Workspace persistence
- Server persistence
- Auto-repair engine
- Startup diagnostics
- Self-healing recovery
- Improved tunnel monitoring
- Improved configuration handling
- Improved dependency recovery

---

🚀 Installation

git clone https://github.com/DarkShadow04/ShadowNexus.git

cd ShadowNexus

python snx.py

---

🔮 Future Development

Planned future releases may include:

- Security Sessions
- Security Profiles
- Security Auditing
- Environment Hardening
- Advanced Monitoring

Stay tuned for future updates.

---

👨‍💻 Author

Dark_Shadow04

Cybersecurity Researcher • Pentester • Developer

---

<div align="center">Built with Python + Termux
