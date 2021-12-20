import re

def clean_data(lyrics):
    # List of words to replace
    rep = {
        "urlcopyembedcopy": "",
        "onembedshare": "",
        "\u2005": " ",
        "\u205f": " ",
        "\n": " ",
        "\'": "",
        '"': "",
        ",": "",
        "\.": "",
        "[0-9]*embedshare": "",
        "\[.*\]": " ",
        "\(.*\)": " ",
    }
    pattern = re.compile("|".join(rep))
    lyrics = lyrics.lower()
    lyrics = re.sub(pattern, " ", lyrics)
    return lyrics
