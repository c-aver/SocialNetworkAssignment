import hashlib
from Posts import *
from typing import Set, List
from Inbox import Inbox


def hash_str(s: str) -> bytes:
    return hashlib.sha256(s.encode("utf-8")).digest()


class User:
    name: str
    password_hash: bytes

    logged_in: bool

    follower_inboxes: Set[Inbox]
    posts: List['Post']

    inbox: Inbox

    def __init__(self, name: str, password: str):
        self.name = name
        self.password_hash = hash_str(password)
        self.logged_in = True
        self.follower_inboxes = set()
        self.posts = []
        self.inbox = Inbox(self.name)

    # User name: Alice, Number of posts: 1, Number of followers: 2
    def __str__(self) -> str:
        return (f"User name: {self.name}, "
                f"Number of posts: {len(self.posts)}, Number of followers: {len(self.follower_inboxes)}")

    def authenticate(self, password: str) -> None:
        if hash_str(password) != self.password_hash:
            raise ValueError(f"Incorrect password for {self.name}")

    def log_out(self) -> None:
        self.check_login("log out")
        self.logged_in = False
        print(f"{self.name} disconnected")

    def log_in(self, password: str) -> None:
        if self.logged_in:
            raise RuntimeError("Attempted ")
        self.authenticate(password)
        self.logged_in = True
        print(f"{self.name} connected")

    def follow(self, other: 'User') -> None:
        self.check_login("follow a user")
        print(f"{self.name} started following {other.name}")
        other.add_follower(self)

    def add_follower(self, other: 'User') -> None:
        self.follower_inboxes.add(other.inbox)

    def unfollow(self, other: 'User') -> None:
        self.check_login("unfollow a user")
        print(f"{self.name} unfollowed {other.name}")
        other.remove_follower(self)

    def remove_follower(self, other: 'User') -> None:
        self.follower_inboxes.remove(other.inbox)

    def publish_post(self, post_type: str, text: str, price: int = 0, location: str = ""):
        self.check_login("publish post")
        new_post: 'Post' = create_post(self, post_type, text, price, location)
        self.posts.append(new_post)
        for inbox in self.follower_inboxes:
            inbox.notify(NewPostNotification(self))
        return new_post

    def print_notifications(self):
        self.check_login("check notifications")
        print(f"{self.name}'s notifications:")
        self.inbox.print_all()

    def check_login(self, action: str):
        if not self.logged_in:
            raise RuntimeError(f"Tried to {action} while not logged in")
