from bs4 import BeautifulSoup
import datetime
import json
import os
import requests
import smtplib
import spotipy
import spotipy.util as util
import sqlite3
from sqlite3 import Error
import unicodedata


# ***************************************************************************
# ***************************************************************************

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


# ***************************************************************************
# ***************************************************************************

print(str(datetime.datetime.now()))

with open("credentials.txt") as file:
    credentials = json.load(file)

client_id = credentials["client_id"]
client_secret = credentials["client_secret"]
redirect_uri = credentials["redirect_uri"]
gmail_account = credentials["gmail_account"]
gmail_password = credentials["gmail_password"]
scope = "user-library-read"
username = "me"

# ***************************************************************************
# ***************************************************************************

print("Pulling song info from Spotify")
artists = set()

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

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

# ***************************************************************************
# ***************************************************************************

table_name = "oldListings"
field_name = "name"

try:
    database_path = os.getcwd() + "/database.sqlite"
    database = sqlite3.connect(database_path)
    database.execute("CREATE TABLE IF NOT EXISTS " + table_name + " (" + field_name + " TEXT PRIMARY KEY)")
except Error as e:
    print(e)

# ***************************************************************************
# ***************************************************************************

print("Scraping Smithstix")
soup = BeautifulSoup(requests.get("http://smithstix.com/music").content, "html.parser")

listings = soup.find_all('div', {"class": "event-row"})
concert_strings = []

for listing in listings:
    title = find_css_class(listing, "event-title")

    for artist in artists:
        if artist in title:
            query_results = database.execute(
                "SELECT * FROM " + table_name + " WHERE " + field_name + "='" + title + "'").fetchall()

            if len(query_results) == 0:
                day = find_css_class(listing, "day-container")
                month = find_css_class(listing, "month-container")
                year = find_css_class(listing, "year-container")
                time = find_css_class(listing, "time-container")
                venue = find_css_class(listing, "event-venue")
                price = find_css_class(listing, "price")

                concert_strings.append(
                    title + "\n" + month + " " + day + " " + year + " at " + time + "\n" + venue + "\n" + price + "\n\n")

                database.execute("INSERT INTO " + table_name + " (" + field_name + ") VALUES ('" + title + "')")

# ***************************************************************************
# ***************************************************************************

sender = gmail_account + "@gmail.com"
# receivers = ["Mahkumazahn@gmail.com", "8014718540@vtext.com"]
# receivers = ["8014718540@vtext.com"]
receivers = ["8016691177@vtext.com", "8014718540@vtext.com"]

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(gmail_account, gmail_password)


if len(concert_strings) == 0:
    print("No new concerts found")
else:
    print("One or more concerts found!")

for string in concert_strings:
    new_concerts = True
    message = "\r\nHello! I found a concert for you:\n\n"
    message += string
    message = unicodedata.normalize("NFD", message).encode("ascii", "ignore")

    try:
        server.sendmail(sender, receivers, message)
        print("Message Sent")
    except smtplib.SMTPException:
        print("Error: unable to send:\n" + message)


database.commit()
database.close()
server.quit()
