# Spotify Playlist SPARQL Queries

There is nothing better than a carefully curated playlist to help you stay focused when coding. Some of my personal favorite artists to listen to in this capacity are [A.L.I.S.O.N](https://open.spotify.com/artist/3gi5McAv9c0qTjJ5jSmbL0), [Jasper de Ceuster](https://open.spotify.com/artist/4E653XDFNhfX7sIlJWCiwb) (specifically his album [Memory Bank](https://open.spotify.com/album/0D9t03mcMVQpnToulPQFd7)), and [Lofi Girl](https://open.spotify.com/user/chilledcow).

However, there is another hidden benefit to great playlists: they are perfect subjects for ETL projects!

In this repository, I cover the entire process of extracting Spotify metadata from my wedding reception playlist, transforming it into RDF triples(subject-predicate-object), and finally loading the data as an RDF file that can be queried using SPARQL. I've also included istructions for how you can repeat this process on your own with any playlist of your choosing.

## Table of Contents
1. [Why SPARQL?](#why-sparql)
2. [RDF Data Structure](#rdf-data-structure)
3. [SPARQL Queries Used](#sparql-queries-used)
4. [Running the Queries](#running-the-queries)
5. [Examples](#examples)
6. [Setup Instructions](#setup-instructions)

## Why SPARQL?

SPARQL is a powerful language specifically designed for querying RDF data. RDF is a graph-based data format, meaning it stores information as a collection of triples, which represent relationships between different pieces of data. Each triple consists of:
- **Subject**: The resource being described (e.g., a track).
- **Predicate**: The property or characteristic of the resource (e.g., the track's duration or its artist).
- **Object**: The value of the property (e.g., "4:02" or "The Killers").

SPARQL queries are well-suited for querying this kind of data because they match patterns of triples in the RDF graph. SPARQL allows you to filter, sort, group, and manipulate RDF data to obtain meaningful insights.

## RDF Data Structure

The RDF data in this project is structured using the `schema1` namespace, which references the `schema.org` vocabulary. Here’s an example of how a track might be represented in RDF:

```ttl
@prefix schema1: <http://schema.org/> .

<spotify:track:07QlP7twNI81IsqhKLFiER> a schema1:MusicRecording ;
    schema1:byArtist <spotify:artist:4vGrte8FDu062Ntj0RsPiZ> ;
    schema1:duration "4:02" ;
    schema1:inAlbum <spotify:album:3cN3mENkACWuRCDOuQUtfw> ;
    schema1:name "Reverie" .
```

This RDF triple represents:
- A track identified by `<spotify:track:07QlP7twNI81IsqhKLFiER>`.
- It is a music recording (`a schema1:MusicRecording`).
- It is associated with an artist (`schema1:byArtist`), has a duration (`schema1:duration`), belongs to an album (`schema1:inAlbum`), and has a name (`schema1:name`).

## SPARQL Queries Used

Here are some examples of the SPARQL queries used in this project, along with explanations of why they are SPARQL queries:

1. **Get the Total Number of Songs**:
    ```sparql
    SELECT (COUNT(?track) AS ?totalSongs)
    WHERE {
        ?track a schema1:MusicRecording .
    }
    ```
    - This query counts all tracks that are classified as `schema1:MusicRecording`. The `SELECT` clause retrieves the count, and the `WHERE` clause specifies the pattern for matching the triples.

2. **Get the Total Playlist Duration**:
    ```sparql
    SELECT ?duration
    WHERE {
        ?track a schema1:MusicRecording ;
               schema1:duration ?duration .
    }
    ```
    - This query retrieves the `duration` for all tracks and calculates the total playlist duration. The `WHERE` clause matches triples where the subject is a music recording and has a `schema1:duration` predicate.

3. **Get Songs Grouped by Artist**:
    ```sparql
    SELECT ?artistName ?songTitle
    WHERE {
        ?track a schema1:MusicRecording ;
               schema1:name ?songTitle ;
               schema1:byArtist ?artist .
        ?artist schema1:name ?artistName .
    }
    ORDER BY ?artistName
    ```
    - This query retrieves songs and groups them by artist. The results are ordered by artist name, making it easy to see all songs associated with each artist.

## Running the Queries

To run any of the SPARQL queries, use the following command:

```bash
python3 sparql.py --query <query_name> [--additional_options]
```

For example, to get the total number of songs, run:

```bash
python3 sparql.py --query total_songs
```

To list songs longer than 4 minutes:

```bash
python3 sparql.py --query longer_than --min_duration "4:00"
```

## Examples

### Example 1: Get Songs Grouped by Artist
```bash
python3 sparql.py --query artist
```

**Output**:
```
The Killers:
 - Shot At The Night
 - Somebody Told Me
 - Read My Mind

Pharrell Williams:
 - Get Lucky
 - Happy
```

### Example 2: Get Artists Sorted by Most Appearances
```bash
python3 sparql.py --query by_appearance
```

**Output**:
```
1. The Weeknd: 5 songs
2. Imagine Dragons: 3 songs
3. Daft Punk: 2 songs
```

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies**:
   Make sure you have `rdflib` installed:
   ```bash
   pip install rdflib
   ```

3. **Run the Queries**:
   Use the `python3 sparql.py --query <query_name>` command to run any of the supported queries.