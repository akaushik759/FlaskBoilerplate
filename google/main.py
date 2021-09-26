from flask import Flask, redirect, url_for, jsonify, render_template, request, session
from flask_dance.contrib.google import make_google_blueprint, google

import os

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.environ.get("FLASK_SECRET_KEY"))
app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

google_bp = make_google_blueprint(redirect_url="/login",scope=["profile", "email"])
app.register_blueprint(google_bp, url_prefix="/login")



@app.route("/")
def home():
	return "Welcome home"

@app.route("/login")
def index():
	if not google.authorized:
		print("Unauthorized Access, redirecting to Google for login")
		return redirect(url_for("google.login"))
	try:
		print("Authorized Login")
		resp = google.get("/oauth2/v1/userinfo")
		print(resp.json())
		data = resp.json()

		name = data['name']
		email = data['email']
		oauth_id = data['id']

		# APPLY YOUR LOGIC TO SAVE USER IN YOUR DATABASE

		return redirect("/")
	except Exception as e:
		print(e)
		return redirect(url_for("google.login"))


if __name__ == "__main__":
	
	app.run(debug=True)
	
