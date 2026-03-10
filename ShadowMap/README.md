# ShadowMap 🌑📍

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/shanmkuu/Automated-Recon-Framework/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/shanmkuu/Automated-Recon-Framework.svg)](https://github.com/shanmkuu/Automated-Recon-Framework/issues)

> A modular, lightweight, and blazingly fast reconnaissance framework for automated penetration testing and Bug Bounty hunting.

---

## 🚫 Legal Disclaimer

**ShadowMap** is created for educational purposes and ethical penetration testing. 
The developer assumes **no liability** and is not responsible for any misuse or damage caused by this program. 
You must have explicit permission from the system owner before running this tool against any assets. Do not use ShadowMap against systems you do not own or have permission to test.

---

## 🚀 Features

- **Modular Architecture:** Cleanly separated phases (`Enumerator`, `HostChecker`, `PortScanner`, `Reporter`).
- **Rapid Subdomain Discovery:** Uses `crt.sh` and `Sublist3r` to quickly build a domain profile.
- **Asynchronous Host Checking:** Uses the powerful `httpx` async library to concurrently ping hosts and extract server headers and page titles.
- **Fast Port Scanning:** Wraps `nmap` for lightning-fast top 100 ports scans against discovered alive hosts.
- **Structured Output:** Automatically generates a comprehensive `scan_results.json` and an elegant `summary.md` in the `reports/{domain}/` directory.

---

## ⚙️ Installation

### Prerequisites

Ensure you have the following installed on your system:
- **Python 3.8+**
- **Nmap**: Network exploration tool and security / port scanner.
  - *Ubuntu/Debian:* `sudo apt-get install nmap`
  - *MacOS:* `brew install nmap`
  - *Windows:* Download from [nmap.org](https://nmap.org/download.html)
- **Sublist3r**: Fast subdomains enumeration tool.
  - *Installation:* `pip install sublist3r` or via package manager.

### Setup

Clone the repository and install the Python dependencies:

```bash
git clone https://github.com/shanmkuu/Automated-Recon-Framework.git
cd Automated-Recon-Framework/ShadowMap
pip install -r requirements.txt
```

---

## 🎯 Usage

To start a reconnaissance scan, simply provide the target domain to the main script:

```bash
python main.py example.com
```

### Advanced Options

You can control the concurrency of the asynchronous HTTP alive-host checking phase:

```bash
python main.py example.com --concurrency 100
```

### Example Output

```text
  ___ _               _               __  __           
 / __| |_  __ _ __| |_____ __ _|  \/  |__ _ _ __  
 \__ \ ' \/ _` / _` / _ \ V  V / |\/| / _` | '_ \ 
 |___/_||_\__,_\__,_\___/\_/\_/|_|  |_\__,_| .__/ 
                                           |_|    
    Modular Reconnaissance Framework (v1.0)
    
2026-03-10 11:45:00 - Starting reconnaissance on target: example.com
2026-03-10 11:45:00 - --- [ Phase 1: Subdomain Enumeration ] ---
[*] Enumerating subdomains for example.com...
...
```

---

## 📁 Project Structure

```text
ShadowMap/
├── main.py
├── requirements.txt
├── README.md
├── shadowmap/
│   ├── __init__.py
│   ├── enumerator.py       # crt.sh & Sublist3r integration
│   ├── host_checker.py     # async httpx alive checking
│   └── port_scanner.py     # nmap wrapper and XML parsing
└── utils/
    ├── __init__.py
    └── reporter.py         # JSON and Modular Markdown reporting
```

---

## 💡 Visual Reconnaissance
ShadowMap generates an `alive_urls.txt` file within the `reports/{domain}/` directory. This acts as a seamless handoff point for advanced web screenshotting tools (such as Aquatone, EyeWitness, or an automated Antigravity Browser Agent) to capture the visual footprint of the discovered infrastructure.

---

**Made with 🖤 by shanmkuu.**
