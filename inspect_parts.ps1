$partsDir = "c:\Users\krupe\Downloads\rexnord.co.in\rexnord.co.in\parts"
$htmlFiles = Get-ChildItem -Path $partsDir -Filter "*.html"

$results = @()

foreach ($file in $htmlFiles) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    
    # Check if disc coupling page
    if ($content -match 'disc couplings/([^"\''<>]+)') {
        $pdfName = $matches[1]
        
        # h1
        $h1 = "N/A"
        if ($content -match '<h1[^>]*>([^<]+)</h1>') {
            $h1 = $matches[1].Trim()
        }
        
        # part number
        $partNo = "N/A"
        if ($content -match 'Part Number:\s*([A-Za-z0-9_-]+)') {
            $partNo = $matches[1].Trim()
        }
        
        # PDF filename from URL (decode %20 to space)
        $pdfNameDecoded = [System.Uri]::UnescapeDataString($pdfName)
        
        $results += [PSCustomObject]@{
            html_file = $file.Name
            part_no = $partNo
            h1 = $h1
            pdf_name = $pdfNameDecoded
        }
    }
}

Write-Output "Found $($results.Count) disc coupling HTML files."

# Format output and save
$outputFile = "c:\Users\krupe\Downloads\rexnord.co.in\rexnord.co.in\disc_couplings_info.txt"
$results | ForEach-Object {
    "$($_.html_file)|$($_.part_no)|$($_.h1)|$($_.pdf_name)"
} | Set-Content -Path $outputFile

Write-Output "Saved to $outputFile"
