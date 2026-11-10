"""Discography display."""

import time

from itunes_api import ITunesAPI
from models import Album, Artist


class Discography:
    """Holds an artist and their albums and displays the full track listing."""

    def __init__(self, artist: Artist, albums: list[Album]) -> None:
        self.artist = artist
        self.albums = albums

    # Step 1: load_all_tracks

    def load_all_tracks(self, api: ITunesAPI) -> None:
        """Fetch tracks for every album via the API."""
        for album in self.albums:
            print(f'  Loading tracks for "{album.name}"...')
            album.tracks = api.get_tracks(album.collection_id)
            time.sleep(3)

    # Step 2: display

    def display(self) -> None:
        """Print every album followed by its track listing."""
        for album in self.albums:
            print(album)
            for track in album.tracks:
                print(
                    f"  {track.track_number:>2}. {track.name:<30} "
                    f"{track.duration_formatted}"
                )
            print()
