# module name must be in PascalCase for assignment # pylint: disable=invalid-name
"""This module introduces the SocialNetwork class, the main class in the project's logic"""
from __future__ import annotations
from typing import Dict, Union
from users import User


class SocialNetwork:
    """The class representing the entire social network, holds the main logic of the project"""
    __instance: Union[SocialNetwork, None] = None  # the singleton instance of this class

    __name: str  # the name of the social network
    __users: Dict[str, User]  # the user data structure

    def __new__(cls, net_name: str):
        if cls.__instance is None:  # if singleton instance does not exists
            cls.__instance = super().__new__(cls)  # create it
        cls.__instance.__name = net_name  # initialize values
        cls.__instance.__users = {}
        print(f"The social network {cls.__instance.__name} was created!")
        return cls.__instance

    def instance(self) -> SocialNetwork:
        """Return the singleton instance of SocialNetwork"""
        if self.__instance is None:  # if an instance was not created yet
            self.__instance = SocialNetwork("Default")  # create a new one with some default name
        return self.__instance  # return the singleton instance

    def __str__(self) -> str:
        return (f"{self.__name} social network:\n"  # print the network header and then all users
                + "\n".join([str(user) for user in self.__users.values()]) + "\n")

    def sign_up(self, username: str, password: str) -> User:
        """
        Creates a new user and adds it to the network
        :param username: username for the new user
        :param password: password for the new user
        :return: the newly created user
        """
        if not 4 <= len(password) <= 8:  # enforce password requirement
            raise ValueError(
                f"Password must have between 4 and 8 characters, provided {len(password)}")
        if username in self.__users:  # make sure username is not taken
            raise ValueError(f"User with username {username} already exists")
        new_user: User = User(username, password)  # create new user with parameters
        self.__users[username] = new_user  # add the new user to the users database
        return new_user  # return the new user

    def log_out(self, username: str) -> None:
        """Logs-out the user with given username"""
        user: Union[User, None] = self.__users.get(username)
        if user is None:  # make sure gotten user exists
            raise RuntimeError(f"User {username} does not exist")
        user.log_out()

    def log_in(self, username: str, password: str) -> None:
        """Logs-in the user with given username, given the user's password"""
        user: Union[User, None] = self.__users.get(username)
        if user is None:  # make sure gotten user exists
            raise RuntimeError(f"User {username} does not exist")
        user.log_in(password)
