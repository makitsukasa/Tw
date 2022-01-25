import os
import json
import datetime
from tweet import update_status, home_timeline
from flask import Flask, request, render_template
from flask_httpauth import HTTPDigestAuth
from flask_talisman import Talisman

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('CUSTOMCONNSTR_SECRET_KEY')
Talisman(app)
users = json.loads(os.getenv('CUSTOMCONNSTR_USERS'))
auth = HTTPDigestAuth()

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

@app.route("/tl")
@auth.login_required
def app_route_tl():
	return render_template('tl.html', home_timeline = home_timeline())

@app.route("/update_status", methods=["POST"])
@auth.login_required
def app_route_update_status():
	body = request.form.get("body")
	if not update_status(body):
		return "/update_status server error", 500
	return "/update_status post succeeded"

@app.route("/receive", methods=["GET", "POST"])
def app_route_receive():
	return "HRADER<br>" + str(request.headers) + "<br><br>" +\
		"DATA<br>" + request.get_data(as_text=True)

@auth.get_password
def get_password(username):
	if username in users:
		return users.get(username)
	return None

if __name__ == "__main__":
	app.run(debug=True)
