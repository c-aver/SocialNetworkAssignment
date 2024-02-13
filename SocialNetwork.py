from User import User
from typing import Dict


_instance = None


def instance():
    global _instance
    if _instance is None:
        _instance = SocialNetwork("Default")
    return _instance


class SocialNetwork:
    __name: str
    __users: Dict[str, User] = {}

    def __init__(self, net_name: str):
        global _instance
        if _instance is not None:
            raise RuntimeError("Do not use constructor more than once, use instance() instead")
        self.__name = net_name
        _instance = self
        print(f"The social network {self.__name} was created!")

    def __str__(self) -> str:
        return f"{self.__name} social network:\n" + "\n".join([str(user) for user in self.__users.values()]) + "\n"

    def sign_up(self, username: str, password: str) -> User:
        if not 4 <= len(password) <= 8:
            raise ValueError(f"Password must have between 4 and 8 characters, provided {len(password)}")
        if username in self.__users:
            raise ValueError(f"User with username {username} already exists")
        new_user: User = User(username, password)
        self.__users[username] = new_user
        return new_user

    def log_out(self, username: str) -> None:
        if self.__users.get(username) is None:
            raise RuntimeError(f"User {username} does not exist")
        self.__users.get(username).log_out()

    def log_in(self, username: str, password: str) -> None:
        if self.__users.get(username) is None:
            raise RuntimeError(f"User {username} does not exist")
        self.__users.get(username).log_in(password)
