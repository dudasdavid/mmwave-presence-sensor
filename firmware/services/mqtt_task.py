import uasyncio as asyncio
from umqtt.simple import MQTTClient
import umqtt.config

from logger import Logger

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

    #Run
    while True:
        log.debug("Task is running")
        client.publish("pico_motion/motion_detected", "1")
        client.publish("pico_motion/occupancy_detected", "1")
        client.publish("pico_motion/active", "1")
        client.publish("pico_motion/fault", "0")
        client.publish("pico_motion/low_battery", "0")
        client.publish("pico_motion/tampered", "0")
        await asyncio.sleep(period)
