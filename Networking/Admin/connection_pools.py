from concurrent.futures import thread
import socket 
import threading
import queue
import os
from urllib3 import get_host

thread_data = []
class connections_active:
    def __init__(self, wkr):
        print("Starting Connections Server...")
        self.base_url = "10.247.71.187"
        self.port = 4969
        self.wkr = wkr
        self.thread_queues = {}

        # threading.Thread(target=self.commands_worker, daemon=True).start()
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
            get_host_name = conn.recv(2048).decode()
            if get_host_name.startswith("hostname:"):
                get_host_name = get_host_name.split("hostname:")[1]
                c.wrk_cntrl(get_host_name, conn, addr, create=True)
            # self.wkr.put({"newhost":[get_host_name, q]})
            # thread_data[get_host_name] = q
            # thread_data.append(q)
            # self.thread_queues[get_host_name] = q
    # def commands_worker(self):
    #     print("STARTED COMMANDS WORKER")
    #     thread_database = {}
    #     while True:
    #         if not self.wkr.empty():

    #             d = self.thread_queues
    #             rec_work = self.wkr.get_nowait()
    #             if "newhost" in rec_work:
    #                 hostname = rec_work["newhost"][0]
    #                 queue_func = rec_work["newhost"][1]
    #                 thread_database[hostname]=queue_func
    #                 print("Added host from thread: ", thread_database)
    #                 self.wkr.task_done()
    #                 continue
    #             print("Got new job: ", rec_work)
    #             print("Current thread database: ", thread_database)
    #             # print("Current list: ", self.a)
    #             queue_to_input = thread_database[rec_work["hostname"]]
    #             print("Selected queue: ", queue_to_input)
    #             queue_to_input.put(rec_work["command"])
    #             self.wkr.task_done()

class controller:
    def __init__(self):
        self.queue_database = {}
    def wrk_cntrl(self, hostname, conn=None, addr=None, create=False, command=False):
        if create:
            try:
                os.mkdir(f"./logs/{hostname}")
            except Exception as e:
                print(e)
            t = threading.Thread(target = threaded_client, args=(conn, addr, hostname)).start()
        elif command:
            print("Running command")
            print("Current object: ", self.queue_database)
            print(self)
            get_q_object = self.queue_database[hostname]
            get_q_object.put(command)
            print("inserted command")
        else:
            print("Not sure what to run")


c = controller()


class threaded_client:
    def __init__(self, conn, addr, hostname):
        self.conn = conn
        self.addr = addr
        self.hostname = hostname
        print(f"A thread for {self.hostname} has started!")
        # ready_to_execute[self.addr] = []

        threading.Thread(target=self.recieve).start()
        threading.Thread(target=self.execute_commands).start()
        
    def recieve(self):
        while True:
            data = (self.conn.recv(2048).decode())
            print(f"Recieved: {data}")
            if not data:
                print("Client closed the connection.")
                # we set it offline

                break
            if data.startswith("execute:"):
                # to_append = data.split("execute:")[1]
                # print(f"Appending : {to_append}")
                # ready_to_execute[self.hostname_to_append].append(to_append)
                self.send_message(data.split("execute:")[1])
            elif data.startswith("hostname:"):
                self.hostname_to_append = data.split("hostname:")[1 ]
                print(f"Appending hostname: {self.hostname_to_append}")
                # self.thread_d[self.hostname_to_append] = []
    def execute_commands(self):
        print("Starting commands")
        while True:
            try:
                get_file = os.listdir(f"./logs/{self.hostname}")
                if len(get_file) >= 1:
                    print("found file")
                    with open (f"./logs/{self.hostname}/request", "r") as f:
                        read_cmd = f.read()
                        f.close()
                    print("sending message to client...")
                    self.send_message(read_cmd)
                    os.remove(f"./logs/{self.hostname}/request")
                        
            except Exception as e:
                print(e)
                continue               
    def send_message(self, message):
        self.conn.send(message.encode())
