from __future__ import annotations
import hashlib
from Posts import Post, create_post
from Notifications import NewPostNotification, Notification
from typing import Set, List
from Inbox import Inbox


def hash_str(s: str) -> bytes:
    """Hash a string using SHA-256"""
    return hashlib.sha256(s.encode("utf-8")).digest()


class User:
    __name: str
    __pass_hash: bytes

    __logged_in: bool

    __follower_inboxes: Set[Inbox]
    __posts: List['Post']

    __inbox: Inbox

    def __init__(self, name: str, password: str):
        self.__name = name
        self.__pass_hash = hash_str(password)
        self.__logged_in = True
        self.__follower_inboxes = set()
        self.__posts = []
        self.__inbox = Inbox(self.__name)

    def get_name(self):
        return self.__name

    def notify(self, notification: Notification):
        self.__inbox.notify(notification)

    def __str__(self) -> str:
        return (f"User name: {self.__name}, "
                f"Number of posts: {len(self.__posts)}, Number of followers: {len(self.__follower_inboxes)}")

    def authenticate(self, password: str) -> None:
        if hash_str(password) != self.__pass_hash:
            raise ValueError(f"Incorrect password for {self.__name}")

    def log_out(self) -> None:
        self.check_login("log out")
        self.__logged_in = False
        print(f"{self.__name} disconnected")

    def log_in(self, password: str) -> None:
        if self.__logged_in:
            raise RuntimeError("Attempted ")
        self.authenticate(password)
        self.__logged_in = True
        print(f"{self.__name} connected")

    def follow(self, other: User) -> None:
        self.check_login("follow a user")
        print(f"{self.__name} started following {other.__name}")
        other.add_follower(self)

    def add_follower(self, other: User) -> None:
        self.__follower_inboxes.add(other.__inbox)

    def unfollow(self, other: User) -> None:
        self.check_login("unfollow a user")
        print(f"{self.__name} unfollowed {other.__name}")
        other.remove_follower(self)

    def remove_follower(self, other: User) -> None:
        self.__follower_inboxes.remove(other.__inbox)

    def publish_post(self, post_type: str, text: str, price: int = 0, location: str = ""):
        self.check_login("publish post")
        new_post: Post = create_post(self, post_type, text, price, location)
        self.__posts.append(new_post)
        # publish the post notification to all subscribers
        for inbox in self.__follower_inboxes:
            inbox.notify(NewPostNotification(self))
        return new_post

    def print_notifications(self):
        self.check_login("check notifications")
        print(f"{self.__name}'s notifications:")
        self.__inbox.print_all()

    def check_login(self, action: str):
        if not self.__logged_in:
            raise RuntimeError(f"Tried to {action} while not logged in")
