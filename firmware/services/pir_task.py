import uasyncio as asyncio
from logger import Logger
import utime
from machine import Pin

# ---- Global variables ----
import shared_variables as var

async def pir_task(period = 1.0):
    #Init
    log = Logger("pir", debug_enabled=True)
    
    DEBOUNCE_MS = 30
    _last_ms = 0
    
    def on_edge(p):
        nonlocal _last_ms, DEBOUNCE_MS
        now = utime.ticks_ms()
        if utime.ticks_diff(now, _last_ms) < DEBOUNCE_MS:
            return
        _last_ms = now

        # Read current level inside the IRQ
        level = p.value()   # 0 or 1
        var.pir_detected = bool(level)
        log.info("EDGE! level =", level, "at", now, "ms")

    pir_in = Pin(2, Pin.IN)
    
    pir_in.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=on_edge)
    
    #Run
    while True:

        #log.debug(pir_in.value())
        await asyncio.sleep(period)

