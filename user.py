"""This module holds the User class"""
from __future__ import annotations
import hashlib
from typing import Set, List
from posts import Post, create_post
from notifications import NewPostNotification, Notification
from inbox import Inbox


def hash_str(s: str) -> bytes:
    """Hash a string using SHA-256"""
    return hashlib.sha256(s.encode("utf-8")).digest()


class User:
    """This class represents a user in the network"""
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

    def get_name(self) -> str:
        """Returns the user's name"""
        return self.__name

    def notify(self, notification: Notification) -> None:
        """Sends a notification to the user through its inbox"""
        self.__inbox.notify(notification)

    def __str__(self) -> str:
        return (f"User name: {self.__name}, "
                f"Number of posts: {len(self.__posts)}, "
                f"Number of followers: {len(self.__follower_inboxes)}")

    def authenticate(self, password: str) -> None:
        """Checks that the given password is correct for the user, otherwise raises ValueError"""
        if hash_str(password) != self.__pass_hash:
            raise ValueError(f"Incorrect password for {self.__name}")

    def log_out(self) -> None:
        """Logs the user out of the network"""
        self.__check_login("log out")
        self.__logged_in = False
        print(f"{self.__name} disconnected")

    def log_in(self, password: str) -> None:
        """Logs the user into of the network, given the correct password"""
        if self.__logged_in:
            raise RuntimeError("Attempted to log-in while already logged-in")
        self.authenticate(password)
        self.__logged_in = True
        print(f"{self.__name} connected")

    def follow(self, other: User) -> None:
        """Makes the user follow another user"""
        self.__check_login("follow a user")
        print(f"{self.__name} started following {other.__name}")    # pylint: disable=protected-access
        other._add_follower(self)                                   # pylint: disable=protected-access

    def _add_follower(self, other: User) -> None:
        self.__follower_inboxes.add(other.__inbox)                  # pylint: disable=protected-access

    def unfollow(self, other: User) -> None:
        """Makes the user unfollow another user"""
        self.__check_login("unfollow a user")
        print(f"{self.__name} unfollowed {other.__name}")           # pylint: disable=protected-access
        other._remove_follower(self)                                # pylint: disable=protected-access

    def _remove_follower(self, other: User) -> None:
        self.__follower_inboxes.remove(other.__inbox)               # pylint: disable=protected-access

    def publish_post(self, post_type: str, text: str, price: int = 0, location: str = "") -> Post:
        """Publishes a post by this user, given the post information"""
        self.__check_login("publish post")
        new_post: Post = create_post(self, post_type, text, price, location)
        self.__posts.append(new_post)
        # publish the post notification to all subscribers
        for inbox in self.__follower_inboxes:
            inbox.notify(NewPostNotification(self))
        return new_post

    def print_notifications(self) -> None:
        """Print the user's notifications"""
        self.__check_login("check notifications")
        print(f"{self.__name}'s notifications:")
        self.__inbox.print_all()

    def __check_login(self, action: str) -> None:
        """Makes sure the user is logged in, otherwise raises RuntimeError"""
        if not self.__logged_in:
            raise RuntimeError(f"Tried to {action} while not logged in")
