# AGENTS.md - Pybricks Remote Control

## Project Overview

This is a small Python project for controlling LEGO Technic Hub motors from a Mac via Bluetooth LE. It consists of:
- `hub_listener.py` - MicroPython program that runs on the LEGO Technic Hub
- `mac_sender.py` - Python program that runs on Mac and communicates with the hub via BLE

## Development Commands

### Setup
```bash
# Create virtual environment and install dependencies
./setup.sh

# Or manually:
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Running the Application
```bash
source .venv/bin/activate
python3 mac_sender.py
```

### Testing
There are currently no automated tests in this project. To test manually:
1. Upload `hub_listener.py` to the hub via https://code.pybricks.com
2. Start the hub program (press hub button, wait for YELLOW light)
3. Run `python3 mac_sender.py` on Mac

### Linting/Type Checking
No formal linting or type checking is configured. If adding, consider:
- `ruff check .` for linting
- `mypy .` for type checking
- `black .` for formatting

Run these before committing if you choose to add them.

## Code Style Guidelines

### General
- This is a simple, personal project - keep changes minimal and focused
- Prioritize readability over complexity
- Add comments explaining non-obvious behavior, especially for hardware interactions

### Imports
- Standard library imports first
- Third-party imports second (e.g., `bleak`, `asyncio`)
- Use `from X import Y` for clarity when only using a few items
- Group imports with a single blank line between groups

### Formatting
- Use 4 spaces for indentation (PEP 8 default)
- Maximum line length: 100 characters (softer limit, flexible for readability)
- Use blank lines sparingly to separate logical sections
- Follow existing code patterns in the project

### Types
- Use type hints for new public functions
- Keep type hints simple - avoid complex generics unless necessary
- Example: `def handle_rx(_, data: bytearray):` (from mac_sender.py:25)

### Naming Conventions
- `snake_case` for functions, variables, and file names
- `SCREAMING_SNAKE_CASE` for constants
- Use descriptive names that convey purpose
- Avoid single-letter variable names except for standard loop counters

### Error Handling
- Use `sys.exit(1)` for fatal errors that should stop the program
- Wrap async operations in try/except when BLE operations might fail
- Provide clear error messages that help with debugging

### Async Code (mac_sender.py)
- Use `asyncio` for BLE communication with the hub
- Use `asyncio.current_task()` to get the current task for cancellation
- Use `contextlib.suppress` to handle `CancelledError` gracefully
- Callbacks (e.g., `handle_disconnect`, `handle_rx`) should be simple and non-blocking

### MicroPython Code (hub_listener.py)
- Uses Pybricks API: `TechnicHub`, `Motor`, `Port`, `wait`, `Color`
- Uses `usys` and `uselect` for stdin/stdout communication
- Keep the hub program simple - it runs on resource-constrained hardware
- Use `stdout.buffer.write()` for binary output, not `print()`

### BLE Communication
- Characteristic UUID: `c5f50002-8280-46da-89f4-6d8051e4aeef`
- Protocol: Send `\x06` prefix + command bytes, expect response
- Commands: `b"fwd"`, `b"rev"`, `b"bye"`
- Response format: `b"OK"` on success, `b"rdy"` when hub is ready

### File Structure
```
remote/
├── AGENTS.md           # This file
├── README.md           # Project documentation
├── hub_listener.py     # MicroPython code for LEGO hub
├── mac_sender.py       # Python code for Mac
├── requirements.txt    # Python dependencies (bleak>=0.20.0)
└── setup.sh            # Setup script
```

## Common Tasks

### Adding a New Command
1. Edit `hub_listener.py` to handle the new command in the main loop
2. Edit `mac_sender.py` to send the command bytes
3. Test manually with the hub

### Changing Hub Connection
- Edit `HUB_NAME` in mac_sender.py (default: "Pybricks Hub")
- Edit `PYBRICKS_COMMAND_EVENT_CHAR_UUID` if using a different hub type

### Debugging BLE Issues
- Check hub light color for connection status
- Enable bleak logging: `export PYBLEMT_LOG_LEVEL=DEBUG`
- Ensure hub is not connected to Pybricks Code browser
