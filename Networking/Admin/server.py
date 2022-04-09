import queue
from flask import Flask, request, abort, send_file, make_response, render_template, redirect, url_for
from flask_restful import Api, Resource
import random
import string
import os
import threading
from connection_pools import connections_active, threaded_client, c

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
        return data
class ClientCommands(Resource):
    def post(self):
        name = request.cookies.get('sid')
        if name is None:
            return "Login is required"
        data = request.args
        hostname,command = data["hostname"], data["execute"]
        # print(data["execute"])
        # print(ready_to_execute)
        # return 200
        # ready_to_execute[str(data["hostname"])] = []
        # ready_to_execute[data["hostname"]].append(data["execute"])
        # print(ready_to_execute)
        try:
            os.mkdir(f"./logs/{hostname}")
        except:
            pass
            
        with open(f"./logs/{hostname}/request", "w") as f:
            f.write(command)
            f.close()
            return 200
        c.wrk_cntrl(hostname=hostname,command=command)
        # server_queue.put({"hostname":data["hostname"], "command":data["execute"]})
        print("Queued new item")
        # ready_to_execute[data["hostname"]].append(data["execute"])
    def get(self):
        name = request.cookies.get('sid')
        if name is None:
            return "Login is required"
        response = make_response( render_template("data.html") )
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
        #if "username" not in request.args or "password" not in request.args:
            #return {"error":"Headers did not contain credentials. "}
        # We'll set the cookie here
        response = make_response( render_template("data.html") )
        response.set_cookie( "sid", random_char(20) )
        return response


api.add_resource(ClientAuthenticate, "/auth")
api.add_resource(ClientCommands, "/execute")
api.add_resource(AdminLogin, "/login")

# server = connections_active()
server_queue = queue.Queue()
threading.Thread(target = connections_active, args=(server_queue,)).start()


if __name__ == "__main__":
	app.run(host="10.247.71.196", debug = True, port=6969)