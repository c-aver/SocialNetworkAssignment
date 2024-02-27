"""This module holds the posts classes with their hierarchy"""
from __future__ import annotations
from typing import TYPE_CHECKING, Set, List, Tuple, Union
import logging
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import matplotlib.image as img
from notifications import NewCommentNotification, NewLikeNotification

if TYPE_CHECKING:
    from users import User


class Post(ABC):
    """The abstract class for a post with its basic information"""
    _poster: User  # the user that posted the post

    _content: str  # the content, either text or image file path

    _likes: Set[User]  # the set of users that liked the post
    _comments: List[Tuple[User, str]]  # the list of comments, commenter and content

    def __init__(self, poster: User, text: str):
        self._poster = poster
        self._content = text
        self._likes = set()
        self._comments = []

    @abstractmethod
    def __str__(self) -> str:
        pass

    def like(self, liker: User) -> None:
        """Notifies the post that a user has liked it"""
        self._likes.add(liker)  # add the liker to the likers set
        if liker != self._poster:  # if not self-like, notify the poster
            self._poster.get_inbox().notify(NewLikeNotification(liker))

    def comment(self, commenter: User, text: str) -> None:
        """Notifies the post that a user has commented on it"""
        self._comments.append((commenter, text))  # add the commenter and text to the comments
        if commenter != self._poster:  # if not self-comment, notify the poster
            self._poster.get_inbox().notify(NewCommentNotification(commenter, text))


class TextPost(Post):
    """A concrete class for a text post"""

    def __init__(self, poster: User, text: str):
        super().__init__(poster, text)
        print(self)

    def __str__(self) -> str:
        return (f"{self._poster.get_name()} published a post:\n"
                f"\"" + self._content + "\"\n")


class ImagePost(Post):
    """A concrete class for an image post"""

    def __init__(self, poster: User, file_path: str):
        super().__init__(poster, file_path)
        print(self)

    def display(self) -> None:
        """Attempts to display the image within the post"""
        try:
            # lines of codes to show image using matplotlib
            plt.imshow(img.imread(self._content))
            plt.axis("off")
            plt.tight_layout()
            plt.show(block=False)
        except FileNotFoundError:  # if we failed, that's fine
            pass
        print("Shows picture")

    def __str__(self) -> str:
        return f"{self._poster.get_name()} posted a picture\n"


class SalePost(Post):
    """A concrete class for a sale post"""
    # in the assignment output, the price changes type when a discount is applied
    __price: Union[int, float]  # the price of the sale
    __location: str  # location of pickup
    __already_sold: bool  # whether the item was sold

    def __init__(self, poster: User, text: str, price: int, location: str):
        super().__init__(poster, text)
        self.__price = price
        self.__location = location
        self.__already_sold = False  # initially item is not sold
        print(self)

    def discount(self, discount_percent: int, password: str) -> None:
        """Sets a discount on the sale, given the seller password"""
        self._poster.authenticate(password)  # make sure password is correct for poster
        if self.__already_sold:  # make sure item is not already sold
            raise RuntimeError("Can't discount an already sold item.")
        self.__price -= self.__price * discount_percent / 100  # discount the price
        print(f"Discount on {self._poster.get_name()} product! the new price is: {self.__price}")

    def sold(self, password: str) -> None:
        """Defines the sale as sold, given the seller password"""
        self._poster.authenticate(password)  # make sure password is correct for poster
        self.__already_sold = True  # mark post as sold
        print(f"{self._poster.get_name()}'s product is sold")

    def __str__(self) -> str:
        return (f"{self._poster.get_name()} posted a product for sale:\n"
                + ("Sold" if self.__already_sold else "For sale")  # print correct description
                + f"! {self._content}, price: {self.__price}, pickup from: {self.__location}\n")


def create_post(poster: User, post_type: str, text: str, price: int, location: str) -> Post:
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
