import json
import os
from datetime import datetime

from scripts.test_data_generators.book_generator import create_books_list, Book

books_count: int = 10
test_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data_sets', 'test_data', 'books'))


def test_create_books_list() -> None:
    books: list[Book] = create_books_list(books_count)
    assert len(books) == books_count
    for book in books:
        assert isinstance(book, Book)


def test_write_to_json() -> None:
    time_stamp: str = datetime.now().strftime('%Y%m%dT%H%M%S')
    file_name: str = f'books_test_generated_{time_stamp}.json'
    fp: str = os.path.join(test_data_path, file_name)
    books: list[Book] = create_books_list(books_count)
    json_data: list[dict] = [book.model_dump(by_alias=True) for book in books]

    with open(fp, "w") as f:
        json.dump(json_data, f, indent=4)
    assert os.path.exists(fp)

    with open(fp, "r") as f:
        loaded_data: list[dict] = json.load(f)
    assert len(loaded_data) == books_count

    [print(f'\nbook {i + 1}: \n name: {b["Title"]} \n location: {fp} \n') for i, b in enumerate(loaded_data)]
