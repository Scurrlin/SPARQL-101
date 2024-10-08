import argparse
from rdflib import Graph

g = Graph()
g.parse("wedding_playlist.rdf", format="turtle")

# Helper Functions

def convert_duration(duration_str):
    minutes, seconds = map(int, duration_str.split(":"))
    return f"{minutes} minutes, {seconds} seconds"

def get_all_artists():
    query = """
    SELECT DISTINCT ?artistName
    WHERE {
        ?track a schema1:MusicRecording;
            schema1:byArtist ?artist.
        ?artist schema1:name ?artistName.
    }
    ORDER BY ASC(?artistName)
    """
    results = g.query(query)
    return [str(row.artistName) for row in results]

# 1. Get the total playlist duration
# CLI Command: python3 sparql.py --query duration

def get_total_duration():
    query = """
    SELECT ?duration
    WHERE {
        ?track a schema1:MusicRecording;
            schema1:duration ?duration.
    }
    """
    total_duration_seconds = 0
    results = g.query(query)
    for row in results:
        minutes, seconds = map(int, row.duration.split(":"))
        total_duration_seconds += minutes * 60 + seconds

    total_minutes = total_duration_seconds // 60
    total_seconds = total_duration_seconds % 60
    print(f"Total Playlist Duration: {total_minutes} minutes, {total_seconds} seconds")

# 2. Get the total number of songs in the playlist
# CLI Command: python3 sparql.py --query total_songs

def get_total_songs():
    query = """
    SELECT (COUNT(?track) AS ?totalSongs)
    WHERE {
        ?track a schema1:MusicRecording.
    }
    """
    results = g.query(query)
    for row in results:
        print(f"Total Number of Songs: {row.totalSongs}")

# 3.) Get songs sorted by length in descending order
# CLI Command: python3 sparql.py --query length

def get_songs_sorted_by_length():
    query = """
    SELECT ?songTitle ?duration
    WHERE {
        ?track a schema1:MusicRecording;
            schema1:name ?songTitle;
            schema1:duration ?duration.
    }
    ORDER BY DESC(?duration)
    """
    results = g.query(query)
    for row in results:
        print(f"{row.songTitle}: {row.duration}")

# 4.) Get the longest song in the playlist
# CLI Command: python3 sparql.py --query longest

def get_longest_song():
    query = """
    SELECT ?songTitle ?duration
    WHERE {
        ?track a schema1:MusicRecording;
            schema1:name ?songTitle;
            schema1:duration ?duration.
    }
    ORDER BY DESC(?duration)
    LIMIT 1
    """
    results = g.query(query)
    for row in results:
        print(f"Longest Song: {row.songTitle}, Duration: {row.duration}")

# 5.) Get the shortest song in the playlist
# CLI Command: python3 sparql.py --query shortest

def get_shortest_song():
    query = """
    SELECT ?songTitle ?duration
    WHERE {
        ?track a schema1:MusicRecording;
            schema1:name ?songTitle;
            schema1:duration ?duration.
    }
    ORDER BY ASC(?duration)
    LIMIT 1
    """
    results = g.query(query)
    for row in results:
        print(f"Shortest Song: {row.songTitle}, Duration: {row.duration}")

# 6. Get songs longer than a specific duration
# CLI Command: python3 sparql.py --query longer_than --min_duration "4:00"

def get_songs_longer_than(duration):
    query = f"""
    SELECT ?songTitle ?duration
    WHERE {{
        ?track a schema1:MusicRecording;
            schema1:name ?songTitle;
            schema1:duration ?duration.
        FILTER (?duration > "{duration}")
    }}
    """
    results = g.query(query)
    for row in results:
        print(f"{row.songTitle}: {row.duration}")

# 7. Get songs grouped by album
# CLI Command: python3 sparql.py --query album

def get_songs_grouped_by_album():
    query = """
    SELECT ?albumTitle ?songTitle
    WHERE {
        ?track a schema1:MusicRecording;
            schema1:name ?songTitle;
            schema1:inAlbum ?album.
        ?album schema1:name ?albumTitle.
    }
    ORDER BY ?albumTitle
    """
    results = g.query(query)
    for row in results:
        print(f"{row.albumTitle}: {row.songTitle}")

# 8. Get songs grouped by artist
# CLI Command: python3 sparql.py --query artist

def get_songs_grouped_by_artist():
    query = """
    SELECT ?artistName ?songTitle
    WHERE {
        ?track a schema1:MusicRecording;
            schema1:name ?songTitle;
            schema1:byArtist ?artist.
        ?artist schema1:name ?artistName.
    }
    ORDER BY ?artistName
    """
    results = g.query(query)
    for row in results:
        print(f"{row.artistName}: {row.songTitle}")

# 9. Get artists sorted by most appearances in descending order
# CLI Command: python3 sparql.py --query by_appearance

def get_artists_by_appearance():
    query = """
    SELECT ?artistName (COUNT(?track) AS ?numSongs)
    WHERE {
        ?track a schema1:MusicRecording;
            schema1:byArtist ?artist.
        ?artist schema1:name ?artistName.
    }
    GROUP BY ?artistName
    ORDER BY DESC(?numSongs)
    """
    results = g.query(query)
    for row in results:
        print(f"{row.artistName}: {row.numSongs} songs")

# 10. Get all songs by a specific artist (manual input)
# CLI Command: python3 sparql.py --query by_artist

def get_songs_by_artist():
    artists = get_all_artists()
    print("Artists:")
    for i, artist in enumerate(artists, 1):
        print(f"{i}. {artist}")

    selected_artist = input("Enter the artist's name from the list above: ")

    query = f"""
    SELECT ?songTitle
    WHERE {{
        ?track a schema1:MusicRecording;
            schema1:name ?songTitle;
            schema1:byArtist ?artist.
        ?artist schema1:name "{selected_artist}".
    }}
    """
    results = g.query(query)
    print(f"Songs by {selected_artist}:")
    for row in results:
        print(f" - {row.songTitle}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SPARQL queries on your RDF playlist data.")
    
    parser.add_argument(
        "--query", 
        type=str, 
        required=True, 
        choices=["duration", "total_songs", "length", "longest", "shortest", "longer_than", "album", "artist", "by_appearance", "by_artist"], 
        help="Specify the query to run."
    )
    
    parser.add_argument(
        "--min_duration", 
        type=str, 
        help="Minimum duration in 'mm:ss' (required if 'longer_than' query is selected)"
    )

    args = parser.parse_args()

    if args.query == "duration":
        get_total_duration()
    elif args.query == "total_songs":
        get_total_songs()
    elif args.query == "length":
        get_songs_sorted_by_length()
    elif args.query == "longest":
        get_longest_song()
    elif args.query == "shortest":
        get_shortest_song()
    elif args.query == "longer_than":
        if args.min_duration:
            get_songs_longer_than(args.min_duration)
        else:
            print("Error: --min_duration is required for the 'longer_than' query.")
    elif args.query == "album":
        get_songs_grouped_by_album()
    elif args.query == "artist":
        get_songs_grouped_by_artist()
    elif args.query == "by_appearance":
        get_artists_by_appearance()
    elif args.query == "by_artist":
        get_songs_by_artist()
