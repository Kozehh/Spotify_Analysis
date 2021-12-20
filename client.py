import pandas as pd
import requests
import pickle

from spotify import User
from genius import get_song_lyrics
from process_data import clean_data
from concurrent.futures import ThreadPoolExecutor


def get_user() -> User:
    r = requests.get("http://localhost:8000/user")
    user = pickle.loads(r.content)
    return user


def manipulate(user):
    df = pd.DataFrame(user.playlists[1].tracks)
    print(df.head())

def get_songs_lyrics(songs, thread):
    songslyrics = ""
    songlyrics = ""
    print(f"In thread {thread}")
    for song in songs:
        songlyrics = get_song_lyrics(song.name, song.artists[0].name)
        songslyrics += clean_data(songlyrics)
    return songslyrics

if __name__ == "__main__":
    user = get_user()
    songlyrics = ""
    workers = 20
    chunks = len(user.playlists[1].tracks) // workers
    chunked_list = [user.playlists[1].tracks[i:i+chunks] for i in range(0, len(user.playlists[1].tracks), chunks)]
    ret = []
    with ThreadPoolExecutor(max_workers=workers) as exeggcutor:
        for i in range(workers):
            future = exeggcutor.submit(get_songs_lyrics, chunked_list[i], i)
            ret.append(future)

    all_playlist_lyrics = ""
    for i in ret:
        all_playlist_lyrics += i.result()
    print(all_playlist_lyrics)
