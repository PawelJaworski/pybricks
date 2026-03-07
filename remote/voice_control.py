#!/usr/bin/env python3
"""
Voice-controlled Pybricks Hub via LM Studio
"""

import asyncio
import sys
import speech_recognition as sr
import requests
from contextlib import suppress
from bleak import BleakScanner, BleakClient

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"
HUB_NAME = "Pybricks Hub"
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "google/gemma-3-1b"


def listen_for_command():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Calibrating microphone...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Listening for voice command...")
    with microphone as source:
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except Exception as e:
            print(f"Microphone error: {e}")
            return None


async def keepalive_task(client, disconnected):
    """Send periodic keepalive to maintain BLE connection"""
    while not disconnected.is_set():
        try:
            await asyncio.sleep(5)
            if not disconnected.is_set() and client.is_connected:
                await client.pair()
        except Exception:
            pass


def translate_to_command(text: str) -> str | None:
    if text is None:
        return None

    system_prompt = """You are a command translator for a LEGO robot.
Translate the user's voice command to exactly one of these words:
- "fwd" for forward, go, move ahead, advance
- "rev" for backward, reverse, go back, retreat

Respond with ONLY the command word, nothing else."""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        "max_tokens": 10,
        "temperature": 0.1,
    }

    try:
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        command = result["choices"][0]["message"]["content"].strip().lower()

        if command in ("fwd", "rev"):
            return command
        else:
            print(f"Unexpected response: {command}")
            return None
    except requests.exceptions.ConnectionError:
        print("Could not connect to LM Studio. Is it running?")
        return None
    except Exception as e:
        print(f"Error calling LM Studio: {e}")
        return None


async def run_voice_control():
    ready_event = asyncio.Event()
    disconnected = asyncio.Event()

    def handle_disconnect(_):
        print("Hub was disconnected.")
        disconnected.set()

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

        keepalive = asyncio.create_task(keepalive_task(client, disconnected))

        async def send_command(data):
            await ready_event.wait()
            ready_event.clear()
            await client.write_gatt_char(
                PYBRICKS_COMMAND_EVENT_CHAR_UUID, b"\x06" + data, response=True
            )
            print(f"Sent: {data.decode()}")

        print("\nStart the program on the hub now with the button.")
        print("Waiting for hub to be ready...\n")

        await ready_event.wait()
        print("\nVoice control ready! Say 'forward' or 'backward'")

        while not disconnected.is_set():
            try:
                text = await asyncio.wait_for(
                    asyncio.to_thread(listen_for_command), timeout=10
                )
                if text:
                    command = await asyncio.to_thread(translate_to_command, text)
                    if command:
                        await send_command(command.encode())
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break

        keepalive.cancel()
        with suppress(asyncio.CancelledError):
            await keepalive


if __name__ == "__main__":
    with suppress(asyncio.CancelledError):
        asyncio.run(run_voice_control())
