

from bs4 import BeautifulSoup
import json
import requests
import spotipy
import spotipy.util as util




def find_css_class(input_soup, requested_class):
    output_soup = input_soup.find('div', class_=requested_class)
    if (output_soup):
        return output_soup.get_text().strip()
    else:
        return requested_class + " unavailable"


soup = BeautifulSoup(requests.get("http://smithstix.com/music").content, "html.parser")

listings = soup.find_all('div', {"class" : "event-row"})

for listing in listings:
    title = find_css_class(listing, "event-title")
    day = find_css_class(listing, "day-container")
    month = find_css_class(listing, "month-container")
    year = find_css_class(listing, "year-container")
    time = find_css_class(listing, "time-container")
    venue = find_css_class(listing, "event-venue")
    price = find_css_class(listing, "price")

    # print(title)
    # print(day)
    # print(month)
    # print(year)
    # print(time)
    # print(price)
    # print(venue)
    #
    # print(listing.prettify())
    # print("\n")


# Cool Libraries
# Beautiful Soup
# SQLite - CSV
# SMTP python
# Import SSL (Secure Sockets Layer)


with open("credentials.txt") as file:
    credentials = json.load(file)

client_id = credentials["client_id"]
client_secret = credentials["client_secret"]
redirect_uri = credentials["redirect_uri"]
scope = "user-library-read"
username = "me"

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

# if token:
#     sp = spotipy.Spotify(token)
#     results = sp.current_user_saved_tracks()
#     for item in results['items']:
#         track = item['track']
#         print(track['name'] + ' - ' + track['artists'][0]['name'])
# else:
#     print("Can't get token for", username)




# credentials_manager = SpotifyClientCredentials(client_id, client_secret, "http://localhost:8080")

# sp = spotipy.Spotify(credentials_manager)

# search_str = "Thrice"
# result = sp.search(search_str)
# print(result)

# import sys
# import spotipy
# import spotipy.util as util
#
# scope = 'user-library-read'
#
# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     print "Usage: %s username" % (sys.argv[0],)
#     sys.exit()
#
# token = util.prompt_for_user_token(username, scope)
#
# if token:
#     sp = spotipy.Spotify(auth=token)
#     results = sp.current_user_saved_tracks()
#     for item in results['items']:
#         track = item['track']
#         print track['name'] + ' - ' + track['artists'][0]['name']
# else:
#     print "Can't get token for", username

# token = util.prompt_for_user_token("me", "user-library-read", "00d93d999ee44e53a7264db918e03aa0", "e141ada5b1c343589c88b9edbd42bb38", "google.com")