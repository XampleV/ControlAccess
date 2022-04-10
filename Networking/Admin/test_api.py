import requests
BASE_URL = "http://10.247.71.196:6969"

def admin_login(username, password):
    login_r = requests.post(BASE_URL + "/login", params={"username":"admin", "password":"admin"})
    print (login_r.text)
def retrieve_cookie():
    login_g = requests.get(BASE_URL + "/login")
    print(login_g.text)
def send_command(command):
    send_exec = requests.post(BASE_URL + "/execute", params={"hostname":"DESKTOP-S0T4008", "execute":command}, cookies={"sid":"yes"})
    print(send_exec.text)
#retrieve_cookie()
# admin_login("admin","admin")

# send_command("execute:shutdown")

import mysql.connector

mydb = mysql.connector.connect(
  host="10.247.67.192",
  user="root",
  password="SunnyD2020",
  database="mysql"
)

mycursor = mydb.cursor()
mycursor.execute("create table if not exists admin_users (USERNAME TEXT NOT NULL, PASSWORD TEXT NOT NULL, SESSSIONID TEXT NOT NULL)")
mydb.commit()