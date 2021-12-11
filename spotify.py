#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List
import requests

BASE_URL = "https://api.spotify.com/v1/"
token = None
headers = None


class Image:
    """Image object in Spotify API"""

    def __init__(self, url):
        self.url = url

    @classmethod
    def build_from_json(cls, image_json):
        return cls(image_json["url"])


class Artist:
    """Artist object in Spotify API"""

    def __init__(self, name: str, id: str, href: str):
        self.name = name
        self.id = id
        self.href = href

    @classmethod
    def build_from_json(cls, artist_json):
        return cls(
            artist_json["name"],
            artist_json["id"],
            artist_json["href"],
        )


class Track:
    """Track object in Spotify API"""

    def __init__(
        self, name: str, id: str, href: str, popularity: int, artists: List[Artist]
    ):
        self.name = name
        self.id = id
        self.href = href
        self.popularity = popularity
        self.artists = artists

    @classmethod
    def build_from_json(cls, track_json):
        return cls(
            track_json["name"],
            track_json["id"],
            track_json["href"],
            track_json["popularity"],
            [Artist.build_from_json(artist) for artist in track_json["artists"]],
        )


class Playlist:
    """Playlist object in Spotify API"""

    def __init__(
        self, name: str, id: str, href: str, images: List[Image], tracks: List[Track]
    ):
        self.name = name
        self.id = id
        self.href = href
        self.images = images
        self.tracks = tracks

    @classmethod
    def build_from_json(cls, playlist_json):
        return cls(
            playlist_json["name"],
            playlist_json["id"],
            playlist_json["href"],
            [Image.build_from_json(image) for image in playlist_json["images"]],
            [
                Track.build_from_json(track["track"])
                for track in playlist_json["tracks"]["items"]
            ],
        )

    @staticmethod
    def get_playlist(playlist_href: str):
        r = requests.get(playlist_href, headers=headers)
        if r.status_code == 200:
            return Playlist.build_from_json(r.json())


class User:
    """User object in the Spotify API"""

    def __init__(self, user_token):
        global token
        global headers
        token = user_token
        headers = {"Authorization": "Bearer {}".format(token)}
        self.name = None
        self.id = None
        self._get_user_info()
        self.playlists = None

    def _get_user_info(self):
        try:
            r = requests.get(BASE_URL + "me", headers=headers)
            if r.status_code == 200:
                self.name = r.json()["display_name"]
                self.id = r.json()["id"]
        except Exception as e:
            print("[!] Error getting user's info [!]")
            print(e)

    def get_user_playlists(self) -> List[Playlist]:
        endpoint = "users/{}/playlists"
        r = requests.get(BASE_URL + endpoint.format(self.id), headers=headers)
        if r.status_code == 200:
            items = r.json()["items"]

            self.playlists = [
                Playlist.get_playlist(playlist["href"]) for playlist in items
            ]
        else:
            print("EROOR")
            return None
