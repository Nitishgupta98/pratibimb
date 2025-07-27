#!/bin/zsh

echo "🔧 Starting setup on macOS..."

# Create virtual environment with system Python
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip and install dependencies from requirements.txt
echo "📦 Upgrading pip and installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete! To activate the environment later, run: source .venv/bin/activate"