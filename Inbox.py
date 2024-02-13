from typing import List
from Notifications import *


class Inbox:
    owner_name: str
    notifications: List[Notification]

    def __init__(self, owner_name: str):
        self.owner_name = owner_name
        self.notifications = []

    def notify(self, notification: Notification, comment: str = ""):
        self.notifications.append(notification)
        if not isinstance(notification, NewPostNotification):
            print(f"notification to {self.owner_name}: {notification}" + (": " + comment if comment != "" else ""))

    def print_all(self):
        for notification in self.notifications:
            print(notification)
