import uasyncio as asyncio
from logger import Logger

# ---- Global variables ----
import shared_variables as var
 
async def fake_detection_task(period = 1.0):
    #Init
    log = Logger("fake_detection", debug_enabled=True)

    #Run
    while True:

        var.occupancy_detected = not var.occupancy_detected
            
        await asyncio.sleep(period)


