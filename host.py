from db import db, User
import bcrypt
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity,
								create_access_token, set_access_cookies, get_jwt, unset_jwt_cookies)
from flask import Flask, jsonify, render_template, request
import socket
import os
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError

from vosk import Model, KaldiRecognizer
import json
import subprocess
import zCmd

if not os.path.exists('zRec'):
	os.makedirs('zRec')


def convertAudio(filename):
	path = os.path.abspath(os.getcwd() + '/ffmpeg')
	si = subprocess.STARTUPINFO()
	si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	subprocess.call(
		f'{path} -nostdin -y -i "{filename}" -ac 1 "temp.wav"', startupinfo=si)


model = Model("model")
rec = KaldiRecognizer(model, 44100)


def speechRec(fname):
	convertAudio(fname)
	wf = open("temp.wav", "rb")
	wf.read(44)  # skip header

	while True:
		data = wf.read(4000)
		if len(data) == 0:
			break

		if rec.AcceptWaveform(data):
			res = json.loads(rec.Result())
			print(res['text'])

	res = json.loads(rec.FinalResult())
	return res['text']


# Constants
app = Flask(__name__)
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in your code!

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

jwt = JWTManager(app)

with app.app_context():
	db.create_all()


@app.route('/')
def main():
	return render_template("AI.html")


@app.route('/home')
def home():
	return jsonify({"msg": "HOME"}), 200


@app.route('/upload', methods=["POST"])
def upload():
	now = datetime.now()
	timestamp = str(int(datetime.timestamp(now)))
	data = request.files['audio']
	fname = timestamp + data.filename
	data.save(f'./zRec/{fname}')
	try:
		task = speechRec(f'./zRec/{fname}')
		if task:
			if zCmd.handleCmd(task):
				os._exit(1)
			return "yes"

		else:
			return jsonify({"msg": "Invalid Commands"})
	except Exception as e:
		print(e)
		return "nope"

@app.route('/todo', methods=["POST"])
# @jwt_required()
def todo():
	task = request.json.get('todo', None)
	if zCmd.handleCmd(task):
		os._exit(1)
	return jsonify({"msg": "exc"})


@app.route("/uname", methods=["POST"])
@jwt_required()
def uname():
	current_user = get_jwt_identity()
	return jsonify(current_user), 200


@app.after_request
def refresh_expiring_jwts(response):
	try:
		exp_timestamp = get_jwt()["exp"]
		now = datetime.now(timezone.utc)
		target_timestamp = datetime.timestamp(now + timedelta(minutes=10))
		if target_timestamp > exp_timestamp:
			access_token = create_access_token(identity=get_jwt_identity())
			set_access_cookies(response, access_token)
		return response

	except (RuntimeError, KeyError):
		return response


@app.route('/register', methods=['POST'])
def register():
	try:
		username = request.json.get('username', None)
		password = request.json.get('password', None)

		if not username:
			return 'Missing username', 400
		if not password:
			return 'Missing password', 400

		hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

		user = User(username=username, hash=hashed)
		db.session.add(user)
		db.session.commit()

		response = jsonify({"msg": "login successful"})
		access_token = create_access_token(identity={"username": username})
		response = jsonify({"msg": access_token})
		set_access_cookies(response, access_token)
		return response

	except IntegrityError:
		db.session.rollback()
		return 'User Already Exists', 400


@app.route('/login', methods=['POST'])
def login():
	try:
		username = request.json.get('username', None)
		password = request.json.get('password', None)

		if not username or not password:
			return jsonify({"msg": 'Missing Credentials'}), 400

		user = User.query.filter_by(username=username).first()
		if not user or not bcrypt.checkpw(password.encode('utf-8'), user.hash):
			return jsonify({"msg": 'Invalid Credentials'}), 400

		response = jsonify({"msg": "login successful"})
		access_token = create_access_token(identity={"username": username})
		response = jsonify({"msg": access_token})
		set_access_cookies(response, access_token)
		return response

	except AttributeError:
		return 'Provide an username and Password in JSON format in the request body', 400


@app.route("/logout", methods=["POST"])
def logout():
	response = jsonify({"msg": "logout successful"})
	unset_jwt_cookies(response)
	return response


def mainf():
	_ = os.system('cls')
	hostname = socket.gethostname()
	IPAddr = socket.gethostbyname_ex(hostname)[2][-1]
	# os.system(f"start http://{IPAddr}:5000")
	# app.run(host=IPAddr)
	app.run(host=IPAddr, debug=True, use_reloader=False)


if __name__ == '__main__':
	mainf()
