import hashlib
from Post import *

def hash_str(s: str) -> bytes:
    return hashlib.sha256(s.encode("utf-8")).digest()


class User:
    name: str
    password_hash: bytes

    logged_in: bool

    followers: set['User']
    posts: list['Post']

    def __init__(self, name: str, password: str):
        self.name = name
        self.password_hash = hash_str(password)
        self.logged_in = True
        self.followers = set()

    # User name: Alice, Number of posts: 1, Number of followers: 2
    def __str__(self) -> str:
        return f"User name: {self.name}, Number of posts: {len(self.posts)}, Number of followers: {len(self.followers)}"

    def authenticate(self, password: str) -> None:
        if hash_str(password) != self.password_hash:
            raise ValueError(f"Incorrect password for {self.name}")

    def log_out(self) -> None:
        self.logged_in = False
        print(f"{self.name} disconnected")

    def log_in(self, password: str) -> None:
        self.authenticate(password)
        self.logged_in = True
        print(f"{self.name} connected")

    def follow(self, other: 'User') -> None:
        other.add_follower(self)

    def add_follower(self, other: 'User') -> None:
        self.followers.add(other)

    def publish_post(self, post_type: str, text: str, price: int = 0, location: str = ""):
        new_post: 'Post' = create_post(post_type, text, price, location)
