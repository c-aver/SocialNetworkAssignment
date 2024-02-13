from User import User


_instance = None


def instance():
    return _instance


class SocialNetwork:

    name: str
    users: dict[str, User] = {}

    def __init__(self, net_name: str):
        global _instance
        if _instance is not None:
            raise RuntimeError("Do not use constructor more than once, use instance() instead")
        self.name = net_name
        _instance = self
        print(f"The social network {self.name} was created!")

    def sign_up(self, username: str, password: str) -> User:
        if not 4 <= len(password) <= 8:
            raise ValueError(f"Password must have between 4 and 8 characters, provided {len(password)}")
        if username in self.users:
            raise ValueError(f"User with username {username} already exists")
        new_user: User = User(username, password)
        self.users[username] = new_user
        return new_user

    def log_out(self, username: str) -> None:
        if username not in self.users:
            raise RuntimeError(f"User {username} does not exist")
        self.users.get(username).log_out()

    def log_in(self, username: str, password: str) -> None:
        if username not in self.users:
            raise RuntimeError(f"User {username} does not exist")
        self.users.get(username).log_in(password)
