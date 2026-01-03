import uasyncio as asyncio
import machine

import network
import socket
import ntptime
from my_wifi import SSID, PASSWORD

from services.idle_task import idle_task
from services.serial_task import serial_task
from services.mqtt_task import mqtt_task

from logger import Logger
log = Logger("main", debug_enabled=True)

# ---- Global variables ----
import shared_variables as var

def wifi_connect():

    # ---- CONNECT TO WIFI ----
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    log.info("Connecting to WiFi...")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)

    log.info("Connected!")
    log.info("IP address:", wlan.ifconfig()[0])

    # ---- SYNC TIME FROM NTP ----
    log.info("Fetching time from NTP...")
    try:
        ntptime.settime()  # sets internal RTC to UTC
        log.info("Time synchronized.")
    except Exception as e:
        log.error("NTP sync failed:", e)

# ---------- Boot ----------
async def main():
    
    # kick watchdog if you want (optional)
    #wdt = machine.WDT(timeout=8000)

    # 1) bring up network in main thread (safer)
    wifi_connect()

    # 2) spawn threads
    asyncio.create_task(idle_task(2))
    asyncio.create_task(serial_task(1))
    asyncio.create_task(mqtt_task(5))

    # 3) main loop can do supervision / LEDs / watchdog
    led = machine.Pin("LED", machine.Pin.OUT)

    while True:
        led.toggle()
        #wdt.feed()
        await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop()
