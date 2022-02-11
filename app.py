import os
import json
from imgutil import get_image
from tweet import (update_status, get_timeline, get_reply_chain,
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
	return render_template('tl.html', timeline = get_timeline())

@app.route('/chn', methods=['POST'])
@auth.login_required
def app_route_chn():
	id = request.form.get('id')
	if not id:
		return '/chn server error', 500
	return render_template('chn.html', statuses = get_reply_chain(id))

@app.route('/img', methods=['POST'])
@app.route('/img/<string:id>/<int:index>', methods=['GET'])
@auth.login_required
def app_route_image(id='', index=0):
	if not id:
		id = request.form.get('id')
		if not id:
			return '/img server error', 500
		count = request.form.get('count') or 4
		return render_template('img.html', id=id, count=count)
	try:
		url = get_image_url(id, index)
		response = make_response(get_image(url))
		response.headers.set('Content-Type', request.content_type)
		return response
	except IndexError:
		return '/img server error', 500

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
	id = request.json['id']
	if not id or not create_favorite(id):
		return '/create_favorite server error', 500
	return '/create_favorite post succeeded'

@app.route('/destroy_favorite', methods=['POST'])
@auth.login_required
def app_route_destroy_favorite():
	id = request.json['id']
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
