import uasyncio as asyncio
from umqtt.simple import MQTTClient
import umqtt.config

from logger import Logger

# ---- Global variables ----
import shared_variables as var

# Constants for MQTT Topics
MQTT_TOPIC = 'test'

# MQTT Parameters
MQTT_SERVER = umqtt.config.mqtt_server
MQTT_PORT = 1883
MQTT_USER = umqtt.config.mqtt_username
MQTT_PASSWORD = umqtt.config.mqtt_password
MQTT_CLIENT_ID = b"raspberrypi_pico2w"
MQTT_KEEPALIVE = 7200
MQTT_SSL = False   # set to False if using local Mosquitto MQTT broker
MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}

async def mqtt_task(period = 1.0):
    #Init
    log = Logger("mqtt", debug_enabled=True)

    try:
        client = MQTTClient(client_id=MQTT_CLIENT_ID,
                            server=MQTT_SERVER,
                            port=MQTT_PORT,
                            user=MQTT_USER,
                            password=MQTT_PASSWORD,
                            keepalive=MQTT_KEEPALIVE,
                            ssl=MQTT_SSL,
                            ssl_params=MQTT_SSL_PARAMS)
        client.connect()

    except Exception as e:
        log.error('Error connecting to MQTT:', e)
        raise  # Re-raise the exception to see the full traceback

    occupancy_detected_prev = None
    active_prev = None
    fault_prev = None
    low_battery_prev = None
    tampered_prev = None

    #Run
    while True:
        log.debug("Task is running")
        
        occupancy_detected_temp = var.occupancy_detected
        if occupancy_detected_temp != occupancy_detected_prev:
            occupancy_detected_prev = occupancy_detected_temp
            client.publish("pico_motion/occupancy_detected", str(int(occupancy_detected_temp)))
        
        active_temp = var.active
        if active_temp != active_prev:
            active_prev = active_temp
            client.publish("pico_motion/active", str(int(active_temp)))
        
        fault_temp = var.fault
        if fault_temp != fault_prev:
            fault_prev = fault_temp
            client.publish("pico_motion/fault", str(int(fault_temp)))

        low_battery_temp = var.low_battery
        if low_battery_temp != low_battery_prev:
            low_battery_prev = low_battery_temp
            client.publish("pico_motion/low_battery", str(int(low_battery_temp)))
            
        tampered_temp = var.tampered
        if tampered_temp != tampered_prev:
            tampered_prev = tampered_temp
            client.publish("pico_motion/tampered", str(int(tampered_temp)))

        await asyncio.sleep(period)
