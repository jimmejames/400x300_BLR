######################################
######
###### Use:
######   python slim_scaled.py [your_image.png]
######
######
######################################

import asyncio
import sys
import time
from PIL import Image, ImageDraw, ImageFont
from bleak import BleakClient, BleakScanner
import struct

SERVICE_UUID = "0000fef0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_CMD_UUID = "0000fef1-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_IMG_UUID = "0000fef2-0000-1000-8000-00805f9b34fb"

#################
TARGET_ADDRESS = "FF:FF:99:86:XX:XX"
canvas_width = 400
canvas_height = 300
ble_client = None
img_data = b""
image_part_size = 180
upload_done = False
#################

def log(msg):
    print(msg)

def get_bitpacked_image_data(image):
    image = image.convert("RGB")
    pixels = image.load()
    byte_data = []
    byte_data_red = []
    bit_position = 7
    current_byte = 0
    current_byte_red = 0

    for y in range(canvas_height):
        for x in range(canvas_width):
            r, g, b = pixels[x, y]
            luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
            if luminance > 128:
                current_byte |= (1 << bit_position)
            if r > 170 and g < 170:
                current_byte_red |= (1 << bit_position)
            bit_position -= 1
            if bit_position < 0:
                byte_data.append(current_byte)
                byte_data_red.append(current_byte_red)
                current_byte = 0
                current_byte_red = 0
                bit_position = 7

    if bit_position != 7:
        byte_data.append(current_byte)
        byte_data_red.append(current_byte_red)

    return byte_data + byte_data_red

def notification_handler(sender, data):
    global image_part_size, upload_done
    hex_data = data.hex()
    log(f"Got bytes: {hex_data}")
    if hex_data.startswith("01"):
        size = int.from_bytes(data[1:3], byteorder="little")
        image_part_size = size - 4
        log(f"Display requested part size: {image_part_size}")
    elif hex_data.startswith("02"):
        asyncio.run_coroutine_threadsafe(send_command("03"), asyncio.get_event_loop())
    elif hex_data.startswith("05"):
        if data[1] == 0x08:
            log("Upload complete. Disconnecting.")
            upload_done = True
            asyncio.run_coroutine_threadsafe(ble_client.disconnect(), asyncio.get_event_loop())
        elif data[1] != 0x00:
            log("Display reported an error during upload.")
        else:
            ack_part = struct.unpack("<I", data[2:6])[0]
            asyncio.run_coroutine_threadsafe(send_next_image_part(ack_part), asyncio.get_event_loop())

async def connect_ble():
    global ble_client
    while True:
        log(f"Scanning for {TARGET_ADDRESS} BLE devices (10 seconds)...")
        devices = await BleakScanner.discover(timeout=10.0)
        for d in devices:
            if d.address.upper() == TARGET_ADDRESS.upper():
                ble_client = BleakClient(d)
                try:
                    await ble_client.connect()
                except Exception as e:
                    log(f"Connection failed: {e}")
                    continue
                await ble_client.start_notify(CHARACTERISTIC_CMD_UUID, notification_handler)
                log(f"Connected to {d.name} ({d.address})")
                return
        log("Device not found. Waiting 3 seconds...")
        await asyncio.sleep(3)

async def send_command(cmd_hex):
    if ble_client and ble_client.is_connected:
        data = bytes.fromhex(cmd_hex)
        await ble_client.write_gatt_char(CHARACTERISTIC_CMD_UUID, data)

async def send_next_image_part(part_number):
    global img_data
    start = part_number * image_part_size
    end = start + image_part_size
    chunk = img_data[start:end]
    if not chunk:
        return
    header = struct.pack("<I", part_number)
    full_packet = header + chunk
    try:
        await ble_client.write_gatt_char(CHARACTERISTIC_IMG_UUID, full_packet)
    except Exception as e:
        log(f"Error sending part {part_number}: {e}")

async def upload_image():
    global img_data
    img_data = bytes(get_bitpacked_image_data(prepared_image))
    log(f"Total bytes to send: {len(img_data)}")

    await send_command("01")
    await send_command("02" + format_le_uint32(len(img_data)) + "000000")

def format_le_uint32(value):
    return ''.join(f"{b:02x}" for b in struct.pack("<I", value))

def verify_and_scale_image(image_path):
    log(f"Loading image: {image_path}")
    image = Image.open(image_path)
    if image.size != (canvas_width, canvas_height):
        log(f"Original image size: {image.size}. Scaling to ({canvas_width}, {canvas_height})...")
        image = image.resize((canvas_width, canvas_height))
        log("Scaling complete.")
    else:
        log("Image already matches target dimensions.")
    return image

async def main(image_path):
    global prepared_image
    prepared_image = verify_and_scale_image(image_path)

    await connect_ble()
    await upload_image()

    global upload_done
    while not upload_done:
        await asyncio.sleep(0.2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python slim_scaled.py your_image.png")
        sys.exit(1)
    asyncio.run(main(sys.argv[1]))
