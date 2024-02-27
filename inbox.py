"""This module holds the Inbox class for collecting notifications"""
from typing import List
from notifications import Notification, NewPostNotification, NewCommentNotification


class Inbox:
    """
    An observer class for collecting notifications for a user
    Only directly published to by the owner
    Indirectly published to by a post being commented on or like or by a user publishing a post
    """
    __owner_name: str  # the name of the inbox owner, for printing on new notification received
    __notifications: List[Notification]  # the list of notifications that arrived

    def __init__(self, owner_name: str):
        self.__owner_name = owner_name
        self.__notifications = []

    def notify(self, notification: Notification) -> None:
        """Adds a notification to the inbox"""
        self.__notifications.append(notification)  # append the new notification
        # by assignment definition, print that a notification arrived unless it is a new post
        if not isinstance(notification, NewPostNotification):
            print(f"notification to {self.__owner_name}: {notification}"
                  + (": " + notification.get_text()  # if it is a comment print content
                     if isinstance(notification, NewCommentNotification)
                     else ""))

    def print_all(self) -> None:
        """Prints all user notifications as a list"""
        for notification in self.__notifications:  # iterate through notifications and print them
            print(notification)
