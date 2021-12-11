#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List
import requests

BASE_URL = "https://api.spotify.com/v1/"


class Image:
    def __init__(self, url):
        self.url = url

    @classmethod
    def build_from_json(cls, image_json):
        return cls(image_json["url"])


class Playlist:
    """Playlist Object in Spotify API"""

    def __init__(self, name: str, id: str, href: str, images: List[Image]):
        self.name = name
        self.id = id
        self.href = href
        self.images = images

    @classmethod
    def build_from_json(cls, playlist_json):
        return cls(
            playlist_json["name"],
            playlist_json["id"],
            playlist_json["href"],
            [Image.build_from_json(image) for image in playlist_json["images"]],
        )


class User:
    """User object in the Spotify API"""

    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": "Bearer {}".format(self.token)}
        self.name = None
        self.id = None
        self._get_user_info()
        self.playlists = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def _get_user_info(self):
        try:
            r = requests.get(BASE_URL + "me", headers=self.headers)
            if r.status_code == 200:
                self.name = r.json()["display_name"]
                self.id = r.json()["id"]
        except Exception as e:
            print("[!] Error getting user's info [!]")
            print(e)

    def get_user_playlists(self) -> List[Playlist]:
        endpoint = "users/{}/playlists"
        r = requests.get(BASE_URL + endpoint.format(self.id), headers=self.headers)
        if r.status_code == 200:
            res = r.json()["items"]
            self.playlists = [Playlist.build_from_json(playlist) for playlist in res]
            return self.playlists
        else:
            print("EROOR")
            return None
