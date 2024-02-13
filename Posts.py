import logging

from Notifications import *
from typing import Set, List, Tuple, Union
import matplotlib.pyplot as plt
import matplotlib.image as img


class Post:
    poster: 'User'

    content: str

    likes: Set['User'] = set()
    comments: List[Tuple['User', str]] = []

    def __init__(self, poster: 'User', text: str):
        self.poster = poster
        self.content = text

    def like(self, liker: 'User') -> None:
        self.likes.add(liker)
        if liker != self.poster:
            self.poster.notify(NewLikeNotification(liker))

    def comment(self, commenter: 'User', text: str) -> None:
        self.comments.append((commenter, text))
        if commenter != self.poster:
            self.poster.notify(NewCommentNotification(commenter, text))


class TextPost(Post):
    def __init__(self, poster: 'User', text: str):
        super().__init__(poster, text)
        print(self)

    def __str__(self) -> str:
        return (f"{self.poster.get_name()} published a post:\n"
                f"\"" + self.content + "\"\n")


class ImagePost(Post):
    def __init__(self, poster: 'User', text: str):
        super().__init__(poster, text)
        print(self)

    def display(self) -> None:
        try:
            plt.imshow(img.imread(self.content))
            plt.axis("off")
            plt.tight_layout()
            plt.show(block=False)
        except Exception as e:
            logging.exception(e)
            pass    # if something went wrong, just skip the displaying
        print("Shows picture")

    def __str__(self) -> str:
        return f"{self.poster.get_name()} posted a picture\n"


class SalePost(Post):
    price: Union[int, float]
    location: str
    already_sold: bool

    def __init__(self, poster: 'User', text: str, price: int, location: str):
        super().__init__(poster, text)
        self.price = price
        self.location = location
        self.already_sold = False
        print(self)

    def discount(self, discount: int, password: str) -> None:
        self.poster.authenticate(password)
        self.price = self.price - self.price*discount/100
        print(f"Discount on {self.poster.get_name()} product! the new price is: {self.price}")

    def sold(self, password: str) -> None:
        self.poster.authenticate(password)
        self.already_sold = True
        print(f"{self.poster.get_name()}'s product is sold")

    def __str__(self) -> str:
        return (f"{self.poster.get_name()} posted a product for sale:\n"
                + ("Sold" if self.already_sold else "For sale")
                + f"! {self.content}, price: {self.price}, pickup from: {self.location}\n")


def create_post(poster: 'User', post_type: str, text: str, price: int, location: str) -> Post:
    """
    Factory method to create an instance of Post
    :param poster: user to be defined as the poster
    :param post_type: the type of the post, one of ("Text", "Image", "Sale")
    :param text: the content of the post
    :param price: for SalePost - the initial price
    :param location: for SalePost - the location
    :return: the newly created Post
    """
    new_post: Post
    if post_type == "Text":
        new_post = TextPost(poster, text)
    elif post_type == "Image":
        new_post = ImagePost(poster, text)
    elif post_type == "Sale":
        new_post = SalePost(poster, text, price, location)
    else:
        raise ValueError(f"Unknown post type: {post_type}")
    return new_post
