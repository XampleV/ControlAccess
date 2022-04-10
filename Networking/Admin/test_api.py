from socket import getfqdn
import requests
import os
BASE_URL = "http://10.247.71.196:6969"
sid = "dXvHskHsciOgpAEiXsOy"
def admin_login(username, password):
    login_r = requests.post(BASE_URL + "/login", params={"username":"admin", "password":"admin"})
    print (login_r.text)
def retrieve_cookie():
    login_g = requests.get(BASE_URL + "/login")
    print(login_g.text)

def send_command(command):
    send_exec = requests.post(BASE_URL + "/execute", params={"hostname":"DESKTOP-S0T4008", "execute":command}, cookies={"sid":sid})
    print(send_exec.text)

def install_app(command):
    send_request = requests.post(BASE_URL +"/execute", params={"hostname":"DESKTOP-S0T4008", "execute":command}, cookies={"sid":sid, "X-API-KEY":"yes"})
    print(send_request.text)

def restart():
    send_restat = requests.post(BASE_URL +"/execute", params={"hostname":"DESKTOP-S0T4008", "execute":command}, cookies={"sid":sid, "X-API-KEY":"yes"})
    print(send_restat.text)

def shutDown():
    send_shutDown = requests.post(BASE_URL +"/execute", params={"hostname":"DESKTOP-S0T4008", "execute":command}, cookies={"sid":sid, "X-API-KEY":"yes"})
    print(shutDown.text)
#retrieve_cookie()
# admin_login("admin","admin")

# send_command("execute:shutdown")
install_app("program:sublime")

    
# set up for pc_specs here 

# sql_cmd = "create table if not exists pc_info (hostname TEXT NOT NULL, active INT NOT NULL, ip_address text not null, os_version text not null, cpu text not null, ram_size text not null)"


# print(c.get_admin_details("admin"))
# c.register_device(("fr",0, "mx", "work", "bruh", "ram_size"))
# c.pull_device("fr")

# mycursor.execute(sql_cmd)
# mydb.commit()
# get_admin_details("admin")
