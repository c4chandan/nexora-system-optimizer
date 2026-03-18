# ⚡ Nexora System Optimizer

Nexora is a modular desktop application designed for system optimization, performance monitoring, and task automation. Built using Python and CustomTkinter, it demonstrates real-world software architecture with a plugin-based system and multi-task execution engine.

---

## 🚀 Features

- 🧹 System Cleanup (temporary files, cache)
- 🎮 Game Mode Optimization
- 🌐 Internet Speed Test
- 📀 Disk Usage Analyzer
- 🧩 Plugin-Based Architecture (auto-load)
- 📊 Real-Time Task Monitoring
- ⛔ Multi-task Execution with Cancel Support
- 🖥️ Modern UI with task panels and logs

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
2. Task starts in a dedicated panel  
3. Progress updates in real-time  
4. Multiple tasks can run in parallel  
5. Tasks can be cancelled anytime  

---

## 🧠 Architecture

- Task-based execution engine  
- Plugin system with dynamic loading  
- Thread-safe UI updates  
- Modular and scalable design  

---

## 🔌 Plugin System

Nexora supports dynamic plugins:

1. Create a Python file inside `/plugins`
2. Define a `run(log, progress, cancel)` function
3. It will automatically appear in the UI

---

## 🧹 Cleanup Engine

The cleanup module handles:

- Temporary file removal  
- Cache cleanup  
- System optimization routines  

---

## ⚡ Challenges & Solutions

- Prevented UI freezing using multithreading  
- Designed task registry to avoid duplicate execution  
- Implemented modal popups for controlled task handling  
- Built plugin system for extensibility  

---

## 📦 Installation

```bash
pip install -r requirements.txt
python pro_app.py
