# Cool Libraries
# Beautiful Soup
# SQLite - CSV
# SMTP python
# Import SSL (Secure Sockets Layer)

from bs4 import BeautifulSoup
import json
import requests
import spotipy
import spotipy.util as util

#***************************************************************************
#***************************************************************************

def add_artists(input_songs, artists_list):
    for song in input_songs['items']:
        _artist = song['track']['artists'][0]['name']
        artists_list.add(_artist)

def find_css_class(input_soup, requested_class):
    _output_soup = input_soup.find('div', class_=requested_class)
    if _output_soup:
        return _output_soup.get_text().strip()
    else:
        return requested_class + " unavailable"

#***************************************************************************
#***************************************************************************

with open("credentials.txt") as file:
    credentials = json.load(file)

client_id = credentials["client_id"]
client_secret = credentials["client_secret"]
redirect_uri = credentials["redirect_uri"]
scope = "user-library-read"
username = "me"

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

artists = set()

if token:
    sp = spotipy.Spotify(token)
    offset = 0
    while True:
        songs = sp.current_user_saved_tracks(50, offset)
        if len(songs['items']) == 0:
            break

        add_artists(songs, artists)
        offset += 50

    offset = 0
    while True:
        playlists = sp.current_user_playlists(50, offset)
        if len(playlists['items']) == 0:
            break

        for playlist in playlists['items']:
            songs = sp.user_playlist(sp.current_user()['display_name'], playlist['id'], fields="tracks")['tracks']

            add_artists(songs, artists)

        offset += 50

else:
    print("Can't get token for", username)

#***************************************************************************
#***************************************************************************

soup = BeautifulSoup(requests.get("http://smithstix.com/music").content, "html.parser")

listings = soup.find_all('div', {"class": "event-row"})

for listing in listings:
    title = find_css_class(listing, "event-title")

    for artist in artists:
        if artist in title:
            day = find_css_class(listing, "day-container")
            month = find_css_class(listing, "month-container")
            year = find_css_class(listing, "year-container")
            time = find_css_class(listing, "time-container")
            venue = find_css_class(listing, "event-venue")
            price = find_css_class(listing, "price")

            print(title)
            print(month + " " + day + " " + year + " at " + time)
            print(venue)
            print(price)
            print()







