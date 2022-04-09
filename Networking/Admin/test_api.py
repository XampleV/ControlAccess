import requests
BASE_URL = "http://127.0.0.1:5000"

def admin_login(username, password):
    login_r = requests.post(BASE_URL + "/login", params={"username":"admin", "password":"admin"})
    print (login_r.text)
def retrieve_cookie():
    login_g = requests.get(BASE_URL + "/login")
    print(login_g.text)
#retrieve_cookie()
admin_login("admin","admin")