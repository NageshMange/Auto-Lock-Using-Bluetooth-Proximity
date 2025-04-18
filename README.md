# Auto-Lock-Using-Bluetooth-Proximity

This Python project automatically locks your Windows PC when a specific Bluetooth device (like your smartwatch or fitness band) goes out of range. It's your digital watchdog—if you're not nearby, your PC locks itself for security. 🕵️‍♂️💻

🚀 Features

- 🔍 **Scans Bluetooth devices** in real-time using `bleak`
- 🎯 Locks only when your **target device** is out of range
- 🕒 Includes a **grace period** before locking (configurable)
- 📶 Warns when the Bluetooth signal is weak
- 🔔 **Windows toast notifications** to keep you informed
- 🧠 Smart enough to avoid false positives

 
🛠️ Requirements

- Python 3.8+
- Windows 10 or higher
- A Bluetooth adapter on your PC
- Target BLE device (smartwatch, fitness band, etc.)
 Install dependencies:
   pip install bleak win10toast


📦 Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/bluetooth-screen-locker.git
   cd bluetooth-screen-locker

⚙️ Configuration
Open the script and update the following:

-TARGET_DEVICE_NAME = "ColorFit Cadet"
-TARGET_DEVICE_ADDRESS = "F7:F6:DB:64:91:E8"
-SCAN_INTERVAL = 5           
-GRACE_PERIOD = 15          
-MIN_RSSI = -70              


▶️ Running the Script

 Simply run
-python main.py


🧪 Tested On

-Windows 11 
-ColorFit Cadet smartwatch
-Python 3.11


🧠 Use Case

Ideal for:
-Preventing unauthorized access when you step away from your computer.
 Automatically locking your PC without relying on idle timers.


📝 macOS/Linux support not included due to use of Windows-specific lock API (rundll32.exe).
