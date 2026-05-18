$projectDir = "A:\Tirocinio\WorkDistributionSystem"

# Load .env file
Get-Content "$projectDir.env" | ForEach-Object {
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

# Delete older backups
# -lt => less than, | =>
Get-ChildItem $backupDir -Filter "*.zip" |
    Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-2)} |
    Remove-Item
