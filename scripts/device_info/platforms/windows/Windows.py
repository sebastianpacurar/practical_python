import asyncio
import concurrent.futures
import psutil
from typing import Any, Coroutine
from scripts.device_info.platforms.utils import (
    prettify_wmi_class_name,
    async_wmi_iter,
    install_wmi_by_version,
    async_set_wmi_data_attribute,
    set_wmi_data_attribute,
)
from scripts.device_info.platforms.windows.enums.WmiClass import WmiClass
from scripts.device_info.platforms.GenericPlatform import GenericPlatform
from scripts.utils_global.console_table.ConsoleTable import ConsoleTable

WMI_VERSION = '1.5.1'


class Windows(GenericPlatform):
    wmi_obj: Any = None

    async def set_platform_sys_data(self) -> None:
        await self.fetch_wmi_data()

    def is_laptop(self) -> bool:
        try:
            return psutil.sensors_battery() is not None
        except AttributeError:
            return False

    def display_table(self) -> None:
        self.tabulate_content()

    async def check_and_install_wmi(self) -> None:
        """
        Steps
            1) Check for wmi if installed. If not then install it using the given version
            2) Instantiate wmi_obj to WMI()
        """
        if self.wmi_obj is None:
            try:
                import wmi
            except ModuleNotFoundError:
                print("WMI package not found. Installing through pip...")
                install_wmi_by_version(WMI_VERSION)
            finally:
                print('Gathering Data...')
                self.wmi_obj = wmi.WMI()

    async def fetch_wmi_data(self) -> None:
        tasks: list[Coroutine[Any, None, None]] = [self.get_wmi_class_data(wmi_class) for wmi_class in WmiClass]
        await asyncio.gather(*tasks)

    async def get_wmi_class_data(self, wmi_class: WmiClass) -> None:
        await self.check_and_install_wmi()
        class_name: str
        target_enum: Any
        row_name: str
        class_name, target_enum, row_name = wmi_class.value

        header: str = prettify_wmi_class_name(class_name)
        self.add_sys_info_key(header)
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                wmi_class_instance = set_wmi_data_attribute(self.wmi_obj, class_name)
                async for item in async_wmi_iter(wmi_class_instance(), executor):
                    info: dict[str, dict] = {}
                    row_value: str = getattr(item, row_name, '---')
                    info_tasks: list[Coroutine[Any, None, None]] = [async_set_wmi_data_attribute(item, i.name) for i in target_enum]
                    info_results: tuple[Any] = await asyncio.gather(*info_tasks)
                    for enum_prop, result in zip(target_enum, info_results):
                        if enum_prop.value == 'Caption' and len(info_results) > 0:
                            continue
                        if type(result) is tuple:
                            result = '\n'.join(map(str, result))
                        info[enum_prop.value] = result
                    self.set_sys_info_entry_key(header, row_value, info)
        except AttributeError as ex:
            print(f"AttributeError processing WMI class {class_name}: {ex}")
        except TypeError as ex:
            print(f"TypeError processing WMI class {class_name}: {ex}")
        except ValueError as ex:
            print(f"ValueError processing WMI class {class_name}: {ex}")
        except asyncio.TimeoutError as ex:
            print(f"AsyncioError (TimeoutError) processing WMI class {class_name}: {ex}")
        except Exception as ex:
            print(f"Unexpected error processing WMI class {class_name}: {ex}")

    def tabulate_content(self) -> None:
        for k, v in self.sys_info.items():
            headers: list[str] = ['Caption']
            if len(v) == 0:
                print(f'\nNo entries found for {k}\n')
                continue
            data = []
            for name, description in v.items():
                headers += list(description.keys())
                data_row: list[str] = list(description.values())
                data.append([name] + data_row)
            ConsoleTable(data, title=f'{k} Info:', headers=headers, clear_empty_cols=True).display()
