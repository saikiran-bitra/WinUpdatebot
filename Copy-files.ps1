$Hosts = "C:\temp\winpatching\Pinged-Hosts.txt"
$Scripts_From = "C:\temp\winpatching\scripts"
$Output_File = "$Scripts_From\..\Output-File.txt"
$NoFiles_Hosts = "$Scripts_From\..\NoFiles-Hosts.txt"
$YesFiles_Hosts = "$Scripts_From\..\YesFiles-Hosts.txt"
$Scripts_To = "temp\winpatching\scripts"
$Updates_Search = "Updates-search.ps1"
$Uinstall = "Install-updates.ps1"
$Reboot_State = "Reboot-state.ps1"

$servers = Get-Content "$Hosts"


if (Test-Path $YesFiles_Hosts){ Clear-Content $YesFiles_Hosts }


foreach ($sserver in $servers) {
$server = $sserver.Trim()


robocopy "$Scripts_From" "\\$server\C$\$Scripts_To" /r:2 /w:5

If ((Test-Path "\\$server\C$\$Scripts_To\$Updates_Search") -and (Test-Path "\\$server\C$\$Scripts_To\$Uinstall") -and (Test-Path "\\$server\c$\$Scripts_To\$Reboot_State")){
$server | Add-Content  $YesFiles_Hosts
}
Else {
$server | Add-Content $NoFiles_Hosts
"ERROR: $server Files not copied" | Add-Content $Output_File
}
}

if (Test-Path $NoFiles_Hosts){echo "NoFiles_Hosts created"}

if (Test-Path $YesFiles_Hosts){echo "YesFiles_Hosts created"}