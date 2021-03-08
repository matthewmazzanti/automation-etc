import asyncio
import json
from collections import defaultdict

import aiohttp
import evdev
from evdev import ecodes, categorize
from evdev.events import KeyEvent

class Hass:
    def __init__(self):
        with open("token") as f:
            token = f.read().strip()

        self.url = "http://192.168.3.10:8123"
        self.headers = { "Authorization": f"Bearer {token}" }
        self._session = None

    def session(self):
        "This function can *only* be called within an event loop"

        if not self._session:
            self._session = aiohttp.ClientSession(headers=self.headers)

        return self._session

    async def exec(self, service, entity_id):
        req = self.session().post(
            f"{self.url}/api/services/{service}",
            json={ "entity_id": entity_id }
        )

        async with req as res:
            print("status:", res.status)
            print(await res.json())


    async def lights_on(self):
        await self.exec(
            "automation/trigger",
            "automation.matthew_bedroom_all_on"
        )

    async def lights_off(self):
        await self.exec(
            "automation/trigger",
            "automation.matthew_bedroom_all_off"
        )

    async def fan_toggle(self):
        await self.exec("fan/toggle", "fan.matthew_bedroom")

    async def fan_up(self):
        await self.exec("fan/speed_up", "fan.matthew_bedroom")

    async def fan_down(self):
        await self.exec("fan/speed_down", "fan.matthew_bedroom")


def get_zima():
    for dev in map(evdev.InputDevice, evdev.list_devices()):
        if dev.name == "splitkb Zima":
            return dev

def translate(handlers):
    return {
        ecodes.ecodes[f"KEY_{key.upper()}"]: fn
        for key, fn in handlers.items()
    }

def default(key):
    async def notify():
        print(f"Key {key} has no handler")

    return notify

async def main():
    hass = Hass()

    handlers = translate({
        "q": default("q"),
        "w": default("w"),
        "e": default("e"),
        "o": default("o"),
        "f": default("f"),
        "g": default("g"),
        "k": default("k"),
        "l": default("l"),
        "x": hass.fan_toggle,
        "a": hass.fan_up,
        "v": hass.fan_down,
        "c": default("c"),
        "comma": hass.lights_off,
        "dot": hass.lights_on
    })

    zima = get_zima()
    with zima.grab_context():
        async for event in zima.async_read_loop():
            if event.type == ecodes.EV_KEY and event.value == KeyEvent.key_down:
                asyncio.create_task(handlers[event.code]())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
