$Server = "ftp://159.89.94.209"
$Username = "rexnord"
$Password = "7N6e5bRejisKwRsk"

# Directories and files to upload
$SourceDir = "\\server\MasterData\Branding & Marketing\AAPanelWebsites_Antigravity\dhwani_edits\rexnord.co.in"

# Function to upload a single file
function Upload-File {
    param (
        [string]$LocalFile,
        [string]$RemotePath
    )

    try {
        $uri = "$Server/$RemotePath"
        # Convert spaces to %20 to avoid parsing issues
        $uri = $uri.Replace("\", "/")
        
        Write-Host "Uploading $LocalFile to $uri"
        
        $webclient = New-Object System.Net.WebClient
        $webclient.Credentials = New-Object System.Net.NetworkCredential($Username, $Password)
        $webclient.UploadFile($uri, $LocalFile)
        Write-Host "Success: $LocalFile" -ForegroundColor Green
    } catch {
        Write-Host "Failed: $LocalFile" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        
        # If the directory doesn't exist, we might need to create it
        if ($_.Exception.Message -match "The remote server returned an error: \(550\)") {
            Write-Host "Attempting to create directory for $RemotePath..." -ForegroundColor Yellow
            $parentDir = Split-Path $RemotePath -Parent
            if ($parentDir) {
                Create-FtpDirectory $parentDir
                # Retry upload
                try {
                    $webclient.UploadFile($uri, $LocalFile)
                    Write-Host "Success after dir create: $LocalFile" -ForegroundColor Green
                } catch {
                    Write-Host "Failed again: $LocalFile" -ForegroundColor Red
                }
            }
        }
    }
}

# Function to create an FTP directory
function Create-FtpDirectory {
    param (
        [string]$RemoteDir
    )
    
    try {
        $uri = "$Server/$RemoteDir"
        $uri = $uri.Replace("\", "/")
        
        $request = [System.Net.FtpWebRequest]::Create($uri)
        $request.Credentials = New-Object System.Net.NetworkCredential($Username, $Password)
        $request.Method = [System.Net.WebRequestMethods+Ftp]::MakeDirectory
        
        $response = $request.GetResponse()
        Write-Host "Created Directory: $uri" -ForegroundColor Cyan
        $response.Close()
    } catch {
        # Directory might already exist, ignore errors (e.g. 550)
    }
}

# Get all files except the deploy script itself
$files = Get-ChildItem -Path $SourceDir -Recurse -File | Where-Object { $_.Name -ne "deploy.ps1" }

foreach ($file in $files) {
    # Get relative path from source dir
    $relPath = $file.FullName.Substring($SourceDir.Length).TrimStart('\')
    
    # Replace backward slashes with forward slashes for FTP path
    $remotePath = $relPath.Replace('\', '/')
    
    # First ensure parent directory exists on FTP if there is one
    $parentDir = Split-Path $relPath -Parent
    if ($parentDir) {
        $remoteParentPath = $parentDir.Replace('\', '/')
        Create-FtpDirectory $remoteParentPath
    }
    
    # Upload the file
    Upload-File -LocalFile $file.FullName -RemotePath $remotePath
}

Write-Host "Deployment process complete." -ForegroundColor Green
