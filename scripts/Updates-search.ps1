#Find pending updates on the Machine


$c = hostname
$Scripts_From = "C:\temp\winpatching\scripts"
$Update_History_Log = "$Scripts_From\..\update_history_log.txt"
$Updates_Search_Log = "$Scripts_From\..\updates_search_log.txt"
$Check_File = "$Scripts_From\..\check_file.txt"
$report = @()
$Check = "False"

"Running US script" | Add-Content $Check_File

Clear-Content $Check_File

"Running US script" | Add-Content $Updates_Search_Log

Clear-Content $Updates_Search_Log

Try {
            
                $updatesession =  [activator]::CreateInstance([type]::GetTypeFromProgID("Microsoft.Update.Session",$c))
                $updatesearcher = $updatesession.CreateUpdateSearcher()
                
                
                $searchresult = $updatesearcher.Search("IsInstalled=0 and Type='Software'") 
   
                echo "$searchresult.Updates.Count is the update count"

                
                If ($searchresult.Updates.Count -gt 0) {
                    $count = $searchresult.Updates.Count
                                        
                    Write-Verbose "Iterating through list of updates"
                    For ($i=0; $i -lt $Count; $i++) {
                        
                        $update = $searchresult.Updates.Item($i)
                        
                        
                        If (($update.IsDownLoaded -eq "True") -or ($update.IsDownLoaded -eq "False") { 
                            
                            $title = $update.Title
                            
                            "$title" | Add-Content $Updates_Search_Log
                            
                            $Check = "True"
                            }
                        }
                    If (!($Check -eq "True")){
                       
                       "   No Updates Found..." | Add-Content $Updates_Search_Log
                             
                            }
                        
                    }
                Else {
                    "   No Updates Found..." | Add-Content $Updates_Search_Log
                    }              
                }
Catch {
                
                "Exception" | Add-Content $Updates_Search_Log
                }




"Update search check" | Add-Content $Check_File