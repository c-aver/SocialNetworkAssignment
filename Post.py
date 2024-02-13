class Post:
    text: str

    likes: set['User'] = set()
    comments: list[tuple['User', str]] = []

    def like(self, liker: 'User'):
        self.likes.add(liker)

    def comment(self, commenter: 'User', text: str):
        self.comments.append = (commenter, text)


def create_post(post_type: str, text: str, price: int, location: str) -> Post:
    pass
