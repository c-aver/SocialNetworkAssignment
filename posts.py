"""This module holds the posts classes with their hierarchy"""
import logging
from abc import ABC, abstractmethod
from typing import Set, List, Tuple, Union
import matplotlib.pyplot as plt
import matplotlib.image as img
from notifications import NewCommentNotification, NewLikeNotification


class Post(ABC):
    """The abstract class for a post with its basic information"""
    _poster: 'User'

    _content: str

    _likes: Set['User'] = set()
    _comments: List[Tuple['User', str]] = []

    def __init__(self, poster: 'User', text: str):
        self._poster = poster
        self._content = text

    @abstractmethod
    def __str__(self) -> str:
        pass

    def like(self, liker: 'User') -> None:
        """Notifies the post that a user has liked it"""
        self._likes.add(liker)
        if liker != self._poster:
            self._poster.notify(NewLikeNotification(liker))

    def comment(self, commenter: 'User', text: str) -> None:
        """Notifies the post that a user has commented on it"""
        self._comments.append((commenter, text))
        if commenter != self._poster:
            self._poster.notify(NewCommentNotification(commenter, text))


class TextPost(Post):
    """A concrete class for a text post"""
    def __init__(self, poster: 'User', text: str):
        super().__init__(poster, text)
        print(self)

    def __str__(self) -> str:
        return (f"{self._poster.get_name()} published a post:\n"
                f"\"" + self._content + "\"\n")


class ImagePost(Post):
    """A concrete class for an image post"""
    def __init__(self, poster: 'User', file_path: str):
        super().__init__(poster, file_path)
        print(self)

    def display(self) -> None:
        """Attempts to display the image within the post"""
        try:
            plt.imshow(img.imread(self._content))
            plt.axis("off")
            plt.tight_layout()
            plt.show(block=False)
        except Exception as e:      # if we failed, that's fine # pylint: disable=broad-exception-caught
            logging.exception(e)
        print("Shows picture")

    def __str__(self) -> str:
        return f"{self._poster.get_name()} posted a picture\n"


class SalePost(Post):
    """A concrete class for a sale post"""
    # in the assignment output, the price changes type when a discount is applied
    __price: Union[int, float]
    __location: str
    __already_sold: bool

    def __init__(self, poster: 'User', text: str, price: int, location: str):
        super().__init__(poster, text)
        self.__price = price
        self.__location = location
        self.__already_sold = False
        print(self)

    def discount(self, discount: int, password: str) -> None:
        """Sets a discount on the sale, given the seller password"""
        self._poster.authenticate(password)
        if self.__already_sold:
            raise RuntimeError("Can't discount an already sold item.")
        self.__price -= self.__price * discount / 100
        print(f"Discount on {self._poster.get_name()} product! the new price is: {self.__price}")

    def sold(self, password: str) -> None:
        """Defines the sale as sold, given the seller password"""
        self._poster.authenticate(password)
        self.__already_sold = True
        print(f"{self._poster.get_name()}'s product is sold")

    def __str__(self) -> str:
        return (f"{self._poster.get_name()} posted a product for sale:\n"
                + ("Sold" if self.__already_sold else "For sale")
                + f"! {self._content}, price: {self.__price}, pickup from: {self.__location}\n")


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
