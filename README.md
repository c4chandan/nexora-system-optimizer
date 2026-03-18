# ⚡ Nexora System Optimizer

A modular desktop application built with Python and CustomTkinter for system optimization, task automation, and performance monitoring.

---

## 🚀 Features

- 🧹 System Cleanup (Temp, Cache)
- 🎮 Game Mode Optimization
- 🌐 Internet Speed Test
- 📀 Disk Usage Analyzer
- 🧩 Plugin-Based Architecture
- 📊 Real-Time Task Monitoring
- ⛔ Multi-task Execution with Cancel Support

---

## 🖥️ Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Running Tasks
![Tasks](screenshots/tasks.png)

### Multiple Tasks
![Multi Tasks](screenshots/multi_tasks.png)

---

## 🎥 How It Works

1. Select a tool from the sidebar  
2. Task runs in its own panel  
3. Progress updates in real-time  
4. User can cancel tasks anytime  

---

## 🧠 Architecture

- Task-based execution system  
- Plugin architecture (auto-load)  
- Modular and scalable design  
- UI and logic separation  

---

## 🔌 Plugin System

Add new features easily:

1. Create a Python file inside `plugins/`
2. Define a `run(log, progress, cancel)` function
3. It will automatically appear in UI

---

## 🧹 Cleanup Engine

Handles:
- Temporary file removal  
- Cache cleanup  
- System optimization routines  

---

## ⚡ Challenges & Solutions

- Prevented UI freezing using threading  
- Avoided duplicate tasks using task registry  
- Designed modal popups for safe execution  

---

## 📦 Installation

```bash
pip install -r requirements.txt
python pro_app.py