# LabOPS

A tool to monitor PC health, stream live diagnostics, and install software remotely across computer labs over a local network.

[!IMPORTANT]
LabOPS started as an AI-assisted prototype and is being iteratively customized, refined, and built out into a practical, purpose-driven system for managing institutional computer labs over LAN.

## 🚀 Basic Features

* **Real-Time Hardware Telemetry:** Continuously collects and streams live PC metrics—including CPU load, RAM usage, disk space, and GPU status—using `psutil`, `WMI`, and `pynvml` libraries.
* **Live Diagnostics over WebSockets:** Maintains persistent, low-latency connections between lab workstations and the central `FastAPI` server for instant updates.
* **Remote Software Deployment:** Allows administrators to push and install software packages across connected lab machines remotely over the local network.
* **Centralized Fleet Dashboard:** Displays active lab nodes, asset assignments, live health status, and maintenance ticket tracking in one place.

## 🏗️ How It Works

1. **Client Agent:** Runs quietly on each lab PC to read hardware sensors and listen for remote installation commands.
2. **Central Server (FastAPI):** Receives live WebSocket telemetry streams, calculates device health scores, and coordinates deployments.
3. **Database Layer:** Stores registered lab assets, user roles, telemetry logs, and maintenance tickets.

## 🔮 Future Features

* **Automated Ticketing:** Evaluates incoming hardware metrics and automatically raises maintenance tickets when thresholds are crossed.
* **AI-Based Recommendations:** Provides intelligent insights and suggestions based on system health reports and historical telemetry trends.
* **Enhanced Security:** Stronger protection and encrypted communication across lab computers.
* **Timed Admin Mode:** Lets users get temporary administrator rights for specific tasks.
