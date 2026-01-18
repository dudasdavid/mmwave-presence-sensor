import time, sys, gc
import machine
import rp2

# Early "alive" blink (Pico W / Pico 2 W)
try:
    led = machine.Pin("LED", machine.Pin.OUT)
except:
    led = machine.Pin(25, machine.Pin.OUT)  # fallback on some builds

for _ in range(3):
    led.on(); time.sleep_ms(80)
    led.off(); time.sleep_ms(120)

# Give power + WiFi chip time to settle on cold boot (IMPORTANT)
time.sleep_ms(800)
gc.collect()

BOOTSEL_WINDOW_MS = 5000  # 5 seconds
t0 = time.ticks_ms()

while time.ticks_diff(time.ticks_ms(), t0) < BOOTSEL_WINDOW_MS:
    if rp2.bootsel_button():
        print("BOOTSEL pressed → safe mode")
        raise SystemExit   # stop boot.py, drop to REPL
    time.sleep_ms(50)

try:
    import main
    main.start()
except Exception as e:
    # Log exception to filesystem so you can read it later
    try:
        with open("boot_error.txt", "w") as f:
            sys.print_exception(e, f)
    except:
        pass
    # Slow blink 3 times to indicate "boot failed"
    for i in range(0,3):
        led.on(); time.sleep_ms(200)
        led.off(); time.sleep_ms(800)