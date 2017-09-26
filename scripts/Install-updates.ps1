
$c = hostname

$Scripts_From = "C:\temp\winpatching\scripts"

$Check_File = "$Scripts_From\..\check_file.txt"

$Install_Updates_Log = "$Scripts_From\..\install_updates_log.txt"

$Install_Updates_Error_Log = "$Scripts_From\..\install_updates_error_log.txt"

$Check = "False"

"Running IU script" | Add-Content $Check_File
"Running IU script"  | Add-Content $Install_Updates_Log
"Running IU script"  | Add-Content $Install_Updates_Error_Log

Clear-Content $Check_File
Clear-Content $Install_Updates_Log
Clear-Content $Install_Updates_Error_Log

Try {

    $updatesession =  [activator]::CreateInstance([type]::GetTypeFromProgID("Microsoft.Update.Session",$c))

    $updatesearcher = $updatesession.CreateUpdateSearcher()

    $searchresult = $updatesearcher.Search("IsInstalled=0 and Type='Software'")    

    



    If ($searchresult.Updates.Count -gt 0) {
        $count = $searchresult.Updates.Count


        For ($i=0; $i -lt $count; $i++) {
            $Update = $searchresult.Updates.Item($i)
            
            $UpdatesToDownload = New-Object -Com Microsoft.Update.UpdateColl
            $updatesToInstall = New-Object -ComObject Microsoft.Update.UpdateColl
            $Installer = $updatesession.CreateUpdateInstaller()
            
            If (($update.IsDownLoaded -eq "True") -or ($update.IsDownLoaded -eq "False")){ 
               
               If ($update.IsDownLoaded -eq "False") {
                   Try {

                   $NULL = $UpdatesToDownload.Add($Update)
                   $Downloader = $UpdateSession.CreateUpdateDownloader()
                   $Downloader.Updates = $UpdatesToDownload
                   $NULL = $Downloader.Download()

                   }

                   Catch {

                   echo Exception

                   }
               }

               If ($update.IsDownLoaded -eq "True") {

               $Update | foreach-Object {$updatesToInstall.Add($_) }
               $Check = "True"
               $u = $update.Title
   
   
   
               Try {
   
                   $Installer.Updates = $updatesToInstall
                   $Result = $Installer.Install()
                   $res = $Result
                   $r = $Result.HResult
                   $rr = $Result.ResultCode
                   sleep 3
   
   
   
                   #$Result.GetUpdateResult(0).ResultCode
   
                   If (($r -gt 0) -or ($r -lt 0)) {
                      
                       $u | Add-Content $Install_Updates_Error_Log
                          }
                   Else {
                      
                      $u | Add-Content $Install_Updates_Log
                       }
                   }


                Catch {
                   
                   $u | Add-Content $Install_Updates_Error_Log
                   }
   
                }

              }
   
         
           }       


   }

}

Catch {
"Exception" | Add-Content $Install_Updates_Log

}

"Install updates" | Add-Content $Check_File



