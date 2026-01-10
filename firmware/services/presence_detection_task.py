import uasyncio as asyncio
from logger import Logger
import time

# ---- Global variables ----
import shared_variables as var

def _now_ms():
    # Prefer monotonic ticks on MicroPython
    try:
        return time.ticks_ms()
    except AttributeError:
        # Fallback (lower resolution, not wrap-safe)
        return int(time.time() * 1000)

def _ms_since(t0_ms, t1_ms):
    # Wrap-safe if ticks_ms exists
    try:
        return time.ticks_diff(t1_ms, t0_ms)
    except AttributeError:
        return t1_ms - t0_ms

async def presence_detection_task(period = 1.0):
    #Init
    log = Logger("presence", debug_enabled=True)
    
    hold_on_s=10.0      # minimum ON time after any trigger
    mmwave_grace_s=2.0  # small grace to bridge mmWave brief dropouts

    hold_on_ms = int(hold_on_s * 1000)
    mmwave_grace_ms = int(mmwave_grace_s * 1000)

    occupancy = False
    last_on_ms = 0
    last_mmwave_true_ms = 0

    var.occupancy_detected = False

    #Run
    while True:
        try:
            now = _now_ms()

            pir = var.pir_detected
            mmw = var.mm_wave_detected

            # Track last time mmWave was TRUE (for dropout grace)
            if mmw:
                last_mmwave_true_ms = now

            # PIR triggers immediately (fast path)
            if pir:
                if not occupancy:
                    occupancy = True
                    last_on_ms = now
                    var.occupancy_detected = True
                    log.info("Occupancy ON (PIR)")
                else:
                    # refresh hold window on repeated PIR hits
                    last_on_ms = now

            # mmWave triggers immediately (fast path)
            if mmw:
                if not occupancy:
                    occupancy = True
                    last_on_ms = now
                    var.occupancy_detected = True
                    log.info("Occupancy ON (mmWave)")
                else:
                    # refresh hold window on repeated mmWave hits
                    last_on_ms = now

            # If already occupied, keep it on for at least hold_on_s
            if occupancy:
                on_for_ms = _ms_since(last_on_ms, now)
                if on_for_ms < hold_on_ms:
                    # hard hold: do not turn off regardless of inputs
                    pass
                else:
                    # after hold window, rely mostly on mmWave to sustain
                    mmwave_recent = _ms_since(last_mmwave_true_ms, now) <= mmwave_grace_ms
                    if mmwave_recent:
                        # still present (or brief dropout)
                        pass
                    else:
                        # Only turn off if BOTH are false (and mmWave not recent)
                        if (not pir) and (not mmw):
                            occupancy = False
                            var.occupancy_detected = False
                            log.info("Occupancy OFF (no PIR + no mmWave)")

        except Exception as e:
            # Never let the task die; log and continue
            try:
                log.error("Exception:", e)
            except Exception:
                pass

        await asyncio.sleep(period)


