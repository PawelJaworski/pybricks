#!/bin/bash

echo "Setting up Pybricks Remote Control..."

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Upload hub_listener.py to hub:"
echo "   - Visit https://code.pybricks.com"
echo "   - Create new program, paste hub_listener.py"
echo "   - Click Download to upload"
echo "   - Close browser tab (disconnect)"
echo ""
echo "2. Start hub program:"
echo "   - Press hub button"
echo "   - Wait for YELLOW light"
echo ""
echo "3. Run sender:"
echo "   source .venv/bin/activate"
echo "   python3 mac_sender.py"
echo ""
