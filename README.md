# Auto-Lock-Using-Bluetooth-Proximity

This Python project automatically locks your Windows PC when a specific Bluetooth device (like your smartwatch or fitness band) goes out of range. It's your digital watchdog—if you're not nearby, your PC locks itself for security. 🕵️‍♂️💻

## 🚀 Features

- 🔍 **Scans Bluetooth devices** in real-time using `bleak`
- 🎯 Locks only when your **target device** is out of range
- 🕒 Includes a **grace period** before locking (configurable)
- 📶 Warns when the Bluetooth signal is weak
- 🔔 **Windows toast notifications** to keep you informed
- 🧠 Smart enough to avoid false positives

## 🛠️ Requirements

- Python 3.8+
- Windows 10 or higher
- A Bluetooth adapter on your PC
- Target BLE device (smartwatch, fitness band, etc.)

## 📦 Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/bluetooth-screen-locker.git
   cd bluetooth-screen-locker
