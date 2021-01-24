from dataclasses import dataclass


@dataclass
class User:
    email: str
    password: str

    def __repr__(self):
        return f"<User {self.email} ({self.id})>"
