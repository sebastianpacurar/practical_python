from abc import ABC, abstractmethod


class GenericPlatform(ABC):
    def __init__(self):
        """
        Initialize platform instance and create sys_info empty dict.
        """
        self.sys_info: dict[str, str | dict] = {}  # TODO: this should be private by name mangling

    def add_sys_info_key(self, key: str) -> None:
        """
        Adds a new parent key to the sys_info dict (this can be considered the name of the table).
        examples of keys: Disks, Processor, Drivers

        Parameters:
        - key (str): The key to be added.
        """
        self.sys_info[key] = {}

    def set_sys_info_entry_key(self, key: str, entry_key: str, entry_value: str | dict) -> None:
        """
        Sets the entry key and value in the system information dictionary.

        Parameters:
        - key (str): The key under which the information is stored. It represents the name of the table.
        - entry_key (str): The key for the specific entry within the category. It represents a row caption.
        - entry_value (str | dict): The value or dictionary of values associated with the entry key. It represents a row value.
        """
        self.sys_info.get(key)[entry_key] = entry_value

    @abstractmethod
    async def set_platform_sys_data(self) -> None:
        """
        Populate sys_info dict asynchronously
        """
        ...

    @abstractmethod
    def display_table(self) -> None:
        """
        Displays the collected system information in a formatted table.
        """
        ...

    @abstractmethod
    def is_laptop(self) -> bool:
        """
        Returns True if the platform is a laptop, False otherwise.
        """
        ...
