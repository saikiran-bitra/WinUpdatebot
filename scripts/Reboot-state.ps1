#Check the Reboot status of the Machine

$c = hostname
$Scripts_From = "C:\temp\winpatching\scripts"
$Reboot_State_Log = "$Scripts_From\..\reboot_state_log.txt"
$Check_File = "$Scripts_From\..\check_file.txt"

"Running RS script" | Add-Content $Check_File

Clear-Content $Check_File

if (Test-Path $Reboot_State_Log){ Clear-Content $Reboot_State_Log }


Try {
                    
                    $updatesession =  [activator]::CreateInstance([type]::GetTypeFromProgID("Microsoft.Update.Session",$c))
                    $updatesearcher = $updatesession.CreateUpdateSearcher()
                    $searchresult = $updatesearcher.Search("RebootRequired=1")
                    Switch (@($searchresult.updates).count) {
                        {$_ -eq 0} {
                            "False" | Add-Content $Reboot_State_Log
                        }
                        {$_ -ge 1} {
                            "True" | Add-Content $Reboot_State_Log            
                        }
                    }
} 
Catch {
      "Exception" | Add-Content $Reboot_State_Log
      }

"Reboot check" | Add-Content $Check_File