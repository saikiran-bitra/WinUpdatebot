# WinUpdatebot
The project targets on finding pending software updates and install them on windows machines. 
The code is written in Python3 which runs on a control machine and pushes Powershell scripts on to the target machines for Finding updates/Installing updates/Checking reboot status of the target machines.
Output of the powershell scripts are captured in text files on the target machines and the content of files is retrived by the Python program running on the contol machine for processing.
