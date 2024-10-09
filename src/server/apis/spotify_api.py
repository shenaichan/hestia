from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
import json



# # DEBUG
# from pprint import pprint
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())



SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = "http://localhost:5000/"



def get_token_info():
    with open('apis/spotify_tokens.json', 'r') as f:
        return json.load(f)

def save_token_info(token_info):
    with open('apis/spotify_tokens.json', 'w') as f:
        json.dump(token_info, f)



def refresh_access_token_if_needed():
    token_info = get_token_info()
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope="user-modify-playback-state user-read-playback-state")
    
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        save_token_info(token_info)

    return token_info['access_token']



def play_music(query):
    access_token = refresh_access_token_if_needed()

    sp = Spotify(auth=access_token)

    devices = sp.devices()
    if len(devices['devices']) == 0:
        return "No active devices found."
    
    for device in devices['devices']:
        if device['name'] == "Web Player (Firefox)":
            device_id = device['id']

            result = sp.search(q=query, type='track', limit=1)
            track = result['tracks']['items'][0]
            track_uri = track['uri']

            sp.start_playback(device_id=device_id, uris=[track_uri])

            artists = track['artists']
            artist_names = ""
            if len(artists) == 1:
                artist_names = artists[0]['name']
            elif len(artists) == 2:
                artist_names = artists[0]['name'] + " and " + artists[1]['name']
            else:
                for idx, artist in enumerate(artists):
                    if idx == len(artists) - 1:
                        artist_names += "and " + artist['name']
                    else:
                        artist_names += artist['name'] + ", "
            
            song_name = track['name']
            
            return f"Playing {song_name} by {artist_names}."    

    return "Raspberry Pi not connected."

def pause_music():
    access_token = refresh_access_token_if_needed()

    sp = Spotify(auth=access_token)

    devices = sp.devices()
    if len(devices['devices']) == 0:
        return "No active devices found."
    
    for device in devices['devices']:
        if device['name'] == "Web Player (Firefox)":
            device_id = device['id']
            sp.pause_playback(device_id=device_id)
            return "Pausing music."    

    return "Raspberry Pi not connected."

# play_music("juna clairo")