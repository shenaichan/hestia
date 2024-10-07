from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
import json

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"

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

def play_artist(artist):
    access_token = refresh_access_token_if_needed()

    sp = Spotify(auth=access_token)

    # Search for Taylor Swift
    result = sp.search(q=artist, type='artist', limit=1)
    if len(result['artists']['items']) == 0:
        return "No artist found"

    artist_id = result['artists']['items'][0]['id']

    # Search for top tracks of the artist (Taylor Swift)
    top_tracks = sp.artist_top_tracks(artist_id)
    if len(top_tracks['tracks']) == 0:
        return "No tracks found"

    # Get the URI of the first top track
    track_uri = top_tracks['tracks'][0]['uri']

    # Get the user's available devices
    devices = sp.devices()
    if len(devices['devices']) == 0:
        return "No active devices found"
    
    for device in devices['devices']:
        if device['name'] == "Web Player (Firefox)":
            device_id = device['id']
            sp.start_playback(device_id=device_id, uris=[track_uri])
            return f"Playing {artist}"    

    return "Raspberry Pi not connected"
