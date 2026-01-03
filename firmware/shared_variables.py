# shared_variables.py
import uasyncio as asyncio

class SimpleQueue:
    def __init__(self):
        self._items = []
        self._lock = asyncio.Lock()

    async def put(self, item):
        async with self._lock:
            self._items.append(item)

    async def get(self):
        while True:
            async with self._lock:
                if self._items:
                    return self._items.pop(0)
            await asyncio.sleep_ms(10)

# Create a global queue instance
events = SimpleQueue()

async def post_event(ev):
    await events.put(ev)

a = 0
b = 0
c = 0

scd41_co2_ppm = 0
scd41_temp_deg = 0
scd_41_humidity_percent = 0
aht21_temp_deg = 0
aht21_humidity_percent = 0
battery_voltage = 0
input_voltage = 0
analog_lux = 0
bmp280_pressure = 0
ens160_aqi = 0
ens160_tvoc = 0
ens160_tvoc_rating = 0
ens160_eco2 = 0
ens160_eco2_rating = 0
co2_history = []
max_history_samples = 60

free_space = 0
all_space = 0

display_view = 0
