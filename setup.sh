#!/bin/bash

echo "🚀 Setting up LEGO Pybricks env..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Activate venv: source .venv/bin/activate"
echo "2. Test LM Studio: python3 test_lm_studio.py"
echo "3. Run demo: python3 demo.py"
echo "4. Run full app: python3 lego_voice_controller.py"
echo ""
echo "💡 Remember to start LM Studio and load a model before running!"