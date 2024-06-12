import asyncio
from abc import ABC, abstractmethod


class GenericPlatform(ABC):
    def __init__(self):
        self.sys_info: dict[str, str | dict] = {}  # TODO: this should be private by name mangling
        asyncio.run(self.set_platform_sys_data())
        self.display_table()

    def set_sys_info_entry_key(self, key: str, entry_key: str, entry_value: str | dict) -> None:
        self.sys_info.get(key)[entry_key] = entry_value

    def add_sys_info_key(self, key: str) -> None:
        self.sys_info[key] = {}

    @abstractmethod
    async def set_platform_sys_data(self):
        ...

    @abstractmethod
    def display_table(self):
        ...

    @abstractmethod
    def is_laptop(self) -> bool:
        ...
