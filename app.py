import datetime
from flask import Flask, request
from flask_httpauth import HTTPDigestAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'acchikocchifukin'
auth = HTTPDigestAuth()

users = {
	"user01" : "pass01"
}

@app.route("/")
@auth.login_required
def app_route_index():
	try:
		return "Hello, " + auth.username()
	except Exception as e:
		return "Exception:" + str(traceback.format_exc()), 500
		
@auth.get_password
def get_password(username):
    if username in users:
        return users.get(username)
    return None

if __name__ == "__main__":
	app.run(debug = True)
