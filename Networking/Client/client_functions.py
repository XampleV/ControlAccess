import requests
import os
import subprocess
import shutil

class client_func:
    def execute_powershell(cmd):
        subprocess.run(["powershell", "-Command ", cmd], capture_output=True)
    def shutdown_computer():
        os.system("shutdown /s /t 0")   
    def restart_computer():
        os.system("shutdown /r /t 0")
    def silent_deploy(program):
        if program == "firefox":
            shutil.copy("\\10.247.71.188\Deploy\Firefox Setup 99.0.msi","C:\Temp")
            completed = subprocess.run(["powershell", "-Command", "Start-Process 'C:\\Temp\\Firefox Setup 99.0.msi' \"-ms\""], capture_output=True) 
        elif program == "chrome":
            shutil.copy("\\10.247.71.188\Deploy\thechrome.msi","C:\Temp")
            completed = subprocess.run(["powershell", "-Command", "Start-Process 'C:\\Temp\\thechrome.msi' \"/qn\""], capture_output=True)
        elif program == "sublime":
            shutil.copy("\\10.247.71.188\Deploy\\sublime.exe","C:\Temp")
            completed = subprocess.run(["powershell", "-Command", "Start-Process 'C:\\Temp\\sublime.exe' \"/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /Sa\""], capture_output=True)
        elif program == "ipScanner":
            shutil.copy("\\10.247.71.188\Deploy\\ipscanner.exe","C:\Temp")
            completed = subprocess.run(["powershell", "-Command", "Start-Process 'C:\Temp\ipscanner.exe' \"/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-\""], capture_output=True)