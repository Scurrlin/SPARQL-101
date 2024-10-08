import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from rdflib import Graph, URIRef, Literal, Namesapce
from rdflib.namespace import RDF, RDFS

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SPOTIFY_PLAYLIST_ID = os.getenv('SPOTIFY_PLAYLIST_ID')

sp = spotipy.Spotify(auth_manaer=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-read-private"
))

def convert_duration(duration_ms):
    minutes = duration_ms // 60000
    seconds = (duration_ms % 60000) // 1000
    return f"{minutes}:{seconds:02d}"

g = Graph()

SPOTIFY = Namespace("http://www.spotify.com/ontologies/")
SCHEMA = Namespace("http://schema.org/")

g.bind("spotify", SPOTIFY)
g.bind("schema", SCHEMA)

playlist = sp.playlist(SPOTIFY_PLAYLIST_ID)

for track in playlist['tracks']['items']:
    track_info = track['track']
    track_uri = URIRef(track_info['uri'])
    
    g.add((track_uri, RDF.type, SCHEMA.MusicRecording))
    g.add((track_uri, SCHEMA.name, Literal(track_info['name'])))
    g.add((track_uri, SCHEMA.duration, Literal(convert_duration(track_info['duration_ms']))))
    
    artist_uri = URIRef(track_info['artists'][0]['uri'])
    g.add((track_uri, SCHEMA.byArtist, artist_uri))
    g.add((artist_uri, SCHEMA.name, Literal(track_info['artists'][0]['name'])))
    
    album_uri = URIRef(track_info['album']['uri'])
    g.add((track_uri, SCHEMA.inAlbum, album_uri))
    g.add((album_uri, SCHEMA.name, Literal(track_info['album']['name'])))
    
g.serialize(destination="wedding_playlist.rdf", format="turtle")

print("RDF data generated and saved to wedding_playlist.rdf")