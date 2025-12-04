#!/bin/bash
# Quick setup script for macOS

echo "======================================"
echo "OS Agent - macOS Setup"
echo "======================================"
echo ""

# Check Python version
echo "1. Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found! Please install Python 3.8 or higher."
    echo "   Download from: https://www.python.org/downloads/"
    exit 1
fi
echo "✅ Python 3 found"
echo ""

# Install dependencies
echo "2. Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed"
echo ""

# Check for .env file
echo "3. Checking for API configuration..."
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo ""
    echo "Creating .env file template..."
    echo "OPENROUTER_API_KEY=your_gemini_api_key_here" > .env
    echo ""
    echo "📝 Please edit .env file and add your Gemini API key"
    echo "   Get your key from: https://aistudio.google.com/app/apikey"
    echo ""
    echo "Opening .env file for editing..."
    open -e .env
else
    echo "✅ .env file found"
fi
echo ""

# Make scripts executable
echo "4. Setting up executable scripts..."
chmod +x convert.sh
echo "✅ Scripts configured"
echo ""

# Create directories
echo "5. Creating necessary directories..."
mkdir -p screenshots
mkdir -p recordings
mkdir -p screenshots/errors
echo "✅ Directories created"
echo ""

echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "⚠️  IMPORTANT: macOS Permissions Required"
echo ""
echo "You need to grant permissions for:"
echo "  1. Accessibility Control"
echo "  2. Screen Recording"
echo ""
echo "Go to: System Preferences → Security & Privacy → Privacy"
echo "Add Terminal to both Accessibility and Screen Recording"
echo ""
echo "======================================"
echo "Ready to use!"
echo "======================================"
echo ""
echo "Launch with GUI:  python3 main.py --gui"
echo "Launch CLI mode:  python3 main.py"
echo ""
