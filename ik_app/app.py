"""
export FLASK_APP=app.py

"""
from flask import Flask, render_template, request, make_response, session, redirect, url_for, jsonify


app = Flask(__name__)
app.secret_key = 'KEEP_THIS_A SECRET'


@app.route("/")
def root():

	"""
	The simplest possible route
	"""

	return 'It works!'


@app.route('/hello')
def hello():
	'''
	the brand new hello world path
	'''

	return "hello world"


@app.route('/hello/<name>/<town>')
def hello_name(name, town):
	'''
	extract potentially dynamic content from the path
	'''

	return 'hello {} from {}'.format(name, town)


@app.route('/render/')
@app.route('/render/<name>')
def render_name(name=None):
	'''
	render the response with a jinja2 template
	'''
	return render_template('hello.html', name=name)


@app.route('/form', methods=['GET', 'POST'])
def form():
	'''
	render a form and deal with either GET or POST requests
	'''
	if request.method == 'POST':
		name = request.form['name']
		return render_template('form_result.html', name=name)
	else:
		return render_template('form.html')


@app.route('/cookie', methods=['GET','POST'])
def cookie():
	'''
	use cookies state on the client
	'''
	if request.method == 'POST':
		name = request.form['name']
		response = make_response(render_template('cookie.html', name=name))
		response.set_cookie('name', name)
		return response
	else:
		name = request.cookies.get('name')
		return render_template('cookie.html', name=name)


@app.route('/session', methods=['POST', 'GET'])
def session_handler():
	'''
	Set flask control a session (simple [non existant] authentication)
	'''
	# import pdb; pdb.set_trace()
	if request.method == 'POST':
		# check credentials
		name = request.form['name'].strip()
		if name:
			session['name'] = name
		else:
			del session['name']

	if 'name' in session:
		username = session['name']
	else:
		username = None

	return render_template('session.html', username=username)


@app.route('/logout')
def logout():
	'''
	remover the name to dignal that the user is loffed out an dredirect them to a sensible location
	'''
	session.pop('name', None)
	return redirect(url_for('session_handler'))


@app.route('/secret')
def secret():
	'''
	a secret endpoint that only john can see
	'''
	if 'name' in session:
		if session['name'].lower() == 'john':
			return render_template('secret.html')
	return redirect(url_for('session_handler'))


@app.route('/data')
def data():
	'''
	return json data
	'''
	# some data
	data = {
			"name": "john",
			"spouse": "liz",
			"town": "chingford"
			}
	return jsonify(data)
