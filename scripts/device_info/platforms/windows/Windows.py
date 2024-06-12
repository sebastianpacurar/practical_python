import asyncio

import psutil

from scripts.device_info.platforms.utils import set_wmi_data_attribute, prettify_wmi_class_name
from scripts.device_info.platforms.windows.enums.WmiClass import WmiClass
from scripts.device_info.platforms.GenericPlatform import GenericPlatform
from scripts.utils_global.console_table.ConsoleTable import ConsoleTable


class Windows(GenericPlatform):
    wmi_obj = None

    async def set_platform_sys_data(self):
        self.check_and_install_wmi()
        await self.fetch_wmi_data()

    def check_and_install_wmi(self):
        if self.wmi_obj is None:
            try:
                import wmi
            except ModuleNotFoundError:
                print("WMI package not found. Installing through pip...")
                try:
                    import pip
                    pip.main(['install', 'WMI'])
                    import wmi
                except Exception as e:
                    print(f"Failed to install WMI package: {e}")
                    return
            print('Gathering Data...')
            self.wmi_obj = wmi.WMI()

    async def fetch_wmi_data(self):
        tasks = [self.get_wmi_class_data(wmi_class) for wmi_class in WmiClass]
        await asyncio.gather(*tasks)

    async def get_wmi_class_data(self, wmi_class):
        class_name, target_enum, row_name = wmi_class.value
        header = prettify_wmi_class_name(class_name)
        self.add_sys_info_key(header)
        wmi_c = getattr(self.wmi_obj, class_name)()

        # Ensure wmi_c is an asynchronous iterable
        if isinstance(wmi_c, list):
            wmi_c = iter(wmi_c)

        # TODO: this should be async over an aiter()
        for item in wmi_c:
            info = {}
            row_value = getattr(item, row_name, '---')

            # Collect info asynchronously
            info_tasks = [async_set_wmi_data_attribute(item, i.name) for i in target_enum]
            info_results = await asyncio.gather(*info_tasks)

            for i, value in zip(target_enum, info_results):
                if i.value == 'Caption' and len(info) > 0:
                    continue
                info[i.value] = value

            self.set_sys_info_entry_key(header, row_value, info)

    def display_table(self):
        self.tabulate_content()

    def tabulate_content(self):
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

    def is_laptop(self) -> bool:
        try:
            return psutil.sensors_battery() is not None
        except AttributeError:
            return False


async def async_set_wmi_data_attribute(item, attribute_name):
    return await asyncio.to_thread(set_wmi_data_attribute, item, attribute_name)
