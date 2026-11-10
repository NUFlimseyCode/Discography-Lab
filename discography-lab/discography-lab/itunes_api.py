"""Client for the iTunes Search API."""

import requests

from models import Album, Artist, Track

SEARCH_URL = "https://itunes.apple.com/search"
LOOKUP_URL = "https://itunes.apple.com/lookup"
COUNTRY = "GB"


class ITunesAPI:
    """Wraps all HTTP interaction with the iTunes Search API.

    Every method in this class should:
    - use requests.get() with a timeout of 10 seconds
    - call response.raise_for_status() to catch HTTP errors
    - parse the JSON with response.json()
    - return model objects, never raw dictionaries
    """

    # Step 1: search_artist

    def search_artist(self, term: str, limit: int = 5) -> list[Artist]:
        """Search for artists matching *term*."""
        response = requests.get(
            SEARCH_URL,
            params={
                "term": term,
                "entity": "musicArtist",
                "country": COUNTRY,
                "limit": limit,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        artists = []
        for item in data["results"]:
            artists.append(Artist.from_dict(item))
        return artists

    # Step 2: get_albums

    def get_albums(self, artist_id: int) -> list[Album]:
        """Fetch albums for the given artist ID."""
        response = requests.get(
            LOOKUP_URL,
            params={
                "id": artist_id,
                "entity": "album",
                "country": COUNTRY,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        albums = []
        for item in data["results"]:
            if item["wrapperType"] == "collection":
                albums.append(Album.from_dict(item))
        return albums

    # Step 3: get_tracks

    def get_tracks(self, collection_id: int) -> list[Track]:
        """Fetch tracks for the given album (collection) ID."""
        response = requests.get(
            LOOKUP_URL,
            params={
                "id": collection_id,
                "entity": "song",
                "country": COUNTRY,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        tracks = []
        for item in data["results"]:
            if item["wrapperType"] == "track":
                tracks.append(Track.from_dict(item))
        return tracks
