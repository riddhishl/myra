import re
import time
import argparse
import requests as req
import json
import threading
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

# Initialize the LED matrix device
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90, rotate=2, mode="RGB")
print("Created device")

msg = "Display Starting..."
print(msg)
show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)
time.sleep(1)

# Global variable to control display
display_active = True

def monitor_file():
    """
    Thread function to monitor /home/alpha/hacked.txt file.
    If the content of the file is 'true', stops the LED display.
    """
    global display_active
    file_path = "/home/alpha/hacked.txt"
    while True:
        try:
            with open(file_path, 'r') as file:
                content = file.read().strip().lower()
                if content == "true":
                    display_active = False
                else:
                    display_active = True
        except FileNotFoundError:
            print(f"File {file_path} not found. Retrying...")
        time.sleep(1)  # Check the file periodically

# Start the file monitoring thread
file_monitor_thread = threading.Thread(target=monitor_file, daemon=True)
file_monitor_thread.start()

# Main loop for the LED matrix display
while True:
    print(display_active)
    if display_active:
        try:
            response = req.get("http://172.16.17.100/stock/getInfo.php?")
            dict = response.json()
            print(dict)
            for l in dict:
                if not display_active:  # Recheck display status
                    break

                msg = ""
                Company = str(l["company"])
                Price = str(l["price"])
                Change_per = str(l["change_per"])
                Value = str(l["value"])

                msg = f"{Company}: {Price} Change %: {Change_per} Value: {Value}"
                show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Display halted due to hacking simulation.")
        time.sleep(1)  # Avoid busy-waiting
