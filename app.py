import os
import json
from datetime import timezone, timedelta
from imgutil import base64ify, get_image
from tweet import (update_status, home_timeline,
	create_favorite, destroy_favorite, retweet, get_image_url)
from flask import Flask, request, render_template, make_response
from flask_httpauth import HTTPDigestAuth
from flask_talisman import Talisman

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('CUSTOMCONNSTR_SECRET_KEY')
Talisman(app)
users = json.loads(os.getenv('CUSTOMCONNSTR_USERS'))
auth = HTTPDigestAuth()

@app.route('/')
@auth.login_required
def app_route_index():
	return 'Hello, ' + auth.username()

@app.route('/tw')
@auth.login_required
def app_route_tw():
	return render_template('tw.html')

@app.route('/tl')
@auth.login_required
def app_route_tl():
	return render_template('tl.html', home_timeline = home_timeline())

@app.route('/update_status', methods=['POST'])
@auth.login_required
def app_route_update_status():
	body = request.form.get('body')
	if not update_status(body):
		return '/update_status server error', 500
	return '/update_status post succeeded'

@app.route('/create_favorite', methods=['POST'])
@auth.login_required
def app_route_create_favorite():
	print('create_favorite')
	id = request.json['id']
	print(id)
	if not id or not create_favorite(id):
		return '/create_favorite server error', 500
	return '/create_favorite post succeeded'

@app.route('/destroy_favorite', methods=['POST'])
@auth.login_required
def app_route_destroy_favorite():
	print('destroy_favorite')
	id = request.json['id']
	print(id)
	if not id or not destroy_favorite(id):
		return '/destroy_favorite server error', 500
	return '/destroy_favorite post succeeded'

@app.route('/retweet', methods=['POST'])
@auth.login_required
def app_route_retweet():
	id = request.json['id']
	if not id or not retweet(id):
		return '/retweet server error', 500
	return '/retweet post succeeded'

@app.route('/image', methods=['POST'])
@app.route('/image/<string:id>/<int:index>', methods=['GET'])
@auth.login_required
def app_route_image(id='', index=0):
	if not id:
		id = request.form.get('id')
		if not id:
			return '/image server error', 500
		count = request.form.get('count') or 4
		return render_template('img.html', id=id, count=count)
	try:
		url = get_image_url(id, index)
		image = get_image(url)
		response = make_response(image)
		response.headers.set('Content-Type', request.content_type)
		return response
	except IndexError:
		return '/image server error', 500

@app.route('/receive', methods=['GET', 'POST'])
def app_route_receive():
	return 'HRADER<br>' + str(request.headers) + '<br><br>' +\
		'DATA<br>' + request.get_data(as_text=True)

@auth.get_password
def get_password(username):
	if username in users:
		return users.get(username)
	return None

if __name__ == '__main__':
	app.run(debug=True)
