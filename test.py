import asyncio
import aiohttp
from pprint import pprint

with open("token") as f:
    token = f.read().strip()

async def expect(ws, exp_type):
    msg = await ws.receive_json()
    print(msg)

    for key, value in exp_type.items():
        if not msg[key] == value:
            raise Exception(
                f"Unexpected message key {msg[key]}, expected {value}"
            )

    return msg

async def auth(ws):
    await expect(ws, {"type": "auth_required"})

    await ws.send_json({
        "type": "auth",
        "access_token": token
    })

    await expect(ws, {"type": "auth_ok"})

async def print_messages(ws):
    await auth(ws)

    await ws.send_json({
        "id": 1,
        "type": "subscribe_events",
        "event_type": "call_service",
    })

    await expect(ws, {"id": 1, "type": "result", "success": True})

    while not ws.closed:
        msg = await ws.receive_json()
        try:
            await handle(msg["event"]["data"])
        except KeyError as e:
            print(e)

async def handle(data):
    if data["domain"] == "notify" and data["service"] == "mmazzanti":
        print(data["service_data"])
        await notify(**data["service_data"])

async def notify(message, title=None):
    cmd = ["notify-send"]
    if title:
        cmd.append(title)

    cmd.append(message)
    print(cmd)
    await asyncio.create_subprocess_exec(*cmd)


async def main():
    async with aiohttp.ClientSession() as session:
        url = "http://192.168.3.10:8123/api/websocket"
        async with session.ws_connect(url) as ws:
            await print_messages(ws)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
