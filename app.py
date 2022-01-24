import os
import json
import datetime
from tweet import update_status
from flask import Flask, request, render_template
from flask_httpauth import HTTPDigestAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('CUSTOMCONNSTR_SECRET_KEY')
users = json.loads(os.getenv('CUSTOMCONNSTR_USERS'))
auth = HTTPDigestAuth()

# https://www.mathpython.com/ja/flask-https-redirect
# @app.before_request
# def before_request():
# 	if not request.is_secure:
# 		url = request.url.replace('http://', 'https://', 1)
# 		code = 301
# 		return redirect(url, code=code)

@app.route("/")
@auth.login_required
def app_route_index():
	try:
		return "Hello, " + auth.username()
	except Exception as e:
		return "Exception:" + str(traceback.format_exc()), 500

@app.route("/tw")
@auth.login_required
def app_route_tw():
	return render_template('tw.html')

@app.route("/update_status", methods=["POST"])
@auth.login_required
def app_route_update_status():
	body = request.form.get("body")
	if not update_status(body):
		return "/update_status server error", 500
	return "/update_status post succeeded"
		
@auth.get_password
def get_password(username):
    if username in users:
        return users.get(username)
    return None

if __name__ == "__main__":
	app.run(debug = True)
