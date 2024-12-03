class Playlist:
    def __init__(self, id, name, user_id):
        if not id or not name or not user_id:
            raise ValueError("All fields (id, name, user_id) are required")
        self.id = id  # Unique ID para a playlist
        self.name = name
        self.user_id = user_id  # Relacionamento com o usuário

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            user_id=data.get("user_id")
        )
