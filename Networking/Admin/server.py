from flask import Flask, request, abort, send_file, make_response, render_template, redirect, template_rendered, url_for
from flask_restful import Api, Resource
import random
import string
import requests
import json


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
    def get(self):
        # if ("")
        args = request.args
        return args
    def post(self):
        return {"data": f"{request.data} | headers : {request.headers['api-key']}"}
        
class ClientCommands(Resource):
    def get(self):
        print("Running")
        name = request.cookies.get('sid')
        if name is None:
            return "Login required"
        response = make_response(render_template("data.html"))
        return response


class AdminLogin(Resource):
    def get(self):
        # We read session id cookie here
        #self.post()
        print("Starting...")
        name = request.cookies.get('sid')
        if (name == None):
            print("Rendering Login HTML")
            response = make_response(render_template("Login.html"))
            return response
        return name
    def post(self):
        """
        This function will be called to authenticate admin.
        After verifying info, we'll set a cookie
        """
        print("Posting to login")
        print( request.form['uname'])

        # We'll set the cookie here
        response = make_response(render_template("data.html") )
        response.set_cookie( "sid", random_char(20) )
        print("Saved cookie")
        return response


api.add_resource(ClientAuthenticate, "/auth")
api.add_resource(ClientCommands, "/execute")
api.add_resource(AdminLogin, "/login")





if __name__ == "__main__":
	app.run(host="10.247.71.196", debug = True, port=6969)