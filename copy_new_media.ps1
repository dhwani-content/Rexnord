$SourceMotors = "C:\Users\krupe\.gemini\antigravity\brain\88422db0-529c-4298-aabe-153263bffe25\uploaded_media_0_1775732816143.jpg"
$SourcePartner = "C:\Users\krupe\.gemini\antigravity\brain\88422db0-529c-4298-aabe-153263bffe25\uploaded_media_1_1775732816143.png"
$DestMotors = "\\server\MasterData\Branding & Marketing\AAPanelWebsites_Antigravity\dhwani_edits\rexnord.co.in\Rexnord - update photos\electric_motors.jpg"
$DestPartner = "\\server\MasterData\Branding & Marketing\AAPanelWebsites_Antigravity\dhwani_edits\rexnord.co.in\Rexnord - update photos\auth_partner.png"

Copy-Item $SourceMotors -Destination $DestMotors -Force
Copy-Item $SourcePartner -Destination $DestPartner -Force

Write-Host "New media copied successfully!" -ForegroundColor Green
