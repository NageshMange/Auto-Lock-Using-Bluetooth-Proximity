# Importing necessary libraries
import asyncio  # For asynchronous operations
import subprocess  # To run system commands (like locking the screen)
import logging  # For logging events and info
import time  # To handle timing operations
from bleak import BleakScanner  # BLE scanner library for Bluetooth devices
from win10toast import ToastNotifier  # For Windows toast notifications

# Configuration for the target device and behavior
TARGET_DEVICE_NAME = "ColorFit Cadet"  # Friendly name of the device
TARGET_DEVICE_ADDRESS = "F7:F6:DB:64:91:E8"  # MAC address of the target Bluetooth device
SCAN_INTERVAL = 5  # How often to scan for the device (in seconds)
GRACE_PERIOD = 15  # Time to wait before locking if device is lost (in seconds)
MIN_RSSI = -70  # Minimum acceptable signal strength (RSSI)

# Logging setup to show time, log level, and message
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create a toast notification object
toaster = ToastNotifier()
last_seen_time = None  # Stores last time the target device was seen

# Function to scan for BLE devices and check if the target is nearby
async def check_device():
    try:
        devices = await BleakScanner.discover(timeout=5.0)  # Scan for 5 seconds
        logging.info("-" * 60)
        logging.info("🔍 Scanning for nearby BLE devices...")
        target_found = False

        for d in devices:
            name = d.name or "Unknown"  # Fallback to "Unknown" if name is None
            logging.info(f"📡 Found - Name: {name}, Address: {d.address}, RSSI: {d.rssi} dBm")

            # Check if this is the target device
            if d.address.upper() == TARGET_DEVICE_ADDRESS:
                logging.info(f"✅ Target device '{TARGET_DEVICE_NAME}' detected - RSSI: {d.rssi} dBm")
                
                # Check if the signal is weak
                if d.rssi is not None and d.rssi < MIN_RSSI:
                    logging.warning(f"⚠️ Signal is weak: {d.rssi} dBm")
                target_found = True  # Device found

        return target_found
    except Exception as e:
        logging.error(f"❌ Scan error: {e}")
        return False  # In case of error, return False

# Function to continuously monitor the Bluetooth connection
async def monitor_bluetooth():
    global last_seen_time
    logging.info("📲 Starting Bluetooth proximity monitor...")

    while True:
        found = await check_device()  # Perform device scan
        current_time = time.time()

        if found:
            last_seen_time = current_time  # Update last seen time
            logging.info("📶 Device is nearby.")
        else:
            if last_seen_time:
                time_elapsed = current_time - last_seen_time  # Time since last seen
                time_left = int(GRACE_PERIOD - time_elapsed)  # Time left before locking

                # If the device has been gone longer than grace period
                if time_elapsed > GRACE_PERIOD:
                    logging.warning("🚫 Device not connected. Locking screen...")
                    toaster.show_toast("Bluetooth Lock", f"{TARGET_DEVICE_NAME} not found. Locking screen...", duration=5)
                    try:
                        subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)  # Lock the screen
                    except Exception as e:
                        logging.error(f"❌ Failed to lock workstation: {e}")
                    break  # Exit the loop after locking
                else:
                    logging.warning(f"⏳ Device not seen. Locking in {time_left} seconds if still not found.")
            else:
                logging.warning("🚫 Device not detected yet. Waiting for first connection...")

        await asyncio.sleep(SCAN_INTERVAL)  # Wait before scanning again

# Main block to start the monitoring process
if __name__ == "__main__":
    try:
        asyncio.run(monitor_bluetooth())  # Start the async monitor
    except KeyboardInterrupt:
        logging.info("🛑 Monitoring stopped by user.")  # Handle manual stop
    except Exception as e:
        logging.error(f"💥 Fatal error: {e}")  # Handle unexpected crash
