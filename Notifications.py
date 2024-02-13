class Notification:
    other: 'User'

    def __init__(self, other: 'User'):
        self.other = other


class NewPostNotification(Notification):
    def __init__(self, poster):
        super().__init__(poster)

    def __str__(self) -> str:
        return f"{self.other.get_name()} has a new post"


class NewLikeNotification(Notification):
    def __init__(self, liker: 'User'):
        super().__init__(liker)

    def __str__(self) -> str:
        return f"{self.other.get_name()} liked your post"


class NewCommentNotification(Notification):
    __text: str

    def __init__(self, commenter: 'User', text: str):
        super().__init__(commenter)
        self.__text = text

    def get_text(self) -> str:
        return self.__text

    def __str__(self) -> str:
        return f"{self.other.get_name()} commented on your post"
