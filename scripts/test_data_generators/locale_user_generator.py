import json
import os
import time
from datetime import datetime
import random
from faker import Faker

from pydantic import BaseModel, Field, ConfigDict, model_validator

from utils_global.faker_locales import latin_alphabet_locales, one_per_each
from utils_global.console_table.ConsoleTable import ConsoleTable
from utils_global.console_table.Layout import Layout

"""
    model example:
    [
        {
            "First Name": "Teresa",
            "Last Name": "Alvarado",
            "City": "Mirandaburgh",
            "Building Number": "71331",
            "Country": "Colombia",
            "Address": "654 Yang Harbor Jenniferville, GA 08622"
        }
    }
"""

locale_users_dir_path: str = os.path.join('..', '..', 'data_sets', 'test_data', 'locale_users')


class LocaleUser(BaseModel):
    model_config: ConfigDict = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    locale: str = Field(exclude=True)
    faker: Faker = Field(exclude=True, default_factory=Faker)

    first_name: str = Field(alias='First Name')
    last_name: str = Field(alias='Last Name')
    city: str = Field(alias='City')
    building_number: str = Field(alias='Building Number')
    country: str = Field(alias='Country')
    address: str = Field(alias='Address')

    @model_validator(mode='before')
    @classmethod
    def populate_fields_based_on_locale(cls, values: dict) -> dict:
        locale: str = values.get('locale', 'en_US')
        faker: Faker = Faker(locale)
        address: str = faker.address().replace('\n', ' ')

        values.update({
            'faker': faker,
            'first_name': faker.first_name(),
            'last_name': faker.last_name(),
            'city': faker.city(),
            'building_number': faker.building_number(),
            'country': faker.country(),
            'address': address
        })
        return values


def create_locale_users_list(locales_list: list[str], count: int) -> list[LocaleUser]:
    users_list: list[LocaleUser] = []
    for _ in range(count):
        locale: str = random.choice(locales_list)
        user: LocaleUser = LocaleUser(locale=locale)
        users_list.append(user)
        time.sleep(.01)
    return users_list


def build_console_table() -> None:
    users: list[LocaleUser] = create_locale_users_list(one_per_each, 100)
    headers: list[str] = ['First Name', 'Last Name', 'City', 'Building Number', 'Country']
    user_formatted_rows: list[list[str]] = []
    for entry in users:
        user_values = [getattr(entry, header.lower().replace(' ', '_')) for header in headers]
        user_formatted_rows.append(user_values)

    ConsoleTable(user_formatted_rows, headers=headers, layout=Layout.FANCY_OUTLINE).display()


def write_to_json() -> None:
    time_stamp: str = datetime.now().strftime('%Y%m%dT%H%M%S')
    file_name: str = f'locale_user_{time_stamp}.json'
    file_path: str = os.path.join(locale_users_dir_path, file_name)

    users: list[LocaleUser] = create_locale_users_list(latin_alphabet_locales, 100)
    json_data: list[dict] = [user.model_dump(by_alias=True) for user in users]

    with open(file_path, "w") as f:
        f.write(json.dumps(json_data, indent=4))

    print(f'file {file_name} created in {locale_users_dir_path}')


if __name__ == '__main__':
    build_console_table()
    write_to_json()
