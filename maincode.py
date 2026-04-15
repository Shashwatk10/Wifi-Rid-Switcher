import customtkinter as ctk
import tkinter.messagebox as messagebox
import threading
import requests
import time
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
#Built By Shashwat 
# Setting the theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

LOGIN_URL = "http://172.16.35.1:8090/login.xml" #Add your college's login page address 
CHECK_URL = "http://www.gstatic.com/generate_204"

running = False
current_rid = ""
rid_list = []
data_usage = {}

app = ctk.CTk()
app.title("WiFi RID Switcher - macOS Style")
app.geometry("1024x650")
app.minsize(800, 500)

# --------- Functions ---------
def load_rids():
    global rid_list
    if not os.path.exists("rids.txt"):
        return []
    with open("rids.txt", "r") as f: #this is your id login list
        rid_list = [line.strip() for line in f if line.strip()]
    return rid_list

def internet_working():
    try:
        r = requests.get(CHECK_URL, timeout=2)
        return r.status_code == 204
    except:
        return False

def get_signal_strength():
    try:
        t1 = time.time()
        requests.get(CHECK_URL, timeout=2)
        t2 = time.time()
        delay = t2 - t1
        if delay < 0.1:
            return "Excellent"
        elif delay < 0.3:
            return "Good"
        elif delay < 0.6:
            return "Fair"
        else:
            return "Weak"
    except:
        return "None"

def logout(rid):
    try:
        payload = {"mode": 193, "username": rid, "password": rid, "producttype": 0}
        res = requests.post(LOGIN_URL, data=payload, timeout=5)
        return "signed out" in res.text.lower()
    except:
        return False

def login(rid):
    try:
        payload = {"mode": 191, "username": rid, "password": rid, "producttype": 0}
        res = requests.post(LOGIN_URL, data=payload, timeout=5)
        return "Login successful" in res.text or "LIVE" in res.text
    except:
        return False

def get_rid_text():
    return current_rid if current_rid else 'No RID'

def auto_switch_loop():
    global running, current_rid
    rids = load_rids()
    if not rids:
        update_status("No RIDs found.")
        return

    while running:
        if internet_working() and current_rid:
            signal = get_signal_strength()
            update_status(f"✅ Connected: {get_rid_text()} | Signal: {signal}")
            simulate_data_usage(current_rid)
            log_event(f"Connected to {get_rid_text()}")
            time.sleep(4)
            continue

        update_status("⚠ Internet down. Trying RIDs...")
        switched = False
        for rid in rids:
            logout(rid)
            time.sleep(1)
            if login(rid):
                current_rid = rid
                rid_combobox.set(current_rid)
                update_status(f"🔁 Switched to {get_rid_text()}")
                log_event(f"Switched to {get_rid_text()}")
                simulate_data_usage(current_rid)
                switched = True
                break
            else:
                update_status(f"❌ Failed: {rid}")
            time.sleep(1)
        if not switched:
            update_status("❌ All RIDs failed. Retrying in 1 min...")
            log_event("All RIDs failed")
            current_rid = ""
            rid_combobox.set("Select RID")
            update_data_label()
            time.sleep(60)

def simulate_data_usage(rid):
    if not rid:
        return
    if rid not in data_usage:
        data_usage[rid] = 0
    data_usage[rid] += 0.5
    update_data_label()

def update_data_label():
    usage = data_usage.get(current_rid, 0) if current_rid else 0
    if current_rid:
        data_label.configure(text=f"Data Used: {usage:.2f} MB")
    else:
        data_label.configure(text="Not connected.")

def update_status(msg):
    status_label.configure(text=msg)

def log_event(msg):
    log_box.configure(state="normal")
    log_box.insert("end", f"{time.strftime('%H:%M:%S')} - {msg}\n")
    log_box.see("end")
    log_box.configure(state="disabled")

def start_switching():
    global running
    if running:
        return
    running = True
    threading.Thread(target=auto_switch_loop, daemon=True).start()
    update_status("▶ Started auto switching...")
    log_event("Auto switching started")

def stop_switching():
    global running, current_rid
    running = False
    update_status("■ Stopped. Not connected.")
    log_event("Stopped switching")
    current_rid = ""
    rid_combobox.set("Select RID")
    update_data_label()

def logout_button():
    global current_rid
    if current_rid:
        if logout(current_rid):
            update_status(f"⏏ Logged out {get_rid_text()}")
            log_event(f"Logged out {get_rid_text()}")
            current_rid = ""
            rid_combobox.set("Select RID")
            update_data_label()
        else:
            update_status("Logout failed")
    else:
        update_status("No active RID")

def manual_login():
    global current_rid
    rid = rid_combobox.get().strip()
    if rid:
        logout(rid)
        if login(rid):
            current_rid = rid
            rid_combobox.set(current_rid)
            update_status(f"✔ Logged in with {get_rid_text()}")
            log_event(f"Manual login: {get_rid_text()}")
            update_data_label()
        else:
            current_rid = ""
            rid_combobox.set("Select RID")
            update_data_label()
            update_status(f"❌ Failed login for {rid}. Not connected.")
    else:
        update_status("Please select a RID.")

def toggle_mode():
    current_mode = ctk.get_appearance_mode()
    if current_mode == "Light":
        ctk.set_appearance_mode("dark")
        theme_button.configure(text="🌙 Dark Mode")
    else:
        ctk.set_appearance_mode("light")
        theme_button.configure(text="☀ Light Mode")

def close_app():
    stop_switching()
    app.destroy()

# --------- GUI Layout ---------
title_label = ctk.CTkLabel(app, text="📡 WiFi RID Switcher", font=("Helvetica Neue", 24, "bold"))
title_label.pack(pady=10)

status_label = ctk.CTkLabel(app, text="Status: Idle", font=("Helvetica Neue", 14))
status_label.pack(pady=5)

current_frame = ctk.CTkFrame(app)
current_frame.pack(pady=5)

theme_button = ctk.CTkButton(app, text="🌙 Dark Mode", command=toggle_mode)
theme_button.pack(pady=5)

data_label = ctk.CTkLabel(current_frame, text="Not connected.", font=("Helvetica Neue", 13))
data_label.grid(row=0, column=0, padx=20)

rid_combobox = ctk.CTkComboBox(app, width=200, values=load_rids())
rid_combobox.pack(pady=10)
rid_combobox.set("Select RID")

manual_btn = ctk.CTkButton(app, text="🔐 Manual Login", command=manual_login)
manual_btn.pack(pady=5)

btn_frame = ctk.CTkFrame(app)
btn_frame.pack(pady=10)

ctk.CTkButton(btn_frame, text="▶ Start", command=start_switching, width=100).grid(row=0, column=0, padx=10)
ctk.CTkButton(btn_frame, text="■ Stop", command=stop_switching, width=100).grid(row=0, column=1, padx=10)
ctk.CTkButton(btn_frame, text="⏏ Logout", command=logout_button, width=100).grid(row=0, column=2, padx=10)
ctk.CTkButton(btn_frame, text="✖ Exit", command=close_app, fg_color="red", width=100).grid(row=0, column=3, padx=10)

log_box = ctk.CTkTextbox(app, width=700, height=200, font=("Consolas", 12))
log_box.pack(pady=10)
log_box.insert("end", "Log Initialized...\n")
log_box.configure(state="disabled")

app.protocol("WM_DELETE_WINDOW", close_app)

# ------- GASEOUS ORIGIN EXPLOSION HEATMAP --------
HEATMAP_ROWS = 40
HEATMAP_COLS = 80
COLORMAP = "inferno"
heatmap_data = np.zeros((HEATMAP_ROWS, HEATMAP_COLS))

heatmap_frame = ctk.CTkFrame(app, width=350, height=220)
heatmap_frame.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

fig, ax = plt.subplots(figsize=(3.3, 2.1), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=heatmap_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

def draw_heatmap():
    ax.clear()
    c = ax.imshow(
        heatmap_data,
        cmap=COLORMAP,
        interpolation='gaussian',   # smooth, glowing
        aspect='auto'
    )
    ax.axis("off")
    if ctk.get_appearance_mode() == "Dark":
        fig.patch.set_facecolor('#222')
        ax.set_facecolor('#222')
        ax.title.set_color('#f4f4f4')
    else:
        fig.patch.set_facecolor('#fff')
        ax.set_facecolor('#fff')
        ax.title.set_color('#222')
    ax.set_title("Speed Heat Map", fontsize=10)
    canvas.draw()

draw_heatmap()

def origin_explosion_frame(intensity=100, spread=8):
    """Generate a 2D Gaussian explosion at the center."""
    x0 = HEATMAP_COLS//2
    y0 = HEATMAP_ROWS//2
    y, x = np.ogrid[:HEATMAP_ROWS, :HEATMAP_COLS]
    # 2D Gaussian centered, multiplied by random intensity + random jitter for gas look
    base = np.exp(-((x-x0)**2 + (y-y0)**2)/(2*spread**2))
    base += np.random.normal(scale=0.03, size=base.shape)
    base[base < 0] = 0  # Remove negatives
    return intensity * base

def live_heatmap_update():
    global heatmap_data
    while True:
        # New origin burst (could use actual speed in place of intensity)
        burst_intensity = np.random.uniform(30, 120)
        spread = np.random.uniform(6, 12)
        burst = origin_explosion_frame(intensity=burst_intensity, spread=spread)
        # Fade existing data
        heatmap_data *= 0.88
        # Add new burst at the center
        heatmap_data += burst
        # Bound values for display
        np.clip(heatmap_data, 0, 255, out=heatmap_data)
        
        # Note: Calling canvas.draw() from a background thread can sometimes cause Tkinter to freeze. 
        # If the GUI becomes unresponsive, consider using app.after() to schedule the draw_heatmap update.
        draw_heatmap()
        time.sleep(1.8)

threading.Thread(target=live_heatmap_update, daemon=True).start()

app.mainloop()