# module name must be in PascalCase for assignment # pylint: disable=invalid-name
"""This module introduces the SocialNetwork class, the main class in the project's logic"""
from typing import Dict, Union
from user import User


class SocialNetwork:
    """The class representing the entire social network, holds the main logic of the project"""
    __instance: 'SocialNetwork' = None

    __name: str
    __users: Dict[str, User] = {}

    def __init__(self, net_name: str):
        if self.__instance is not None:
            raise RuntimeError("Do not use constructor more than once, use instance() instead")
        self.__name = net_name
        self.__instance = self
        print(f"The social network {self.__name} was created!")

    def instance(self) -> 'SocialNetwork':
        """Return the singleton instance of SocialNetwork"""
        if self.__instance is None:
            self.__instance = SocialNetwork("Default")
        return self.__instance

    def __str__(self) -> str:
        return (f"{self.__name} social network:\n"
                + "\n".join([str(user) for user in self.__users.values()]) + "\n")

    def sign_up(self, username: str, password: str) -> User:
        """
        Created a new user and adds it to the network
        :param username: username for the new user
        :param password: password for the new user
        :return: the newly created user
        """
        if not 4 <= len(password) <= 8:
            raise ValueError(
                    f"Password must have between 4 and 8 characters, provided {len(password)}")
        if username in self.__users:
            raise ValueError(f"User with username {username} already exists")
        new_user: User = User(username, password)
        self.__users[username] = new_user
        return new_user

    def log_out(self, username: str) -> None:
        """Logs-out the user with given username"""
        user: Union[User, None] = self.__users.get(username)
        if user is None:
            raise RuntimeError(f"User {username} does not exist")
        user.log_out()

    def log_in(self, username: str, password: str) -> None:
        """Logs-in the user with given username, given the user's password"""
        user: Union[User, None] = self.__users.get(username)
        if user is None:
            raise RuntimeError(f"User {username} does not exist")
        user.log_in(password)
