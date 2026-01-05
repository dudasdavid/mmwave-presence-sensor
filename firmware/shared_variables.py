# shared_variables.py
import uasyncio as asyncio

HTTP_STATE = {
    "OccupancyDetected": False,
    "Active": False,
    "Fault": False,
    "LowBattery": False,
    "Tampered": False,
}

_http_lock = asyncio.Lock()

occupancy_detected = False
active = True
fault = False
low_battery = False
tampered = False

pir_detected = False
mm_wave_detected = False