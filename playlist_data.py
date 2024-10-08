import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SPOTIFY_PLAYLIST_ID = os.getenv('SPOTIFY_PLAYLIST_ID')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-read-private"
))

playlist = sp.playlist(SPOTIFY_PLAYLIST_ID)

print(f"Playlist Name: {playlist['name']}")
print(f"Total Tracks: {playlist['tracks']['total']}")

def convert_duration(duration_ms):
    minutes = duration_ms // 60000
    seconds = (duration_ms % 60000) // 1000
    return f"{minutes}:{seconds:02d}"

for track in playlist['tracks']['items']:
    track_info = track['track']
    track_duration = convert_duration(track_info['duration_ms'])
    print(f"Track Name: {track_info['name']}")
    print(f"Artist: {track_info['artists'][0]['name']}")
    print(f"Album: {track_info['album']['name']}")
    print(f"Duration: {track_duration}")
    print('---')