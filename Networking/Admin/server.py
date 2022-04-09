from flask import Flask, request, abort, send_file, make_response, render_template
from flask_restful import Api, Resource
import requests
import json


app = Flask(__name__, template_folder='template')
api = Api(app)


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
    def post(self):
        """"""
        pass

class AdminLogin(Resource):
    @app.route('/')
    def get(self):
        # We read session id cookie here
        name = request.cookies.get('name')
        return name
    def post(self):
        """
        This function will be called to authenticate admin.
        After verifying info, we'll set a cookie
        """
        if "username" or "password" not in request.args:
            return {"error":"Headers did not contain credentials. "}
        # We'll set the cookie here
        response = make_response( render_template("test.html") )
        response.set_cookie( "name", "value" )
        return response


api.add_resource(ClientAuthenticate, "/auth")
api.add_resource(ClientCommands, "/execute")
api.add_resource(AdminLogin, "/login")

if __name__ == "__main__":
	app.run(debug = True)