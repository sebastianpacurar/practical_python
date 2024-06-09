from abc import ABC, abstractmethod

from scripts.utils_global.console_table.ConsoleTable import ConsoleTable


class GenericPlatform(ABC):
    def __init__(self):
        self.sys_info: dict[str, str | dict] = {}  # TODO: this should be private by name mangling
        self.set_platform_sys_data()

    def set_sys_info_entry_key(self, key: str, entry_key: str, entry_value: str | dict) -> None:
        self.sys_info.get(key)[entry_key] = entry_value

    def add_sys_info_key(self, key: str) -> None:
        self.sys_info[key] = {}

    def print_basic_format(self):
        for k, v in self.sys_info.items():
            if isinstance(v, dict):
                print(f'\n{k}')
                for key, val in v.items():
                    print(f'{key}: {val}')
            else:
                print(f'{k}: {v}')

    def print_detailed_format(self) -> None:
        for k, v in self.sys_info.items():
            headers = ['Caption']
            if len(v) == 0:
                print(f'\nNo entries found for {k}\n')
                continue
            data = []
            for name, description in v.items():
                headers += list(description.keys())
                data_row = list(description.values())
                data.append([name] + data_row)
            ConsoleTable(data, title=f'{k} Info:', headers=headers, clear_empty_cols=True).display()

    @abstractmethod
    def set_platform_sys_data(self):
        ...

    @abstractmethod
    def is_laptop(self) -> bool:
        ...
