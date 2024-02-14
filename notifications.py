"""Holds the various notification classes and their hierarchy"""
from abc import ABC, abstractmethod


class Notification(ABC):                        # pylint: disable=too-few-public-methods
    """The abstract class that holds the info common to all notifications"""
    _other: 'User'  # the other user connected to the notification (meaning dependent on class)

    def __init__(self, other: 'User'):
        self._other = other

    @abstractmethod
    def __str__(self) -> str:
        pass


class NewPostNotification(Notification):        # pylint: disable=too-few-public-methods
    """Represents a new post notification for followers"""

    def __str__(self) -> str:
        return f"{self._other.get_name()} has a new post"


class NewLikeNotification(Notification):        # pylint: disable=too-few-public-methods
    """Represents a new like notification for the poster"""

    def __str__(self) -> str:
        return f"{self._other.get_name()} liked your post"


class NewCommentNotification(Notification):     # pylint: disable=too-few-public-methods
    """Represents a new comment notification for the poster"""
    __text: str

    def __init__(self, commenter: 'User', text: str):
        super().__init__(commenter)
        self.__text = text

    def get_text(self) -> str:  # for printing upon new notification
        """Returns the text of the comment being notified on"""
        return self.__text

    def __str__(self) -> str:
        return f"{self._other.get_name()} commented on your post"
