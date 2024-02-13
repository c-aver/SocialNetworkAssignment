class Notification:
    other: 'User'
    def __init__(self, other: 'User'):
        self.other = other


class NewPostNotification(Notification):
    def __init__(self, poster):
        super().__init__(poster)

    def __str__(self):
        return f"{self.other.name} has a new post"


class NewLikeNotification(Notification):
    def __init__(self, liker: 'User'):
        super().__init__(liker)

    def __str__(self):
        return f"{self.other.name} liked your post"

class NewCommentNotification(Notification):
    def __init__(self, commenter: 'User'):
        super().__init__(commenter)

    def __str__(self):
        return f"{self.other.name} commented on your post"
