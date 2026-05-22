$excelFile = "c:\Users\krupe\Downloads\112338broucher18.xlsx"
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$workbook = $excel.Workbooks.Open($excelFile)

Write-Output "Sheets in $excelFile :"
foreach ($sheet in $workbook.Sheets) {
    Write-Output $sheet.Name
}

# Let's search for "10109259" in all sheets to see if we can find it
foreach ($sheet in $workbook.Sheets) {
    Write-Output "Searching in sheet: $($sheet.Name)"
    $usedRange = $sheet.UsedRange
    $rows = $usedRange.Rows.Count
    $cols = $usedRange.Columns.Count
    
    # Check top 5 rows
    Write-Output "Top 5 rows:"
    for ($r = 1; $r -le [Math]::Min($rows, 5); $r++) {
        $rowVal = @()
        for ($c = 1; $c -le [Math]::Min($cols, 10); $c++) {
            $rowVal += $usedRange.Cells.Item($r, $c).Text
        }
        Write-Output ($rowVal -join " | ")
    }
}

$workbook.Close($false)
$excel.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
