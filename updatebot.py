from concurrent.futures.thread import ThreadPoolExecutor
import subprocess
import wmi
import os
import time
import getpass
import re
import csv

Servers = r'C:\temp\winpatching\servers.txt'
Scripts_From = r'C:\temp\winpatching\scripts'
Scripts_To = r'temp\winpatching\scripts'
Csv_File = Scripts_From + r'\..\Report.csv'
Bit9_Csv_File = Scripts_From + r'\..\Bit9-Report.csv'
Output_File = Scripts_From + r'\..\Output-File.txt'
Copy_Files = Scripts_From + r'\..\Copy-files.ps1'
PPinged_Hosts = Scripts_From + r'\..\PPinged-Hosts.txt'
Pinged_Hosts = Scripts_From + r'\..\Pinged-Hosts.txt'
NoFiles_Hosts = Scripts_From + r'\..\NoFiles-Hosts.txt'
YesFiles_Hosts = Scripts_From + r'\..\YesFiles-Hosts.txt'
Reboot_Hosts = Scripts_From + r'\..\Reboot-Hosts.txt'
Reboot_State = Scripts_From + r'\Reboot-state.ps1'
Updates_Search = Scripts_From + r'\Updates-search.ps1'
Install_Updates = Scripts_From + r'\Install-updates.ps1'
Check_File = Scripts_To + r'\..\check_file.txt'
Bit9_File = Scripts_To + r'\..\bit9_file.txt'
Reboot_State_Log = Scripts_To + r'\..\reboot_state_log.txt'
Updates_Search_Log = Scripts_To + r'\..\updates_search_log.txt'
Update_History_Log = Scripts_To + r'\..\update_history_log.txt'
Install_Updates_Log = Scripts_To + r'\..\install_updates_log.txt'
Install_Updates_Error_Log = Scripts_To + r'\..\install_updates_error_log.txt'



rbt=er=r=c=y=p=n=s=None

#Define variables here
check_count = 50
after_reboot = 300
no_threads = 10


h = list()

kb=dict()
d=dict()
up=dict()




class updatebot:

    def __init__(self):
                
        if os.path.exists(YesFiles_Hosts):
            os.remove(YesFiles_Hosts)

        if os.path.exists(NoFiles_Hosts):
            os.remove(NoFiles_Hosts)

        if os.path.exists(Output_File):
            os.remove(Output_File)

    def sleep25(self):
        time.sleep(25)
        return
    
    def creds(self):
        print ('\nNOTICE: Enter host(s) credentials\n')
        self.username = input('Enter Username:')
        self.password = getpass.getpass('Enter password:')
        return

    def ping(self, pfile=Pinged_Hosts, nfile=NoFiles_Hosts, sfile=Servers):
        
        print ('\n############### Running PING Method ##############')
        p = open(pfile, 'w')
        n = open(nfile, 'w')
        s = open(sfile, 'r')
        of = open(Output_File, 'a')
        
        count = 0
        
        for server in s.readlines():
            
            result = subprocess.call("ping -n 2 " + server.strip(), stdout=subprocess.PIPE)
            
            if result == 0:
                output = subprocess.check_output("ping -n 1 " + server.strip(), shell=True)
                if not b'unreachable' in output:
                    p.write(server.strip() + '\n')
                else:
                    with open(nfile, 'a') as n:
                        n.write(server.strip() + '\n')
            else:
                with open(nfile, 'a') as n:
                    n.write(server.strip() + '\n')
                
        
        if os.stat(nfile).st_size > 0:
            out = open(nfile, 'r')
            pfail = out.read()
            if pfail != '\n':
                print ('\nWARNING: Ping failed on below Hosts')
                print (pfail)
                of.write('\nWARNING: Ping failed on below Hosts \n')
                of.write(pfail)
            n.close()
        else:
            print ('\nINFO: All hosts are reachable...')
            
        p.close()    
        s.close()
        of.close()
        return


            

    def bit9_check(self):
        print ('\n########## Running BIT9 CHECK Module ##########\n')
        flag = 0
        h = []
        with open(Output_File, 'a') as of:
            of.write('\n########## Running BIT9 CHECK Module ##########\n')

            if os.path.exists(Pinged_Hosts):
                with open(Pinged_Hosts, 'r') as p:
                    for host in p.readlines():
                        host = host.replace('\n', '')
                        if os.path.exists(r'\\' + host + '\\c$\\Program Files (x86)\\Bit9\\Parity Agent\\DasCLI.exe') or os.path.exists(r'\\' + host + '\\c$\\Program Files\\Bit9\\Parity Agent\\DasCLI.exe'):
                            try:
                                connect = wmi.WMI(host, user=self.username, password=self.password)
                                
                            except:
                                print ('CRITICAL: Access Denied on ' + host + ' check the credentials')
                                of.write('CRITICAL: Access Denied on ' + host + ' check the credentials')
                                exit()
                            try:
                                if os.path.exists(r'\\' + host + '\\c$\\Program Files (x86)\\Bit9\\Parity Agent\\DasCLI.exe'):
                                    #print ('ENter x86')
                                    if not os.path.exists(r'\\' + host + '\\c$\\temp\winpatching'):
                                        prs, out = connect.Win32_Process.Create(CommandLine=r'cmd /c mkdir \\' + host + '\\c$\\temp\winpatching')
                                    prs, out = connect.Win32_Process.Create(CommandLine=r'cmd /c "C:\Program Files (x86)\Bit9\Parity Agent\DasCLI.exe" status > ' + 'C:\\' + Bit9_File)
                                    prs, out = connect.Win32_Process.Create(CommandLine='cmd /c echo Bit9 Check > C:\\' + Check_File)
                                    h.append(host)
                                else:
                                    #print ('enter')
                                    if not os.path.exists(r'\\' + host + '\\c$\\temp\winpatching'):
                                        prs, out = connect.Win32_Process.Create(CommandLine=r'cmd /c mkdir \\' + host + '\\c$\\temp\winpatching')
                                    prs, out = connect.Win32_Process.Create(CommandLine=r'cmd /c "C:\Program Files\Bit9\Parity Agent\DasCLI.exe" status > ' + 'C:\\' + Bit9_File)
                                    prs, out = connect.Win32_Process.Create(CommandLine='cmd /c echo Bit9 Check > C:\\' + Check_File)
                                    h.append(host)
                            except Exception as e:
                                prs, out = connect.Win32_Process.Create(CommandLine='cmd /c echo Exception > C:\\' + Check_File)
                                print ('\nERROR: Exception occured on ' + host + ' while getting BIT9 info' + str(e))
                                of.write('\nERROR: Exception occured on ' + host + ' while getting BIT9 info' + str(e))
            time.sleep(15)
            #with open(Pinged_Hosts, 'r') as p:
            with open(Bit9_Csv_File, 'w') as cf:
                csv_writer = csv.writer(cf, delimiter=',')
                csv_writer.writerow(['Host Name' , 'Agent_Version' , 'Connection_Status' , 'Health_Status'])
                for host in h:
                    host = host.replace('\n', '')
                    C_F = r'\\' + host + '\\c$\\' + Check_File
                    with open(C_F, 'rb') as c:
                        content = (((c.read().replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'')).decode()
                        if 'Bit9 Check' in content:
                            #print ()
                            B_F = r'\\' + host + '\\c$\\' + Bit9_File
                            with open(B_F, 'rb') as b:
                                agent_version = connection_status = health_status = None
                                for i in b.readlines():
                                    i = ((i.replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'').decode()
                                    if 'Agent:' in i:
                                        agent_version = re.findall('[0-9].+', i)[0]
                                        continue
                                    elif 'Connection:' in i:
                                        connection_status = (re.findall(':.+', i)[0].replace(':', '')).strip()
                                        continue
                                    elif 'Health Status:' in i:
                                        health_status = (re.findall(':.+', i)[0].replace(':', '')).strip()
                                        
                                    
                                    if agent_version != None and connection_status != None and health_status != None:
                                        print (host , agent_version , connection_status , health_status)
                                        csv_writer.writerow([host , agent_version , connection_status , health_status])
                                        flag = 1
                                        
                                    
                                    
        if flag != 1:
            print ('\nERROR: BIT9 Agent Status report could not create\n')
        else:
            print ('\nINFO: BIT9 Agent status report created, check it under C:\\temp\winpatching\n')
        
        return
        

    
    
    def copy_files(self):
        print ('\n####### Copying .PS1 Files to Target Hosts #######')
        with open(Output_File, 'a') as of:
            of.write('\n####### Copying .PS1 Files to Target Hosts #######')
            
        output = subprocess.check_output(r'powershell -File ' + Copy_Files, shell=True)
        
        if 'NoFiles' in str(output) and os.stat(NoFiles_Hosts).st_size > 0:
            print ('\nWARNING: Script files not copied on below servers\n')
            with open(Output_File, 'a') as of:
                of.write('\nWARNING: Script files not copied on below servers')
                #print ('--- Find them in NoFiles_Hosts file')
                n = open(NoFiles_Hosts, 'r')
                for i in n.readlines():
                    print (i.replace('\n', ''))
                    of.write(i.replace('\n', ''))
                n.close()
        if 'YesFiles' in str(output) and 'NoFiles' in str(output) and os.stat(NoFiles_Hosts).st_size > 0:
            print ('\nINFO: Copying .ps1 files Done on rest of the hosts\n')

        elif 'YesFiles' in str(output):
            print ('\nINFO: Copying .ps1 files Done on ALL Hosts')

                    
        return



    def check_rbt(self, File_Hosts=YesFiles_Hosts):
        print ('\n############# Checking if RBT Needed ############')
        y = open(File_Hosts, 'rb')
        rbt = open(Reboot_Hosts, 'w')
        for host in y.readlines():
            host = ((host.replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'').decode()
            if host in d.keys():
                j = d[host]
                if len(j) != 0 and 'True' in j[len(j)-1]:
                    rbt.write(host + '\n')
        rbt.close()
        if os.stat(Reboot_Hosts).st_size == 0:
            print ('\nINFO: No reboot needed for any host...')
        else:
            rbt = open(Reboot_Hosts, 'r')
            print ('\nINFO: Reboot needed on below Hosts..')
            print (rbt.read())
            rbt.close()
        return





    def check_file(self, module, File_Hosts=YesFiles_Hosts, h=[]):
        
        c=r=er=None
        
        y = open(File_Hosts, 'rb')
        time.sleep(50)
        count = 0
        for host in y.readlines():
            host = ((host.replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'').decode()

            try:
                of = open(Output_File, 'a')
                try:
                    c_count = 0
                    while not os.path.exists(r'\\' + host + '\\c$\\' + Check_File) and c_count < 5:
                        c_count += 1
                        self.sleep25()
                    size = os.stat(r'\\' + host + '\\c$\\' + Check_File).st_size
                except:
                    with open(Output_File, 'a') as of:
                        print ('\nERROR: ' + host + ' Could not fetch Check_File')
                        if module == 'Reboot':
                            if not host in d.keys():
                                d[host] = []
                            d[host].append('Exception_check')
                            
                        elif module == 'Update':
                            if not host in up.keys():
                                up[host] = []
                            if len(up[host]) != 0:
                                up[host] = up[host] + ['Exception_check']
                            else:
                                up[host] = ['Exception_check']
                            d[host].append('Updates Found = Exception_check')
                        elif module == 'Install':
                            if not host in kb.keys():
                                kb[host] = []
                            d[host].append(' Installed Updates = Exception_check')
                            d[host].append(' Failed Updates = Exception_check')
                            kb[host].append('Exception_check')
                            
                            
                        of.write('\nERROR: ' + host + ' Could not fetch Check_File\n')
                        
                    continue
                
                
                while size == 0 and count < check_count:
                    size = os.stat(r'\\' + host + '\\c$\\' + Check_File).st_size
                    count += 1
                    self.sleep25()
                    
                if size != 0:
                    if not host in d.keys():
                        d[host] = []
                    if module == 'Reboot':
                        r = open(r'\\' + host + '\\c$\\' + Reboot_State_Log, 'r')
                        required = r.read().replace('\n', '')
                        
                        if not 'Exception' in required:
                            print (host + ' Reboot required = ' + required)
                            d[host].append(required)
                        
                        else:
                            print ('\nERROR: ' + host + ' Exception Occured while checking Rreboot status\n')
                            of.write('\nERROR: ' + host + ' Exception Occured while checking Rreboot status\n')
                            d[host].append('Exception')
                        
                        r.close()
                    
                        
                        
                    
                    elif module == 'Update':
                        if not host in up.keys():
                            up[host] = []
                        r = open(r'\\' + host + '\\c$\\' + Updates_Search_Log, 'rb')
                        content = (((r.read().replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'')).decode()
                        
                        updates = []
                        
                        if not 'Exception' in content:
                            up_count = len(re.findall('\(KB[0-9]+\)', content))
                            of.write('\nUpdates Found on ' + host + ':\n')
                            r.close()                      
                            if up_count > 0:
                                print (host + ' Updates Found = ' + str(up_count))
                                d[host].append('Updates Found = ' + str(up_count))            
                                with open(r'\\' + host + '\\c$\\' + Updates_Search_Log, 'rb') as r:
                                    for line in r.readlines():
                                        line = (((line.replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'')).decode()
                                        updates.append(line)
                                        of.write(line + '\n')
                                        
                                if len(up[host]) != 0:
                                    up[host] = up[host] + updates
                                else:
                                    up[host] = updates
                                
                            elif 'No Updates Found...' in content.strip():
                                print (host + ' Updates Found = 0')
                                updates.append(content.strip())
                                if len(up[host]) != 0:
                                    up[host] = up[host] + updates
                                else:
                                    up[host] = updates
                                d[host].append('Updates Found = 0')
                                of.write(content + '\n')
                            else:
                                print ('\nERROR: ' + host + ' Exception Occured while finding Updates\n')
                                of.write('\nERROR: ' + host + ' Exception Occured while finding Updates\n')
                                updates.append('Exception')
                                if len(up[host]) != 0:
                                    up[host] = up[host] + updates
                                else:
                                    up[host] = updates
                                d[host].append('Updates Found = Exception')
                            
                        else:
                            print ('\nERROR: ' + host + ' Exception Occured while finding Updates\n')
                            of.write('\nERROR: ' + host + ' Exception Occured while finding Updates\n')
                            updates.append(content.strip())
                            if len(up[host]) != 0:
                                up[host] = up[host] + updates
                            else:
                                up[host] = updates
                            d[host].append('Updates Found = Exception')
                        
                        
                        
                            
                        
                    
                    elif module == 'Install':
                        if host in h:
                            if not host in kb.keys():
                                kb[host] = []
                            r = open(r'\\' + host + '\\c$\\' + Install_Updates_Log, 'rb')
                            incontent = (((r.read().replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'')).decode()
                            r.close()
                            
                            if not 'Exception' in incontent:
                                print ('\nINFO: ' + host + ' Updates installion Successful\n')
                                of.write('\nINFO: ' + host + ' Updates installion Successful\n')
                                er = open(r'\\' + host + '\\c$\\' + Install_Updates_Error_Log, 'rb')
                                ercontent = (((er.read().replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'')).decode()
                                in_kb = re.findall('\(KB[0-9]+\)', incontent)
                                er_kb = re.findall('\(KB[0-9]+\)', ercontent)
                                er_count = len(er_kb)
                                in_count = len(in_kb)
                                if in_count > 0:
                                    in_updates = []
                                    d[host].append(' Installed Updates = ' + str(in_count))
                                    with open(r'\\' + host + '\\c$\\' + Install_Updates_Log, 'rb') as r:
                                        for line in r.readlines():
                                            line = (((line.replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'')).decode()
                                            in_updates.append(line)
                                    if len(kb[host]) != 1 and len(kb[host]) < 1:
                                        kb[host].append(in_updates)
                                    else:
                                        kb[host][0] = kb[host][0] + in_updates
                                        
                                        
                                else:
                                    d[host].append(' Installed Updates = 0')
                                    kb[host].append(['No Installed updates'])
                                if er_count > 0:
                                    er_updates = []
                                    d[host].append(' Failed Updates = ' + str(er_count))
                                    with open(r'\\' + host + '\\c$\\' + Install_Updates_Error_Log, 'rb') as er:
                                        for line in er.readlines():
                                            line = (((line.replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'')).decode()
                                            er_updates.append(line)
                                    if len(kb[host]) != 2 and len(kb[host]) < 2:
                                        kb[host].append(er_updates)
                                    else:
                                        kb[host][1] = kb[host][1] + er_updates
                                        
                                    
                                else:
                                    d[host].append(' Failed Updates = 0')
                                    kb[host].append(['No Failed Updates'])
                                er.close()
                            else:
                                print ('\nERROR: ' + host + ' Exception Occured at Install\n')
                                of.write('\nERROR: ' + host + ' Exception Occured at Install\n')
                                d[host].append(' Installed Updates = Exception')
                                d[host].append(' Failed Updates = Exception')
                                kb[host].append('Exception')
                        
                            
                    
                else:
                    print ('\nERROR: Check_File Taking time on ' + host + '\n')
                    of.write('\nERROR: Check_File Taking time on ' + host + '\n')
                of.close()
            except Exception as e:
                of = open(Output_File, 'a')
                print ('\nERROR: Last Connection issue on ' + host + str(e) + '\n')
                of.write('\nERROR: Last Connection issue on ' + host + str(e) + '\n')
                of.close()
                #if c != None: c.close()
                if r != None: r.close()
                if er != None: er.close()


        y.close()
        return



    
    def reboot_state(self, File_Hosts=YesFiles_Hosts):
        print ('\n########### Running REBOOT STATE Module ##########')

        '''Checking Reboot state on targets'''
        
        y = open(File_Hosts, 'rb')
        of = open(Output_File, 'a')
        of.write('\n########### Running REBOOT STATE Module ##########\n')
        for host in y.readlines():
            host = ((host.replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'').decode()
            if host != '':
                try:
                    if File_Hosts == YesFiles_Hosts:
                        try:
                            connect = wmi.WMI(host, user=self.username, password=self.password)
                        except Exception as e:
                            print (str(e))
                            print ('CRITICAL: Access Denied on ' + host + ' check the credentials')
                            of.write('CRITICAL: Access Denied on ' + host + ' check the credentials')
                            exit()
                    else:
                        try:
                            connect = wmi.WMI(host, user=self.username, password=self.password)
                        except:
                            print ('CRITICAL: Could not access ' + host + ' check the server state')
                            of.write('CRITICAL: Could not access ' + host + ' check the server state')
                            continue
                    
                    prs, out = connect.Win32_Process.Create(CommandLine='cmd /c powershell "Set-ExecutionPolicy RemoteSigned"')
                    time.sleep(3)
                    prs, out = connect.Win32_Process.Create(CommandLine='powershell -File ' + Reboot_State)
                    if out != 0:
                        print ('\nERROR: '+ host + ' Issue in launching powershell\n')
                        of.write('\nERROR: '+ host + ' Issue in launching powershell\n')
                    
                
                except Exception as e:
                    print ('\nERROR: At reboot_state for ' + host + ' catched err  ' + str(e))
                    of.write('\nERROR: At reboot_state for ' + host + ' catched err  ' + str(e) + '\n')
                    
        of.close()
        y.close()
        self.check_file('Reboot', File_Hosts)
        return




    def reboot(self, Files_Hosts=Reboot_Hosts):
        #self.creds()
        print ('\n############## Running REBOOT Module #############')
        y = open(Files_Hosts, 'rb')
        of = open(Output_File, 'a')
        of.write('\n############## Running REBOOT Module #############\n')
        for host in y.readlines():
            host = (((host.replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'')).replace(b'\n', b'').decode()
            if host != '':
                try:
                    try:
                        connect = wmi.WMI(host, user=self.username, password=self.password)
                    except:
                        print ('CRITICAL: Could not access ' + host + ' check the server state')
                        of.write('CRITICAL: Could not access ' + host + ' check the server state')
                        continue
                    
                    prs, out = connect.Win32_Process.Create(CommandLine=r'cmd /c "shutdown /r /t 25"' )
                    if out != 0:
                        print ('\nERROR: '+ host + ' Issue in Rebooting')
                    
                    else:
                        print ('INFO: Reboot initiated on ' + host)
                
                except Exception as e:
                    print ('At reboot_state for ' + host + ' catched err  ' + str(e))
        of.close()
        y.close()
        return




    def updates_search(self, File_Hosts=YesFiles_Hosts):

        '''Checking for updates on targets'''
        
        print ('\n########## Running UPDATES SEARCH Module #########')
        
        y = open(File_Hosts, 'rb')
        of = open(Output_File, 'a')
        of.write('\n########## Running UPDATES SEARCH Module #########\n')
        ex = []
        
        for host in y.readlines():
            host = ((host.replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'').decode()
            
            if host != '':
                try:
                    if File_Hosts == YesFiles_Hosts:
                        try:
                            connect = wmi.WMI(host, user=self.username, password=self.password)
                        except:
                            print ('CRITICAL: Access Denied on ' + host + ' check the credentials')
                            of.write('CRITICAL: Access Denied on ' + host + ' check the credentials')
                            exit()
                    else:
                        try:
                            connect = wmi.WMI(host, user=self.username, password=self.password)
                            
                        except:
                            print ('CRITICAL: Could not access ' + host + ' check the server state')
                            of.write('CRITICAL: Could not access ' + host + ' check the server state')
                            ex.append(host)
                            continue
                    
                    
                    prs, out = connect.Win32_Process.Create(CommandLine='cmd /c powershell "Set-ExecutionPolicy RemoteSigned"')
                    prs, out = connect.Win32_Process.Create(CommandLine='powershell -File ' + Updates_Search)
                    
                    
                except Exception as e:
                    print ('\nERROR: At update_search for ' + host + ' catched err  ' + str(e))
                    ex.append(host)
                    of.write('\nERROR: At update_search for ' + host + ' catched err  ' + str(e) + '\n')
        y.close()
        if len(ex) > 0:
            with open(File_Hosts) as y:
                temp = [((host.replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'').decode() for i in y.readlines()]
            for i in ex:
                temp.remove(i)
            with open(File_Hosts, 'w') as y:
                for i in temp:
                    y.write(i + '\n')
                
                             
        of.close()    
        self.check_file('Update', File_Hosts)
        return





    def install_updates(self, host):
        of = open(Output_File, 'a')
        
        if host != '':
           try:
               output = subprocess.check_output(r'cmdkey.exe /add ' + host + r' /user:' + self.username  + r' /pass:' + self.password, shell=True)
               
               if 'Credential added successfully'.encode() in output:
                   pass
               else:
                   print ('\nERROR: Error in adding Key for Host ' + host + '\n')
                   of.write('\nERROR: Error in adding Key for Host ' + host + '\n')
               try:
                   print ('\n ######### Update(s) installation initiated on ' + host + ' ########\n')
                   output = subprocess.check_output(r'C:\temp\winpatching\psexec.exe \\' + host + r' -u ' + self.username  + r' -p ' + self.password + r' -accepteula -i -s powershell -File ' + Install_Updates, shell=True)
                   of.write('\nINFO: ' + host + ' Update(s) installation initiated')
                   
               except Exception as e:
                   if password in str(e):
                       print ('At At Install_updates for ' + host + ' catched err\n')
                       print ('\nERROR: Install command did NOT run successfully for ' + host + '\n')
                       of.write('\nERROR: Install command did NOT run successfully for ' + host + '\n')
                   else:
                       print ('\nERROR: At install_updates for ' + host + ' catched err  ' + str(e) + '\n')
                       print ('\nERROR: Install command did NOT run successfully for ' + host + '\n')
                       of.write('\nERROR: Install command did NOT run successfully for ' + host + '\n')
                         
               
                    
           except Exception as e:
               if password in str(e):
                   print ('\nERROR: At install_updates for ' + host + ' catched err\n')
                   of.write('\nERROR: At install_updates for ' + host + ' catched err\n')
               else:
                   print ('\nERROR: At install_updates for ' + host + ' catched err  ' + str(e) + '\n')
                   of.write('\nERROR: At install_updates for ' + host + ' catched err  ' + str(e) + '\n')
        of.close()
        
        return



    def install(self, File_Hosts=YesFiles_Hosts):
        print ('\n############# Running INSTALL Module #############')
        of = open(Output_File, 'a')
        of.write('\n############# Running INSTALL Module #############\n')
        of.close()
        y = open(File_Hosts, 'rb')
        h = []
        for host in y.readlines():
            hh = ((host.replace(b'\x00', b'')).replace(b'\r\n', b'')).replace(b'\xff\xfe', b'').decode()
            if hh in d.keys():
                j = d[hh]
                if len(j) != 0 and not 'Updates Found = 0' in j[len(j)-1] and not 'Updates Found = Exception' in j[len(j)-1] :
                    h.append(hh)
                
        y.close()
        

        if len(h) == 0:
            print ('\nINFO: No Updates to Install on any hosts\n')
            return
            

        with ThreadPoolExecutor(max_workers=int(no_threads)) as executor:
            for host in h:
                time.sleep(10)
                executor.submit(self.install_updates, host)

        self.check_file('Install', File_Hosts, h)
        return



    def create_report(self):
        with open(Csv_File, 'w') as cf:
            csv_writer = csv.writer(cf, delimiter=',')
            csv_writer.writerow(['Host Name' , 'Updates' , 'Installed' , 'Failed'])
            
            for key in up.keys():
                for u in set(up[key]):
                    
                    if 'Exception' in u:
                        csv_writer.writerow([key , u , 'Exception' , 'Exception'])
                    elif  'No Updates Found...' in u:
                        if not key in kb.keys():
                            csv_writer.writerow([key , u , 'N/A' , 'N/A'])
                    elif u in kb[key][0]:
                        installed = 'YES'
                        failed = 'NO'
                        csv_writer.writerow([key , u , installed , failed])
                    elif u in kb[key][1]:
                        installed = 'NO'
                        failed = 'YES'
                        csv_writer.writerow([key , u , installed , failed])
                    else:
                        of = open(Output_File, 'a')
                        of.write('\nERROR: Unhandled EXCEPTION while recording an entry\n')
                        of.close()
                        
        return




if __name__ == '__main__':
    updatebot()

