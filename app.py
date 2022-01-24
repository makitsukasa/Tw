import os
import json
import datetime
from flask import Flask, request
from flask_httpauth import HTTPDigestAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('CUSTOMCONNSTR_SECRET_KEY')
users = json.loads(os.getenv('CUSTOMCONNSTR_USERS'))
auth = HTTPDigestAuth()

# https://www.mathpython.com/ja/flask-https-redirect
@app.before_request
def before_request():
	if not request.is_secure:
		url = request.url.replace('http://', 'https://', 1)
		code = 301
		return redirect(url, code=code)

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
