from typing import List

from models import Book, BookDescription
import uuid


def create_book(description_id: int) -> Book:
    book = Book(description_id, uuid.uuid1().int)
    return book


def create_book_description(name: str, autors: List[str], annotatio: str) -> BookDescription:
    return BookDescription(name, autors, annotatio)