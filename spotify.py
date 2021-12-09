#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

BASE_URL = "https://api.spotify.com/v1/"


class User:
    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": "Bearer {}".format(self.token)}
        self.name = None
        self.id = None
        self._get_user_info()
        # return self.get_user_info()

    def _get_user_info(self):
        try:
            r = requests.get(BASE_URL + "me", headers=self.headers)
            self.name = r.json()["display_name"]
            self.id = r.json()["id"]
        except Exception as e:
            print("[!] Error getting user's info [!]")
            print(e)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
