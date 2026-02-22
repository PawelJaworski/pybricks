#!/usr/bin/env python3
"""
Pybricks Mac Sender - exactly as per official docs
"""

import asyncio
import sys
from contextlib import suppress
from bleak import BleakScanner, BleakClient

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"
HUB_NAME = "Pybricks Hub"


async def main():
    main_task = asyncio.current_task()

    def handle_disconnect(_):
        print("Hub was disconnected.")
        if not main_task.done():
            main_task.cancel()

    ready_event = asyncio.Event()

    def handle_rx(_, data: bytearray):
        if data[0] == 0x01:
            payload = data[1:]
            if payload == b"rdy":
                ready_event.set()
                print("(Hub ready)")
            else:
                print("Received:", payload)

    device = await BleakScanner.find_device_by_name(HUB_NAME)

    if device is None:
        print(f"Could not find hub: {HUB_NAME}")
        sys.exit(1)

    print(f"Found: {device.name}")

    async with BleakClient(device, handle_disconnect) as client:
        await client.start_notify(PYBRICKS_COMMAND_EVENT_CHAR_UUID, handle_rx)

        async def send(data):
            await ready_event.wait()
            ready_event.clear()
            await client.write_gatt_char(
                PYBRICKS_COMMAND_EVENT_CHAR_UUID, b"\x06" + data, response=True
            )

        print("\nStart the program on the hub now with the button.")
        print("Waiting for hub to be ready...\n")

        for i in range(5):
            await send(b"fwd")
            print("Sent: fwd")
            await asyncio.sleep(1)
            await send(b"rev")
            print("Sent: rev")
            await asyncio.sleep(1)

        await send(b"bye")
        print("Sent: bye")
        print("\nDone!")


if __name__ == "__main__":
    with suppress(asyncio.CancelledError):
        asyncio.run(main())
