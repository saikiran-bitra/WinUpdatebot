import updatebot
import os
import time
import subprocess

u = updatebot.updatebot()
#Servers = r'C:\temp\winpatching\servers.txt'


def install_reboot():
    print ('''
******************************************************
** WARNING: Hosts will be rebooted                  **
**          before and after update(s) installation **
**          if needed                               **
******************************************************''')
    
    #updatebot.no_threads  = input ('\nNo of threads: ')
    u.creds()
    u.ping()
    u.copy_files()
    
    if not os.path.exists(updatebot.YesFiles_Hosts):
        print ('INFO: No hosts to patch... ' + updatebot.YesFiles_Hosts + ' does not exist')
        exit()
    u.reboot_state()
    u.check_rbt()

    if os.stat(updatebot.Reboot_Hosts).st_size > 0:
        u.reboot()
        time.sleep(updatebot.after_reboot)
        os.remove(updatebot.Reboot_Hosts)
        u.ping(updatebot.Pinged_Hosts, updatebot.NoFiles_Hosts, updatebot.YesFiles_Hosts)
    else:
        p = open(updatebot.YesFiles_Hosts)
        pp = open(updatebot.Pinged_Hosts, 'w')
        for i in p.readlines():
         pp.write(i)
        pp.close()
        p.close()

    u.updates_search(File_Hosts=updatebot.Pinged_Hosts)
    u.install(File_Hosts=updatebot.Pinged_Hosts)
    u.reboot_state(File_Hosts=updatebot.Pinged_Hosts)
    u.sleep25()
    u.check_rbt(File_Hosts=updatebot.Pinged_Hosts)

    while os.stat(updatebot.Reboot_Hosts).st_size > 0:
        u.reboot()
        time.sleep(updatebot.after_reboot)
        u.ping(updatebot.PPinged_Hosts, updatebot.NoFiles_Hosts, updatebot.Pinged_Hosts)
        #u.reboot_state()
        os.remove(updatebot.Reboot_Hosts)
        u.updates_search(File_Hosts=updatebot.PPinged_Hosts)
        u.install(File_Hosts=updatebot.PPinged_Hosts)
        u.reboot_state(File_Hosts=updatebot.PPinged_Hosts)
        u.sleep25()
        u.check_rbt(File_Hosts=updatebot.PPinged_Hosts)
        updatebot.Pinged_Hosts, updatebot.PPinged_Hosts = updatebot.PPinged_Hosts, updatebot.Pinged_Hosts

    os.remove(updatebot.NoFiles_Hosts)
    print ('\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ GIST OF THE RUN @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    with open(updatebot.Output_File, 'a') as of:
        of.write('\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ GIST OF THE RUN @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n')
        for i,j in zip(updatebot.d.keys(), updatebot.d.values()):
            print (i + ' : ' + str(j) + '\n')
            of.write(i + ' : ' + str(j) + '\n')

    
    u.create_report()
    print ('\nINFO: Report generated, check it under C:\\temp\\winpatching')
    
    return


def noreboot_install():
    print ('''
*****************************************************
** NOTICE: NO reboot is performed                  **
**         before and after update(s) installation **
**         though needed                           **
*****************************************************''')
    #updatebot.no_threads  = input ('\nNo of threads: ')
    u.creds()
    u.ping()
    u.copy_files()
    
    if not os.path.exists(updatebot.YesFiles_Hosts):
        print ('INFO: No hosts to patch... ' + updatebot.YesFiles_Hosts + ' does not exist')
        exit()
    u.reboot_state()
    u.updates_search(File_Hosts=updatebot.Pinged_Hosts)
    u.install(File_Hosts=updatebot.Pinged_Hosts)
    u.reboot_state(File_Hosts=updatebot.Pinged_Hosts)

    print ('\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ GIST OF THE RUN @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    with open(updatebot.Output_File, 'a') as of:
        of.write('\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ GIST OF THE RUN @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n')
        for i,j in zip(updatebot.d.keys(), updatebot.d.values()):
            print (i + ' : ' + str(j) + '\n')
            of.write(i + ' : ' + str(j) + '\n')

    
    u.create_report()
    print ('\nINFO: Report generated, check it under C:\\temp\\winpatching')

    return


def reboot_state():
    u.creds()
    u.ping()
    u.copy_files()    
    u.reboot_state()
    return

def updates_search():
    u.creds()
    u.ping()
    u.copy_files()    
    u.updates_search()
    return
    

def reboot():
    u.creds()
    u.ping()
    u.reboot(updatebot.Pinged_Hosts)
    return

def bit9_check():
    u.creds()
    u.ping()
    u.bit9_check()
    return

def symantic_check():
    pass

def update_history():
    pass
    return





options = {'1': {'1': bit9_check, '2': symantic_check, 'q': exit, 'Q': exit},
           '2': reboot_state,
           '3': updates_search,
           '4': u.ping,
           '5': noreboot_install,
           '6': install_reboot,
           '7': reboot,
           '8': update_history,
           'q': exit,
           'Q': exit,
           }

result = subprocess.call('cmd /c cls')
print ('''
\t\t\t O P E R A T O R    M E N U
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@''')

print ('''
\t\t    CHECK
\t\t\t1. Bit9 & Symantic Check
\t\t\t2. Reboot Status Check
\t\t\t3. Updates Check
\t\t\t4. Ping
\n\t\t    INSTALL
 \t\t\t5. Install Updates & NO Reboot
\t\t\t6. Install Updates & Reboot
\n\t\t    REBOOT
\t\t\t7. Reboot
\n\t\t    AUDIT
\t\t\t8. Update History
          \n''')

num = input ('\t\tChoose option (q to Quit): ')


if num in options.keys():
    if num == '1':
        result = subprocess.call('cmd /c cls')
        print('''
\t\t    BIT9 & SYMANTIC
\t\t\t1. Bit9 Connectivity Check
\t\t\t2. Symantic Connectivity Check
              \n''')
        sub_num = input ('\t\tChoose option (q to Quit): ')
        if sub_num in options['1'].keys():
            options['1'][sub_num]()
            print ('\n')
        else:
            print ('Invalid selection')
            exit()
    else:
        options[num]()
        print ('\n')
else:
    print ('Invalid selection')
    exit()
