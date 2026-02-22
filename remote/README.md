# Pybricks Remote Control

Control LEGO Technic Hub motor from Mac via Bluetooth LE.

## Hardware
- **Hub**: LEGO Technic Hub 88012 (with Pybricks firmware)
- **Motor**: LEGO Technic Large Motor 88013 (connected to Port A)
- **Computer**: Mac laptop

## Files
- `hub_listener.py` - Program to upload to the hub
- `mac_sender.py` - Program to run on Mac
- `setup.sh` - Setup script
- `requirements.txt` - Python dependencies

## Setup

```bash
cd /Users/paweljaworski/projects/github/pybricks/remote
./setup.sh
```

## Usage

### 1. Upload hub program
1. Open https://code.pybricks.com
2. Create new program, paste `hub_listener.py`
3. Click Download to upload to hub
4. Close browser tab (disconnect)

### 2. Start hub program
1. Press hub button - light turns **YELLOW** (waiting for Mac)
2. Wait 3 seconds

### 3. Run sender on Mac
```bash
source .venv/bin/activate
python3 mac_sender.py
```

The sender will:
1. Find and connect to hub (light turns **BLUE**)
2. Wait for hub to be ready
3. Send `fwd` and `rev` commands automatically
4. Print "Received: OK" when hub responds

### Custom commands
Edit `mac_sender.py` to change commands:
- `b"fwd"` - motor forward
- `b"rev"` - motor reverse
- `b"bye"` - stop and exit

## Hub Light Colors
| Color | Status |
|-------|--------|
| YELLOW | Program running, waiting for Mac |
| BLUE | Connected to Mac |
| GREEN | Motor running forward |
| RED | Motor running reverse |

## Troubleshooting

**Hub not found:**
1. Power cycle hub (remove/reinsert batteries)
2. Press hub button to start program
3. Wait 5 seconds
4. Make sure NOT connected to Pybricks Code browser

**Motor not moving:**
1. Check hub light is BLUE (connected)
2. Check motor is connected to Port A
3. Check hub program is running

## Reference
- https://pybricks.com/projects/tutorials/wireless/hub-to-device/pc-communication/
- https://docs.pybricks.com/en/stable/
