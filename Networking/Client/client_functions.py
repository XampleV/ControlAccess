import requests
import os
import subprocess

class client_func:
    def execute_powershell(cmd):
        completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    def shutdown_computer():
        os.system("shutdown /s /t 0")   
    def restart_computer():
        os.system("shutdown /r /t 0")
    def silent_deploy(url):
        pass