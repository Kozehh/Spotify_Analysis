#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import os
import urllib
from flask import request, Flask, redirect, render_template
from flask_socketio import SocketIO
from spotify import User

app = Flask(__name__)
socketio = SocketIO(app)

SERVER_PORT = "8000"
SERVER_HOST = "http://localhost"
SERVER_ADDR = f"{SERVER_HOST}:{SERVER_PORT}"
CLIENT_ID = os.environ["SPOTIFY_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_SECRET"]
TOKEN_URL = "https://accounts.spotify.com/api/token"
AUTH_URL = "https://accounts.spotify.com/authorize?"
REDIRECT_URI = f"{SERVER_ADDR}/callback"
SCOPES = ["user-read-private", "user-read-email"]


def init_server():
    print(f"[INFO] Please Login at {SERVER_ADDR}/login")
    socketio.run(app=app, host="", port=8000)


@app.route("/dashboard")
def dashboard():
    # Va chercher informations du compte spotify
    user = User(os.environ["SPOTIFY_TOKEN"])
    user_playlists = user.get_user_playlists()
    
    return user.name
    # return render_template("dashboard.html", title="Dashboard")


@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")
    if state:
        params = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        }
        r = requests.post(TOKEN_URL, data=params, auth=(CLIENT_ID, CLIENT_SECRET))
        token = r.json()["access_token"]
        os.environ["SPOTIFY_TOKEN"] = token
        return redirect(f"{SERVER_ADDR}/dashboard")


@app.route("/login")
def login():
    params = {
        "grant_type": "client_credentials",
        "response_type": "code",
        "scope": " ".join([str(scope) for scope in SCOPES]),
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "state": 100,
    }
    encoded_params = urllib.parse.urlencode(params)
    return redirect(AUTH_URL + encoded_params)


if __name__ == "__main__":
    init_server()
