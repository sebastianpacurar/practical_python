import pytest
import json
import os
from faker import Faker
from datetime import datetime

from tabulate import tabulate

from utils_global.faker_locales import one_per_each
from test_data_generators.locale_user_generator import create_locale_users_list, LocaleUser
from utils_global.console_table.ConsoleTable import ConsoleTable
from utils_global.console_table.Layout import Layout

locales_list: list[str] = ['en_US', 'fr_FR', 'es_ES']
users_count: int = 10


@pytest.mark.parametrize('locale', one_per_each)
def test_table_locales(locale: str) -> None:
    headers: list[str] = ['First Name', 'Last Name', 'City', 'Building Number', 'Country']
    user_data: list[LocaleUser] = create_locale_users_list([locale], 1)
    user_formatted_rows: list[list[str]] = []
    for entry in user_data:
        user_values = [getattr(entry, header.lower().replace(' ', '_')) for header in headers]
        user_formatted_rows.append(user_values)

    expected_table: list[str] = tabulate(
        user_formatted_rows,
        headers=headers,
        showindex='never',
        stralign='center',
        tablefmt=Layout.FANCY_OUTLINE.value
    ).split('\n')

    table: ConsoleTable = ConsoleTable(user_data, headers=headers, layout=Layout.FANCY_OUTLINE)

    print('\n')
    table.display()
    print('\n')
    assert table.build_tabulate() == expected_table, 'built table does not match expected table'


def test_create_locale_users_list() -> None:
    users: list = create_locale_users_list(locales_list, users_count)
    assert len(users) == users_count
    for user in users:
        assert user.locale in locales_list
        assert isinstance(user.faker, Faker)
        assert hasattr(user, 'first_name')
        assert hasattr(user, 'last_name')
        assert hasattr(user, 'city')
        assert hasattr(user, 'building_number')
        assert hasattr(user, 'country')
        assert hasattr(user, 'address')


def test_writing_json_file(tmpdir) -> None:
    time_stamp: str = datetime.now().strftime('%Y%m%dT%H%M%S')
    file_name: str = f'locale_user_test_generated_{time_stamp}.json'
    file_path: str = os.path.join(tmpdir, file_name)

    users: list = create_locale_users_list(locales_list, users_count)
    json_data: list = [user.model_dump(by_alias=True) for user in users]

    with open(file_path, "w") as f:
        f.write(json.dumps(json_data, indent=4))

    assert os.path.exists(file_path)
