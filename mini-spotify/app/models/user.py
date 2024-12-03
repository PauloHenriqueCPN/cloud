class User:
    def __init__(self, id, username, email):
        if not id or not username or not email:
            raise ValueError("All fields (id, username, email) are required")
        self.id = id  # Unique ID (pode ser o email)
        self.username = username
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            username=data.get("username"),
            email=data.get("email")
        )
