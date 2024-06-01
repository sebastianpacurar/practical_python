import json
import os
import time
import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, field_serializer, Field, ConfigDict
from faker import Faker
import random

"""
    model example:
    [
        {
            "title": "Value close.",
            "subtitle": "Skin majority summer close but.",
            "author": "Stephen Hoffman",
            "publisher": "Mckee Inc",
            "isbn_10": "1-5239-4677-6",
            "isbn_13": "978-1-4700-3975-2",
            "price": 72.04
        }
    ]
"""

fake = Faker()


class Book(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    title: str = Field(alias='Title')
    subtitle: str = Field(alias='Subtitle')
    author: str = Field(alias='Author')
    publisher: str = Field(alias='Publisher')
    isbn_10: str = Field(alias='ISBN-10')
    isbn_13: str = Field(alias='ISBN-13')
    price: float = Field(alias='Price')
    id: str = Field(alias='u_id', default_factory=lambda: str(uuid.uuid4()))
    dt: datetime = Field(alias='Creation Date', default_factory=lambda: datetime.now(timezone.utc))

    @field_serializer("dt")
    def serialize_datetime_to_json(self, value):
        return value.strftime("%A, %B %d, %Y at %I:%M %p")


def gen_fake_book() -> Book:
    return Book(
        title=fake.sentence(nb_words=3),
        subtitle=fake.sentence(nb_words=6),
        author=fake.name(),
        publisher=fake.company(),
        isbn_10=fake.isbn10(),
        isbn_13=fake.isbn13(),
        price=round(random.uniform(10.0, 100.0), 2)
    )


def create_books_list(num_entries: int):
    books_list: list[Book] = []
    for _ in range(num_entries):
        books_list.append(gen_fake_book())
        time.sleep(.05)
    return books_list


if __name__ == '__main__':
    time_stamp = datetime.now().strftime('%Y%m%dT%H%M%S')
    file_name = f'books-{time_stamp}.json'
    books_dir_path = os.path.join('..', 'data_sets', 'test_data', 'books')
    file_path = os.path.join(books_dir_path, file_name)

    books = create_books_list(100)
    json_data = [book.model_dump(by_alias=True) for book in books]

    with open(file_path, "w") as f:
        f.write(json.dumps(json_data, indent=4))

    print(books)
    print(f'file ${file_name} created in {books_dir_path}')
