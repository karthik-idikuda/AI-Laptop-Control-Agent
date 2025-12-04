@echo off
echo Converting HTML to PDF using Chrome...

set CHROME="C:\Program Files\Google\Chrome\Application\chrome.exe"
set HTML_FILE="c:\Users\idiku\Downloads\os agent\OS_Agent_Complete_Report.html"
set PDF_FILE="c:\Users\idiku\Downloads\os agent\OS_Agent_Complete_Report.pdf"

echo Source: %HTML_FILE%
echo Output: %PDF_FILE%
echo.

%CHROME% --headless --disable-gpu --print-to-pdf=%PDF_FILE% %HTML_FILE%

timeout /t 5 > nul

if exist %PDF_FILE% (
    echo.
    echo SUCCESS! PDF created successfully!
    echo Location: %PDF_FILE%
    echo.
    echo Opening PDF...
    start "" %PDF_FILE%
) else (
    echo.
    echo PDF creation seems to have issues.
    echo Opening HTML in browser for manual conversion...
    echo Please use Ctrl+P and "Save as PDF"
    start "" %HTML_FILE%
)
