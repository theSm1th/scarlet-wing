import time
from subprocess import check_output

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import lcd_lib
import logging

import spCreds as spotify

logging.basicConfig(filename="log.log", level=logging.INFO)

lcd = lcd_lib.lcd()
lcd.lcd_clear()
songString = ""

isPlaying = False
s_remaining_2int = 0
min_remaining = 0


sp = spotipy.Spotify(SpotifyOAuth(scope="user-read-currently-playing", client_id=spotify.creds["client_id"],  client_secret=spotify.creds["client_secret"], redirect_uri=spotify.creds["redir"], open_browser=False).get_access_token(as_dict=False))


def displayDTT(display):
    lcd.lcd_display_string(time.strftime("%H:%M %d/%m", time.localtime()) + " {}".format(display), 1)

def twoInt(intInput):
    if len(str(intInput)) < 2:
        newInt = str(0) + str(intInput)
        return newInt
    else:
        return intInput


def getSongAttrib():        
    global songString, isPlaying, s_remaining_2int, min_remaining
    count = 0
    data = sp.current_user_playing_track()
    songString = ""
    artistString = ""

    try:

        for _ in data["item"]["artists"]:

            artistString = artistString + " & " + data["item"]["artists"][count]["name"]
            count += 1
            isPlaying = bool(data["is_playing"])
            songString = artistString[3:] + " - " + data["item"]["name"]

            ms_remaining = data["item"]["duration_ms"] - data["progress_ms"]
            s_remaining = int(ms_remaining / 1000)
            min_remaining = int(s_remaining / 60)
            s_remaining_2int = twoInt(int(s_remaining % 60))

    except TypeError:

        pass


while True:

    while isPlaying:

        getSongAttrib()
        displayedString = songString
        if len(displayedString) > 16:

            displayedString = songString + "   "

            for i in range(0, len(displayedString)):
                getSongAttrib()
                displayDTT("{}:{}".format(min_remaining, s_remaining_2int))
                lcd.lcd_display_string(displayedString[0:16], 2)
                displayedString = displayedString[1:] + displayedString[0]
                time.sleep(0.5)
                displayDTT("{}:{}".format(min_remaining, s_remaining_2int))

        else:

            if len(displayedString) == 15:

                displayedString = songString + " "
                lcd.lcd_display_string(displayedString, 2)
                displayDTT("{}:{}".format(min_remaining, s_remaining_2int))
                time.sleep(0.5)

            else:

                displayedStringDiff = 8 - len(displayedString) / 2
                displayedString = displayedStringDiff * " " + displayedString
                lcd.lcd_display_string(displayedString, 2)
                displayDTT("{}:{}".format(min_remaining, s_remaining_2int))
                time.sleep(0.5)

    while not isPlaying:
        getSongAttrib()
        cpu_temp = check_output(["/opt/vc/bin/vcgencmd", "measure_temp"]).decode("utf-8")[5:9]
        lcd.lcd_display_string(time.strftime("%H:%M %d/%m", time.localtime()) + f" {cpu_temp}", 1)
        lcd.lcd_display_string("TheSmith:Rosetta", 2)
        time.sleep(0.5)
