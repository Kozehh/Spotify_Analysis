import lyricsgenius
import os

# Setup variable and genius object
GENIUS_CLIENT_ID = os.environ["GENIUS_ID"]
genius = lyricsgenius.Genius(GENIUS_CLIENT_ID)


def get_song_lyrics(song_name, artist):
    song = genius.search_song(song_name, artist)
    if song:
        return song.lyrics
    return ""
