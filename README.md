Carrying on from @magicus premise- I don't want to flash my devices with custom firmware if the native firmware works. Reasons being as possible bricking of the device during flashing and an **unfounded assumption** the manufacturer optimally handles battery life.

I simply copy the slim_scaled.py to my local and run the file with an image argument.
```
python slim_scaled.py upload_image.png
```

Substantial testing has not been done.  All usual disclaimers (no warranties, etc) about bricking your device apply).  This is largley a porting of part of ATC1441's solution from Javascript to Python.


# BLE ePaper for Home Assistant

This is a custom integration for Home Assistant that supports BLE (Bluetooth Low Energy) ePaper
ESL (Electronic Shelf Label) displays.

Currently, this integration supports BLE ePaper displays from Picksmart, also known as Gicisky.

## Installation

HACS installation is upcoming, once this integration leaves beta state.

## Supported devices

This integration ~~supports most, but not all, of~~ has only been tested on the 400x300 BWR Gicisky/Picksmart devices.

**Only devices with ~~BW (Black/White) and~~ BWR (Black/White/Red) pixels are supported.**

~~The devices on this list should work in theory, but only those with a check mark
in the Verified column have actually been verified to work.~~
Currently hardcoded to one size (I think- don't understand the UUID's) and looks for a pre-defined MAC address.

### Supported

| Display Type | Size      | Pixel Colors | Verified           |
|--------------|-----------|--------------|--------------------|
| ePaper       | 400x300   | BWR Only (?) | :white_check_mark: |

### Unsupported (Perhaps)

| Display Type | Size      | Pixel Colors |
|--------------|-----------|--------------|
| ePaper       | 212x104   | BW or BWR    |                    |
| ePaper       | 240x416   | BW or BWR    |                    |
| ePaper       | 250x122   | BW or BWR    |                    |
| ePaper       | 272x792   | BW or BWR    |                    |
| ePaper       | 280x480   | BW or BWR    |                    |
| ePaper       | 296x128   | BW or BWR    |                    |
| ePaper       | 640x384   | BW or BWR    |
| ePaper       | 792x272   | BW or BWR    |                    |
| ePaper       | 800x480   | BW or BWR    |                    |
| ePaper       | 960x640   | BW or BWR    |                    |
| ePaper       | 960x680   | BW or BWR    |                    |
| ePaper       | 1360x480  | BW or BWR    |                    |
| TFT          | 168x384   | BW or BWR    |                    |
| TFT          | 196x96    | BW or BWR    |                    |
| TFT          | 250x132   | BW or BWR    |                    |
| TFT          | 384x168   | BW or BWR    |                    |
| TFT          | 640x480   | BW or BWR    |                    |
| TFT          | 384x168   | BW or BWR    |
| TFT          | 400x300   | BW or BWR    |
| Any          | Any       | BWRGBY+      |
