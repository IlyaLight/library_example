import servise
from models import Book


def add_book(description_id: int = None, name: str = None, autors: str = None, annotatio: str = None) -> Book:
    if description_id:
        servise.create_book(description_id)
    elif name:
        servise.create_book(servise.create_book_description(name, autors, annotatio).id)
    else:
        raise TimeoutError("wrong args")
