import uasyncio as asyncio
from logger import Logger
import time
from machine import ADC

# ---- Global variables ----
import shared_variables as var

# measured values
V1 = 0.12   # volts at 30 lux
V2 = 2.10   # volts at 1000 lux

L1 = 20
L2 = 700

# compute linear coefficients
A = (L2 - L1) / (V2 - V1)
B = L1 - A * V1

def voltage_to_lux(voltage):
    return max(0, A * voltage + B)

async def adc_task(period = 1.0):
    #Init
    log = Logger("adc", debug_enabled=False)

    adc = ADC(26)   # GPIO26 = ADC0

    #Run
    while True:
        value = adc.read_u16()  # 0–65535
        voltage = value * 3.3 / 65535
        lux = voltage_to_lux(voltage)
        
        log.info("ADC voltage:", voltage, "Lux:", lux)
        log.debug("ADC voltage:", voltage, "Lux:", lux)
                
        await asyncio.sleep(period)


