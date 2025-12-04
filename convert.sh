#!/bin/bash
# macOS script to convert HTML to PDF using Chrome/Safari

HTML_FILE="$HOME/Downloads/os agent/OS_Agent_Complete_Report.html"
PDF_FILE="$HOME/Downloads/os agent/OS_Agent_Complete_Report.pdf"

echo "Converting HTML to PDF on macOS..."
echo "Source: $HTML_FILE"
echo "Output: $PDF_FILE"
echo ""

# Find Chrome or Safari
CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SAFARI_PATH="/Applications/Safari.app"

if [ -f "$CHROME_PATH" ]; then
    echo "Using Google Chrome for conversion..."
    "$CHROME_PATH" --headless --disable-gpu --print-to-pdf="$PDF_FILE" "$HTML_FILE"
    sleep 2
elif [ -d "$SAFARI_PATH" ]; then
    echo "Chrome not found. Using Safari..."
    echo "NOTE: Safari doesn't support headless PDF conversion."
    echo "Opening HTML file in Safari. Please use File > Export as PDF"
    open -a Safari "$HTML_FILE"
    exit 0
else
    echo "Neither Chrome nor Safari found!"
    exit 1
fi

# Check if PDF was created
if [ -f "$PDF_FILE" ]; then
    echo ""
    echo "SUCCESS! PDF created successfully!"
    echo "Location: $PDF_FILE"
    echo ""
    echo "Opening PDF..."
    open "$PDF_FILE"
else
    echo ""
    echo "PDF creation failed."
    echo "Opening HTML in browser for manual conversion..."
    echo "Please use File > Export as PDF or Print > Save as PDF"
    open "$HTML_FILE"
fi
