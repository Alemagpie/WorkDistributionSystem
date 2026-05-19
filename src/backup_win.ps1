
# DO NOT USE, ODOO WILL BLOCK ANY EXTERNAL API CALL

$projectDir = "A:\Tirocinio\WorkDistributionSystem"

# Load .env file
Get-Content "$projectDir\.env" | ForEach-Object {
    if($_ -match '^(.+)=(.+)$') {
        [System.Environment]::SetEnvironmentVariable($Matches[1], $Matches[2])
    }
}

$date = Get-Date -Format "yyyy-MM-dd"
$backupDir = "$projectDir\backups"
$db = "odoo"
$password = $env:POSTGRES_PASSWORD
$httpURL = "http://localhost:8069/web/database/backup"

# Create directory
New-Item -ItemType Directory -Force -Path $backupDir

# Make the http request
# ` => command continues on the next line
Invoke-WebRequest -Uri $httpURL `
    -Method Post `
    -Body @{
        master_pwd = $password
        name = $db
        backup_format = "zip"
    } `
    -OutFile "$backupDir\$date.zip"


if ($response.ContentType -like "*zip*") {
    $response.Content | Set-Content -Path "$backupDir\$database.$date.zip" -Encoding Byte
    Write-Host "Backup completed: $date"
} else {
    Write-Host "ERROR: Server returned an error instead of a zip file"
    Write-Host $response.Content  # this will show you the actual error
}

# Delete older backups
# -lt => less than, | => command continues on the next line
#Get-ChildItem $backupDir -Filter "*.zip" |
#    Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-2)} |
#    Remove-Item


# Create cron job with this file
# 