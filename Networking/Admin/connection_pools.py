import socket 
import threading

ready_to_execute = {}

class connections_active:
    def __init__(self):
        print("Starting Connections Server...")
        self.base_url = "10.247.71.196"
        self.port = 4969
        self.start_server()
    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server.bind((self.base_url, self.port))
        except socket.error as e:
            raise SystemExit(e)
        print("Server started, waiting for connections...")
        self.server.listen(1)
        while True:
            conn, addr = self.server.accept()
            addr = addr[0]
            print(f"Connected to {addr}")
            threading.Thread(target = threaded_client, args=(conn, addr,)).start()



class threaded_client:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        # ready_to_execute[self.addr] = []

        threading.Thread(target=self.recieve).start()
    def recieve(self):
        while True:
            data = (self.conn.recv(2048).decode())
            print(f"Recieved: {data}")
            if not data:
                print("Server closed the connection.")
                break
            if data.startswith("execute:"):
                to_append = data.split("execute:")[1]
                print(f"Appending : {to_append}")
                ready_to_execute[self.hostname_to_append].append(to_append)
            elif data.startswith("hostname:"):
                self.hostname_to_append = data.split("hostname:")[1 ]
                print(f"Appending hostname: {self.hostname_to_append}")
                ready_to_execute[self.hostname_to_append] = []
    def execute_commands(self):
        while True:
            if (len(ready_to_execute[self.addr]) > 0):
                for i in ready_to_execute[self.addr]:
                    print(i)
                    
    def send_message(self, message):
        self.client.send(message.encode())
