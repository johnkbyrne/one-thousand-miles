"""
export FLASK_APP=app.py

"""
from flask import Flask, render_template, request, make_response, session, redirect, url_for, jsonify

from strava_interactivity import produce_viz
app = Flask(__name__, template_folder='templates')
# app = Flask(__name__)
# app.secret_key = 'KEEP_THIS_A SECRET'


@app.route("/")
def chart():

	strava_plot = produce_viz()
	script, div = components(strava_plot)

	return render_template("index.html",
							the_div=div,
							the_script=script)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
