class Music:
    def __init__(self, id, title, artist, playlist_id):
        if not id or not title or not artist or not playlist_id:
            raise ValueError("All fields (id, title, artist, playlist_id) are required")
        self.id = id  # Unique ID para a música
        self.title = title
        self.artist = artist
        self.playlist_id = playlist_id  # Relacionamento com a playlist

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "playlist_id": self.playlist_id,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            artist=data.get("artist"),
            playlist_id=data.get("playlist_id")
        )
