import queue
from flask import Flask, request, abort, send_file, make_response, render_template, redirect, url_for
from flask_restful import Api, Resource
import random
import string
import os
import threading
from connection_pools import connections_active, threaded_client, c
from database_handler import sql_module

db = sql_module()
app = Flask(__name__, template_folder='template')
api = Api(app)



@app.route('/')
def main():
    return redirect(url_for('adminlogin'))

def random_char(r):
    return ''.join(random.choice(string.ascii_letters) for x in range(int(r)))
@app.before_request
def check_details():
	# if (request.headers.get('User-Agent') != "python-requests/2.25.1"):
	# 	print("Bad header")
	# 	return request.headers.get('User-Agent')
	# elif (api_header not in request.headers):
	# 	return fake_error
	# elif (action not in request.headers):
	# 	return fake_error
    pass
	

class ClientAuthenticate(Resource):
    print("Running this function")
    def post(self):
        # this function will update the details in the database
        data = request.json
        # get_api = request.cookies.get("X-API-KEY")
        # if get_api is None:
        #     return "API Not Included"
        # verify X-API-KEY here....

        # register data here...
        try:
            get_info = db.pull_device(hostname=data["hostname"])
            if get_info != None:
                db.device_re(data["hostname"])
                print("Merged Record...")
            try:
                register = db.register_device((data["hostname"], 1, data["ip_address"], data["mac_address"], data["os_type"], data["os_type"], data["processor"], data["ram"]))
                if (register != True):
                    return f"Registration came back false\nReturned: {register}"
                return True
            except Exception as registration_failed:
                print(f"DB Registration function failed\n** ERROR: {registration_failed}")
                return f"Failed to register, error: {registration_failed}"
            # Here this means that there is already an existing record.
            # It'll compare, and if there is a difference, it'll update the record.

        except Exception as e:
            print(f"Failed to register device\n** ERROR: {e}")
            return "Function failed"


class ClientCommands(Resource):
    def post(self):
        name = request.cookies.get('X-API-KEY')
        if name is None:
            print( "Login is required")
        data = request.get_json(force=True)
        hostname,command = data["hostname"], data["execute"]
        with open(f"./logs/{hostname}/request", "w") as f:
            f.write(command)
            f.close()
            return 200
    def get(self):
        args = request.args
        # hn = hostname
        if "hn" not in args:
            return "device needs to be passed in url"
        name = request.cookies.get('sid')
        if name is None:
            print("Using rule")
            rule = request.args.get('hn')
            rule = f"http://10.247.71.196:6969/login?redirect={rule}"

            return redirect(rule)
            # return redirect(url_for('adminlogin'))
        # verify if the cookie here is valid. 
        print(f"Found Cookie: {name}")
        get_session = db.search_by_session(name)
        if get_session != True:
            return "Invalid cookie"
        # pull device here
        try:
            get_data = db.pull_device(args["hn"])
            if get_data == None:
                return "device not found"
        except Exception as e:
            return f"Error pulling device, error : {e}"
        print("Got data successfully. ")
        # we need to render the data here into the html
        name,status,ipv4,mac,installedOs,osVersion,cpu,ram,applications = get_data

        if status == 0:
            status = "Offline"
        elif status == 1:
            status = "Online"
            
        # redirect('/execute/hn=' + rule)
        response = make_response(render_template("data.html", compName = name, compStatus =status, compIp = ipv4, compVersion = installedOs, compCPU = cpu, compRam = ram))
        return response

class AdminLogin(Resource):
    def get(self):
        # We read session id cookie here
        #self.post()
        
        name = request.cookies.get('sid')
        if name is None:
            response = make_response(render_template("login.html"))
            return response
        return redirect(url_for('clientcommands')) 
    def post(self):
        """
        This function will be called to authenticate admin.
        After verifying info, we'll set a cookie
        """
        try:
            username = request.form.get("uname")
            password = request.form.get("psw")
        except:
            return "Credentails not provided"
        pull_admin_account = db.get_admin_details(username=username)
        retr_name = pull_admin_account[0]
        if pull_admin_account is None:
            return "User account not found"
        # we should hash the passwords in the database
        if (password != pull_admin_account[1]):
            return "Incorrect password"
        print("Admin credentails match, setting a cookie...")
        # We'll set the cookie here
        new_cookie = random_char(20)
        response = make_response( render_template("twofactor.html") )
        response.set_cookie( "sid", new_cookie )
        


        # updating the cookie here in the database..
        if db.modify_admin_cookie(admin_username=retr_name, new_cookie=new_cookie) != True:
            print("Wasn't able to modify cookie.")
        
        return response


api.add_resource(ClientAuthenticate, "/auth")
api.add_resource(ClientCommands, "/execute")
api.add_resource(AdminLogin, "/login")

# server = connections_active()
server_queue = queue.Queue()
threading.Thread(target = connections_active, args=(server_queue,)).start()


if __name__ == "__main__":
	app.run(host="10.247.71.187", debug = True, port=6969)