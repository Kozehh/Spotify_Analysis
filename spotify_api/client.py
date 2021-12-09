#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/python3

import requests
import os



CLIENT_ID = os.environ["SPOTIFY_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_SECRET"]
AUTH_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1/"
REDIRECT_URI = "http://localhost:8000/callback"
SCOPES = ["user-read-private"]


def get_access_token():
    response = requests.post(
        AUTH_URL,
        {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )

    # convert response to json
    auth_response = response.json()
    access_token = auth_response["access_token"]
    return access_token

def init_server():



# headers = {"Authorization": "Bearer {token}".format(token=access_token)}

# track_id = "6y0igZArWVi6Iz0rj35c1Y"

# r = requests.get(BASE_URL + "audio-features/" + track_id, headers=headers)


if __name__ == "__main__":
    get_access_token()
    init_server()
