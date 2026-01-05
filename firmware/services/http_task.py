import uasyncio as asyncio
from logger import Logger
import time
import ujson

# ---- Global variables ----
import shared_variables as var
 
# ------------------ HTTP helpers ------------------
async def _send_json(writer, obj, status="200 OK"):
    body = ujson.dumps(obj).encode("utf-8")
    hdr = (
        "HTTP/1.1 %s\r\n"
        "Content-Type: application/json\r\n"
        "Connection: close\r\n"
        "Content-Length: %d\r\n"
        "\r\n"
    ) % (status, len(body))
    await writer.awrite(hdr)
    await writer.awrite(body)


async def _send_text(writer, text, status="404 Not Found"):
    body = text.encode("utf-8")
    hdr = (
        "HTTP/1.1 %s\r\n"
        "Content-Type: text/plain; charset=utf-8\r\n"
        "Connection: close\r\n"
        "Content-Length: %d\r\n"
        "\r\n"
    ) % (status, len(body))
    await writer.awrite(hdr)
    await writer.awrite(body)


async def _read_request_line(reader):
    line = await reader.readline()
    if not line:
        return None, None, None
    try:
        method, path, version = line.decode().strip().split()
        return method, path, version
    except:
        return None, None, None


async def _drain_headers(reader):
    while True:
        line = await reader.readline()
        if not line or line == b"\r\n":
            return
 
async def http_task(period = 1.0):
    #Init
    log = Logger("http_upd", debug_enabled=True)

    #Run
    while True:
        try:
            async with var._http_lock:
                var.HTTP_STATE["OccupancyDetected"] = bool(var.occupancy_detected)
                var.HTTP_STATE["Active"]            = bool(var.active)
                var.HTTP_STATE["Fault"]             = bool(var.fault)
                var.HTTP_STATE["LowBattery"]        = bool(var.low_battery)
                var.HTTP_STATE["Tampered"]          = bool(var.tampered)

        except Exception as e:
            log.error("State update failed:", e)

        await asyncio.sleep(period)

# ------------------ HTTP server ------------------
async def http_server_task(host="0.0.0.0", port=80):
    log = Logger("http_srv", debug_enabled=True)

    async def handler(reader, writer):
        try:
            method, path, _ = await _read_request_line(reader)
            if method is None:
                await writer.aclose()
                return

            await _drain_headers(reader)

            if method != "GET":
                await _send_text(writer, "Method Not Allowed", "405 Method Not Allowed")

            elif path == "/motion":
                async with var._http_lock:
                    snap = dict(var.HTTP_STATE)
                await _send_json(writer, snap)

            elif path == "/":
                await _send_text(writer, "OK – try GET /motion", "200 OK")

            else:
                await _send_text(writer, "Not Found", "404 Not Found")

        except Exception as e:
            log.error("HTTP handler error:", e)
        finally:
            try:
                await writer.aclose()
            except:
                pass

    server = await asyncio.start_server(handler, host, port)
    log.info("HTTP server listening on %s:%d" % (host, port))

    while True:
        await asyncio.sleep(10)
