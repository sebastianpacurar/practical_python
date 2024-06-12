import asyncio
import json
import subprocess

from scripts.device_info.platforms.GenericPlatform import GenericPlatform
from scripts.device_info.platforms.mac.debugging import not_nested
from scripts.device_info.platforms.mac.enum.system_profiler.SystemProfiler import SystemProfiler
from scripts.utils_global.console_table.ConsoleTable import ConsoleTable


class Darwin(GenericPlatform):
    async def set_platform_sys_data(self):
        await self.get_all_sys_profiler()
        self.sys_info = self.update_key_naming()

    def display_table(self):
        self.tabulate_one_leve_sp()

    async def get_all_sys_profiler(self):
        tasks = [get_target_system_profiler_data(data_type) for data_type in not_nested]
        results = await asyncio.gather(*tasks)

        for result in results:
            self.process_data(result)

    def update_key_naming(self):
        res_info = {}
        try:
            for k, v in self.sys_info.items():
                model_class = getattr(SystemProfiler, k)
                model = model_class.value(**v)
                res_info[k] = model.model_dump(by_alias=True)
            return res_info
        except Exception as ex:
            print(ex)

    def tabulate_one_leve_sp(self):
        for k, v in self.sys_info.items():
            if len(v) == 0:
                print(f'\nNo entries found for {k}\n')
                continue
            data = []
            keys, vals = list(v.keys()), list(v.values())
            headers = ['Name'] if 'Name' in v.keys() else ['Caption']
            try:
                headers += keys
                data.append([k] + vals)
            except Exception as ex:
                print(ex)
            ConsoleTable(data, title=f'{k} Info:', headers=headers, clear_empty_cols=True).display()

    def process_data(self, data_item):
        for data_type_k, data_type_v in data_item.items():
            self.add_sys_info_key(data_type_k)
            for i in data_type_v:
                for k, v in i.items():
                    key = k[1:] if k.startswith('_') else k
                    key = key.replace('-', '_')
                    self.set_sys_info_entry_key(data_type_k, key, v)

    def is_laptop(self) -> bool:
        try:
            pmset: str = subprocess.check_output(['pmset', '-g', 'batt'], text=True)
            return 'Battery' in pmset
        except subprocess.CalledProcessError:
            return False


async def get_target_system_profiler_data(data_type):
    res = await asyncio.create_subprocess_exec('system_profiler', data_type, '-json', stdout=asyncio.subprocess.PIPE)
    stdout, _ = await res.communicate()
    if res.returncode != 0:
        raise RuntimeError(f"system_profiler failed with return code: {res.returncode}")
    return json.loads(stdout)
