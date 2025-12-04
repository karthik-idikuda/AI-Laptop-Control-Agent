# PowerShell script to convert HTML to PDF using Chrome headless

$htmlFile = "c:\Users\idiku\Downloads\os agent\OS_Agent_Complete_Report.html"
$pdfFile = "c:\Users\idiku\Downloads\os agent\OS_Agent_Complete_Report.pdf"

# Find Chrome installation
$chromePaths = @(
    "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "${env:LOCALAPPDATA}\Google\Chrome\Application\chrome.exe"
)

$chromePath = $null
foreach ($path in $chromePaths) {
    if (Test-Path $path) {
        $chromePath = $path
        break
    }
}

if (-not $chromePath) {
    Write-Host "Chrome not found. Trying Microsoft Edge..." -ForegroundColor Red
    $edgePath = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
    if (Test-Path $edgePath) {
        $chromePath = $edgePath
        Write-Host "Using Microsoft Edge" -ForegroundColor Green
    } else {
        Write-Host "Neither Chrome nor Edge found!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Found Chrome:$chromePath" -ForegroundColor Green
}

Write-Host "Converting HTML to PDF..." -ForegroundColor Cyan
Write-Host "Source: $htmlFile" -ForegroundColor Gray
Write-Host "Output: $pdfFile" -ForegroundColor Gray

# Delete existing PDF if present
if (Test-Path $pdfFile) {
    Remove-Item $pdfFile -Force
}

# Convert HTML to PDF using headless Chrome
& $chromePath --headless --disable-gpu --print-to-pdf="$pdfFile" "$htmlFile"

Start-Sleep -Seconds 3

# Check if PDF was created
if (Test-Path $pdfFile) {
    $fileSize = (Get-Item $pdfFile).Length / 1KB
    Write-Host ""
    Write-Host "PDF created successfully!" -ForegroundColor Green
    Write-Host "Location: $pdfFile" -ForegroundColor Cyan
    Write-Host "File size: $($fileSize.ToString('F1')) KB" -ForegroundColor Cyan
    Write-Host ""
    
    # Open PDF
    Write-Host "Opening PDF..." -ForegroundColor Yellow
    Start-Process $pdfFile
} else {
    Write-Host ""
    Write-Host "Failed to create PDF" -ForegroundColor Red
    Write-Host "Trying alternative method..." -ForegroundColor Yellow
    
    # Alternative: Open HTML in browser for manual PDF save
    Write-Host "Opening HTML in browser..." -ForegroundColor Cyan
    Start-Process $htmlFile
    Write-Host "Please use Ctrl+P and Save as PDF manually" -ForegroundColor Yellow
}
