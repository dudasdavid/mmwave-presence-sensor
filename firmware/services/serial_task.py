import uasyncio as asyncio
from machine import UART, Pin
from logger import Logger

async def serial_task(period = 1.0):
    #Init
    log = Logger("uart", debug_enabled=True)

    #Run
    while True:
        log.debug("Task is running")
        
        await asyncio.sleep(period)