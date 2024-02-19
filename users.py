"""This module holds the User class"""
from __future__ import annotations
import hashlib
from typing import Set, List
from posts import Post, create_post
from notifications import NewPostNotification
from inbox import Inbox


def hash_str(to_hash: str) -> bytes:
    """Hash a string using SHA-256"""
    return hashlib.sha256(to_hash.encode("utf-8")).digest()


class User:
    """This class represents a user in the network"""
    __name: str             # the username
    __pass_hash: bytes      # the user's password's hash, for authentication

    __logged_in: bool       # whether the user is currently logged in

    __follower_inboxes: Set[Inbox]  # the follower inboxes, for notifying of a new post
    __posts: List['Post']           # the user's posts

    __inbox: Inbox                  # the user's notification inbox

    def __init__(self, name: str, password: str):
        self.__name = name
        self.__pass_hash = hash_str(password)   # save the hash of the given password
        self.__logged_in = True                 # initially user is logged in
        self.__follower_inboxes = set()         # initialize follower inboxes as empty set
        self.__posts = []                       # initialize posts as empty list
        self.__inbox = Inbox(self.__name)       # initialize inbox with a new inbox

    def get_name(self) -> str:
        """Returns the user's name"""
        return self.__name

    def get_inbox(self) -> Inbox:
        """Get the user's inbox, mainly in order to send them a notification"""
        return self.__inbox

    def __str__(self) -> str:
        return (f"User name: {self.__name}, "
                f"Number of posts: {len(self.__posts)}, "
                f"Number of followers: {len(self.__follower_inboxes)}")

    def authenticate(self, password: str) -> None:
        """Checks that the given password is correct for the user, otherwise raises ValueError"""
        if hash_str(password) != self.__pass_hash:  # compare given password hash with stored hash
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

    # the following 4 methods are for following and unfollowing
    # for each function there is one for the follower and one for the newly followed
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
        self.__check_login("publish post")      # make sure user is logged in
        new_post: Post = create_post(self, post_type, text, price, location)    # create a new post
        self.__posts.append(new_post)       # add the new post to the user's post list
        # publish the post notification to all subscribers
        for inbox in self.__follower_inboxes:
            inbox.notify(NewPostNotification(self))
        return new_post     # return the new post

    def print_notifications(self) -> None:
        """Print the user's notifications"""
        self.__check_login("check notifications")   # make sure user is logged in
        print(f"{self.__name}'s notifications:")
        self.__inbox.print_all()

    def __check_login(self, action: str) -> None:
        """
        This method makes sure the user is logged in when performing an action
        :param action: a string representing the actions being attempted
        :return: nothing, raises RuntimeError if user is not logged in
        """
        if not self.__logged_in:
            raise RuntimeError(f"Tried to {action} while not logged in")
