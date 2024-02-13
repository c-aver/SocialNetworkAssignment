"""This module holds the Inbox class for collecting notifications"""
from typing import List
from notifications import Notification, NewPostNotification, NewCommentNotification


class Inbox:
    """A subscriber class for collecting notifications for a user"""
    owner_name: str
    notifications: List[Notification]

    def __init__(self, owner_name: str):
        self.owner_name = owner_name
        self.notifications = []

    def notify(self, notification: Notification) -> None:
        """Adds a notification to the inbox"""
        self.notifications.append(notification)
        if not isinstance(notification, NewPostNotification):
            print(f"notification to {self.owner_name}: {notification}"
                  + (": " + notification.get_text()
                     if isinstance(notification, NewCommentNotification)
                     else ""))

    def print_all(self) -> None:
        """Prints all user notifications as a list"""
        for notification in self.notifications:
            print(notification)
