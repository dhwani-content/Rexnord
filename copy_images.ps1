$SourceDir = "C:\Users\krupe\.gemini\antigravity\brain\88422db0-529c-4298-aabe-153263bffe25"
$DestDir = "\\server\MasterData\Branding & Marketing\AAPanelWebsites_Antigravity\dhwani_edits\rexnord.co.in\images"

Write-Host "Creating images directory if it doesn't exist..."
if (-Not (Test-Path -Path $DestDir)) {
    New-Item -ItemType Directory -Force -Path $DestDir | Out-Null
}

Write-Host "Copying generated background images..."
Copy-Item -Path "$SourceDir\*.png" -Destination $DestDir -Force

Write-Host "Images copied successfully!" -ForegroundColor Green
