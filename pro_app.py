import customtkinter as ctk
import threading
import os
import importlib
import psutil
import ultimate_cleanup as core

# =========================
# SETTINGS
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Nexora System Optimizer")
app.geometry("1200x760")

# =========================
# STATE
# =========================
active_tasks = {}

# =========================
# LOG
# =========================
def log(msg):
    log_box.insert("end", msg + "\n")
    log_box.see("end")

core.log = log

# =========================
# SYSTEM STATS (LIVE)
# =========================
def update_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    cpu_label.configure(text=f"CPU: {cpu}%")
    ram_label.configure(text=f"RAM: {ram}%")

    app.after(1000, update_stats)

# =========================
# PLUGIN LOADER
# =========================
def load_plugins():
    plugins = {}

    if not os.path.exists("plugins"):
        return plugins

    for file in os.listdir("plugins"):
        if file.endswith(".py") and file != "__init__.py":
            name = file[:-3]
            try:
                module = importlib.import_module(f"plugins.{name}")
                plugins[name] = module
            except Exception as e:
                log(f"Plugin error: {name} → {e}")

    return plugins

plugins = load_plugins()

# =========================
# TASK CARD
# =========================
def create_task_card(name, func, button=None):

    cancel_flag = {"stop": False}

    card = ctk.CTkFrame(task_container, corner_radius=10)
    card.pack(fill="x", padx=10, pady=6)

    ctk.CTkLabel(card, text=name, font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10, pady=5)

    progress = ctk.CTkProgressBar(card)
    progress.pack(fill="x", padx=10)
    progress.set(0)

    status = ctk.CTkLabel(card, text="Running...", text_color="orange")
    status.pack(anchor="w", padx=10)

    def cancel():
        cancel_flag["stop"] = True
        status.configure(text="Cancelled", text_color="red")

    ctk.CTkButton(card, text="Cancel", width=80, command=cancel).pack(padx=10, pady=5)

    def run():
        try:
            func(
                log,
                lambda v: progress.set(v),
                lambda: cancel_flag["stop"]
            )

            if not cancel_flag["stop"]:
                status.configure(text="Completed", text_color="green")

        except Exception as e:
            status.configure(text="Error", text_color="red")
            log(f"{name} error: {e}")

        active_tasks.pop(name, None)

        if button:
            button.configure(state="normal")

    threading.Thread(target=run, daemon=True).start()

# =========================
# POPUP
# =========================
def show_popup(name, func, button):
    popup = ctk.CTkToplevel(app)
    popup.title("Task Running")
    popup.geometry("320x160")
    popup.grab_set()

    ctk.CTkLabel(popup, text=f"{name} is already running.\nRun another?", justify="center").pack(pady=20)

    def yes():
        create_task_card(name + " (New)", func, button)
        popup.destroy()

    def no():
        popup.destroy()

    ctk.CTkButton(popup, text="Continue", command=yes).pack(pady=5)
    ctk.CTkButton(popup, text="Cancel", command=no).pack(pady=5)

# =========================
# START TASK
# =========================
def start_task(name, func, button):

    if name in active_tasks:
        show_popup(name, func, button)
        return

    active_tasks[name] = True
    button.configure(state="disabled")

    create_task_card(name, func, button)

# =========================
# WRAP CORE
# =========================
def wrap_core(func):
    return lambda log, progress, cancel: func()

# =========================
# UI
# =========================

# HEADER
header = ctk.CTkFrame(app, height=60)
header.pack(fill="x")

ctk.CTkLabel(header, text="⚡ Nexora System Optimizer", font=("Segoe UI", 20, "bold")).pack(side="left", padx=20)

cpu_label = ctk.CTkLabel(header, text="CPU: 0%")
cpu_label.pack(side="right", padx=10)

ram_label = ctk.CTkLabel(header, text="RAM: 0%")
ram_label.pack(side="right", padx=10)

# SIDEBAR
sidebar = ctk.CTkFrame(app, width=240)
sidebar.pack(side="left", fill="y")

# MAIN
main = ctk.CTkFrame(app)
main.pack(side="right", fill="both", expand=True)

task_container = ctk.CTkFrame(main)
task_container.pack(fill="x", pady=10)

log_box = ctk.CTkTextbox(main)
log_box.pack(fill="both", expand=True, padx=10, pady=10)

# =========================
# BUTTON HELPER
# =========================
def add_button(text, func):
    btn = ctk.CTkButton(
        sidebar,
        text=text,
        command=lambda: start_task(text, func, btn)
    )
    btn.pack(pady=6, padx=10, fill="x")

# CORE
add_button("🧹 Basic Cleanup", wrap_core(core.basic_cleanup))
add_button("🛠 Full Cleanup", wrap_core(core.full_cleanup))
add_button("🎮 Game Mode", wrap_core(core.game_mode))

# FALLBACK TASKS
def speed_test(log, progress, cancel):
    import speedtest
    log("Running speed test...")
    st = speedtest.Speedtest()
    st.get_best_server()

    if cancel(): return
    progress(0.5)

    d = st.download() / 1_000_000

    if cancel(): return
    progress(0.8)

    u = st.upload() / 1_000_000

    progress(1.0)
    log(f"Download: {d:.2f} Mbps")
    log(f"Upload: {u:.2f} Mbps")

def disk_usage(log, progress, cancel):
    log("Scanning disks...")
    progress(0.5)

    for p in psutil.disk_partitions():
        if cancel(): return
        try:
            usage = psutil.disk_usage(p.mountpoint)
            log(f"{p.device}: {usage.percent}%")
        except:
            pass

    progress(1.0)

# PLUGINS OR DEFAULT
if plugins:
    for name, plugin in plugins.items():
        add_button(f"🔌 {name.replace('_',' ').title()}", plugin.run)
else:
    add_button("🌐 Speed Test", speed_test)
    add_button("📀 Disk Usage", disk_usage)

ctk.CTkButton(sidebar, text="❌ Exit", command=app.quit).pack(pady=20)

# START
log("=== Nexora Started (Production Build) ===")
update_stats()
app.mainloop()