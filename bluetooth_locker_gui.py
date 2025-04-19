import asyncio
import threading
import time
import subprocess
import logging
from bleak import BleakScanner
from win10toast import ToastNotifier
import tkinter as tk
from tkinter import messagebox, scrolledtext

# -------------------- Global Config --------------------
CONFIG = {
    "TARGET_DEVICE_NAME": "ColorFit Cadet",
    "TARGET_DEVICE_ADDRESS": "F7:F6:DB:64:91:E8",
    "SCAN_INTERVAL": 5,
    "GRACE_PERIOD": 15,
    "MIN_RSSI": -70
}

# -------------------- Logging Setup --------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

# -------------------- Bluetooth Monitor Class --------------------
class BluetoothLocker:
    def __init__(self, log_callback, status_callback):
        self.running = False
        self.last_seen_time = None
        self.toaster = ToastNotifier()
        self.log_callback = log_callback
        self.status_callback = status_callback

    def log(self, message):
        self.log_callback(message)
        logger.info(message)

    async def check_device(self):
        try:
            devices = await BleakScanner.discover(timeout=5.0)
            self.log("-" * 50)
            self.log("🔍 Scanning for nearby BLE devices...")
            for d in devices:
                name = d.name or "Unknown"
                self.log(f"📡 Found - Name: {name}, Address: {d.address}, RSSI: {d.rssi} dBm")
                if d.address.upper() == CONFIG["TARGET_DEVICE_ADDRESS"]:
                    self.log(f"✅ Target '{CONFIG['TARGET_DEVICE_NAME']}' found - RSSI: {d.rssi} dBm")
                    if d.rssi is not None and d.rssi < CONFIG["MIN_RSSI"]:
                        self.log(f"⚠️ Signal is weak: {d.rssi} dBm")
                    return True
            return False
        except Exception as e:
            self.log(f"❌ Scan error: {e}")
            return False

    async def monitor(self):
        self.running = True
        self.log("📲 Bluetooth proximity monitor started.")
        while self.running:
            found = await self.check_device()
            now = time.time()
            if found:
                self.last_seen_time = now
                self.status_callback("📶 Device is nearby")
            else:
                if self.last_seen_time:
                    elapsed = now - self.last_seen_time
                    remaining = int(CONFIG["GRACE_PERIOD"] - elapsed)
                    if elapsed > CONFIG["GRACE_PERIOD"]:
                        self.log("🚫 Device not found. Locking screen...")
                        self.status_callback("🔒 Locking screen...")
                        self.toaster.show_toast("Bluetooth Lock", f"{CONFIG['TARGET_DEVICE_NAME']} not found. Locking screen...", duration=5)
                        subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
                        break
                    else:
                        self.status_callback(f"⏳ Locking in {remaining} seconds if device not found")
                else:
                    self.status_callback("🚫 Device not yet detected")
            await asyncio.sleep(CONFIG["SCAN_INTERVAL"])

    def start(self):
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        asyncio.run(self.monitor())

    def stop(self):
        self.running = False
        self.log("🛑 Monitoring stopped.")

# -------------------- GUI Setup --------------------
class LockerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bluetooth Screen Locker")
        self.root.geometry("600x450")

        self.locker = BluetoothLocker(self.log, self.update_status)

        self.create_widgets()

    def create_widgets(self):
        # Configuration Inputs
        config_frame = tk.LabelFrame(self.root, text="Configuration")
        config_frame.pack(padx=10, pady=10, fill="x")

        self.entries = {}
        for idx, (key, label) in enumerate({
            "TARGET_DEVICE_NAME": "Device Name",
            "TARGET_DEVICE_ADDRESS": "MAC Address",
            "SCAN_INTERVAL": "Scan Interval (s)",
            "GRACE_PERIOD": "Grace Period (s)",
            "MIN_RSSI": "Min RSSI (dBm)"
        }.items()):
            tk.Label(config_frame, text=label).grid(row=idx, column=0, sticky="w")
            entry = tk.Entry(config_frame)
            entry.insert(0, str(CONFIG[key]))
            entry.grid(row=idx, column=1, padx=5, pady=2, sticky="ew")
            self.entries[key] = entry

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(btn_frame, text="Start Monitoring", command=self.start_monitoring)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = tk.Button(btn_frame, text="Stop", command=self.stop_monitoring)
        self.stop_btn.grid(row=0, column=1, padx=10)

        # Status
        self.status_var = tk.StringVar(value="Idle")
        tk.Label(self.root, textvariable=self.status_var, fg="blue").pack()

        # Logs
        self.log_output = scrolledtext.ScrolledText(self.root, height=10, state='disabled')
        self.log_output.pack(padx=10, pady=5, fill="both", expand=True)

    def update_status(self, msg):
        self.status_var.set(msg)

    def log(self, msg):
        self.log_output.configure(state='normal')
        self.log_output.insert(tk.END, msg + "\n")
        self.log_output.configure(state='disabled')
        self.log_output.see(tk.END)

    def start_monitoring(self):
        for key, entry in self.entries.items():
            value = entry.get()
            CONFIG[key] = int(value) if key in ["SCAN_INTERVAL", "GRACE_PERIOD", "MIN_RSSI"] else value
        self.locker.start()

    def stop_monitoring(self):
        self.locker.stop()

# -------------------- Main --------------------
if __name__ == '__main__':
    root = tk.Tk()
    app = LockerApp(root)
    root.mainloop()
