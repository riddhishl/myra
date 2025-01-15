import RPi.GPIO as GPIO
import time
import threading
import requests
import paho.mqtt.client as mqtt

# MQTT Setup
BROKER_ADDRESS = "172.16.17.201"
MQTT_TOPIC = "/light/button2"
CONTROL_TOPIC = "villa1/control"

# API and File Path
BALANCE_URL = "http://172.16.17.216:3000/user/19"
FILE_PATH = "/home/alpha/electricity_reading.txt"

# Global Variables
balance = 0
light_on = False

def fetch_balance():
    global balance
    global light_on
    while True:
        try:
            response = requests.get(BALANCE_URL)
            if response.status_code == 200:
                data = response.json()
                balance = data.get('amount', 0)
                print(f"Balance: {balance}")  # Debugging: print balance to console
                print("Light_on: ",light_on)
        except Exception as e:
            print(f"Error fetching balance: {e}")
        time.sleep(5)

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global light_on
    payload = msg.payload.decode('utf-8')
    print(f"MQTT message received: {payload}")  # Debugging: print received message
    if payload.lower() == "true":
        light_on = True
    elif payload.lower() == "false":
        light_on = False

def mqtt_client_setup():
    client = mqtt.Client()
    #client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_ADDRESS)
    return client

def relay_control():
    global balance, light_on
    while True:
        if light_on and balance > 0:
            mqtt_client.publish(CONTROL_TOPIC, "1")
            update_units_consumed()
        else:
            mqtt_client.publish(CONTROL_TOPIC, "0")
        time.sleep(3)  # Small delay to avoid high CPU load

def update_units_consumed():
    global balance
    # This function increases the units consumed by 1 for every 8 seconds the light is on.
    start_time = time.time()
    while light_on and balance > 0:
        if time.time() - start_time >= 8:
            start_time = time.time()  # Reset the start time
            try:
                with open(FILE_PATH, 'r+') as file:
                    units_consumed = int(file.read().strip()) + 1
                    file.seek(0)
                    file.write(str(units_consumed))
                    file.truncate()
                    print(f"Units Consumed Updated: {units_consumed}")  # Debugging
            except FileNotFoundError:
                with open(FILE_PATH, 'w') as file:
                    file.write("1")
            except ValueError:
                # Handle case where the file is empty or has invalid content
                with open(FILE_PATH, 'w') as file:
                    file.write("1")

# Start balance fetching in a separate thread
balance_thread = threading.Thread(target=fetch_balance, daemon=True)
balance_thread.start()

# Start MQTT client in a separate thread
mqtt_client = mqtt_client_setup()
mqtt_thread = threading.Thread(target=mqtt_client.loop_forever, daemon=True)
mqtt_thread.start()

# Main loop for relay control
relay_control()
