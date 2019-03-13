
import time
import os
import spotipy
import spotipy.util as util

import requests
from bs4 import BeautifulSoup

def find_class(input_soup, requested_class):
    return input_soup.find('div', class_=requested_class).get_text().strip()


soup = BeautifulSoup(requests.get("http://smithstix.com/music").content, "html.parser")

# print(soup.prettify())
#
# print("\n")
# print("\n")
print("\n")

listings = soup.find_all('div', {"class" : "event-row"})

for listing in listings:

    title = find_class(listing, "event-title")
    day = find_class(listing, "day-container")
    month = find_class(listing, "month-container")
    year = find_class(listing, "year-container")
    time = find_class(listing, "time-container")

    print(title)
    print(day)
    print(month)
    print(year)
    print(time)


    # print(listing.prettify())
    print("\n")





# os.system("curl http://smithstix.com/music")

# driver = webdriver.Chrome()
# driver.get("http://smithstix.com/music")
#
# time.sleep(2)
#
# concerts = driver.find_elements_by_class_name("event-row")
#
# # concerts[0]
#
# for concert in concerts:
#     print(concert.find_element_by_class_name("date-outer").text)
#     # print(concert)
#
# print(len(concerts))
#
#
# time.sleep(2)
# driver.quit()

# Cool Libraries
# Beautiful Soup
# SQLite - CSV
# SMTP python
# Import SSL (Secure Sockets Layer)

# TODO Import from file for id and secret


scope = "user-library-read"
username = "me"

# token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
#
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