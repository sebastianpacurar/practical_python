import asyncio
import json
import subprocess

from scripts.device_info.platforms.GenericPlatform import GenericPlatform
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.SystemProfiler import simple, nested_active
from scripts.device_info.platforms.mac.pydantic_models.system_profiler import SystemProfiler, formatters, tabulations


class Darwin(GenericPlatform):
    async def set_platform_sys_data(self):
        print('Gathering Data...')
        await self.get_all_sys_profiler()
        self.model_system_profiler()

    def display_table(self) -> None:
        for k in self.sys_info.keys():
            target_group = {k: self.sys_info[k]}
            if k in simple:
                tabulations.tabulate_one_level_depth(target_group)
            elif k in ['SPAudioDataType', 'SPHardwareDataType']:
                tabulations.tabulate_audio_hardware_profiler(target_group)
            elif k == 'SPStorageDataType':
                tabulations.tabulate_storage_data_type(target_group)

    async def get_all_sys_profiler(self):
        """
        Asynchronously retrieves system profiler data for each data type in `simple` and `nested_active` lists.
        Updates `sys_info` with the formatted data based on the data type.
        """
        tasks = [get_target_system_profiler_data(data_type) for data_type in simple + nested_active]
        results = await asyncio.gather(*tasks)
        for result in results:
            target = [k for k in result.keys()][0]
            self.add_sys_info_key(target)
            if target in simple:
                self.sys_info.get(target).update(formatters.format_one_level_depth(result))
            elif target == 'SPAudioDataType':
                self.sys_info.get(target).update(formatters.format_audio_data_type(result))
            elif target == 'SPHardwareDataType':
                self.sys_info.get(target).update(formatters.format_hardware_data_type(result))
            elif target == 'SPStorageDataType':
                self.sys_info.get(target).update(formatters.format_storage_data_type(result))

    def model_system_profiler(self):
        """
        Models the system profiler data stored in `sys_info` into Pydantic models updating `sys_info` with the modeled data.
        """
        for k, v in self.sys_info.items():
            model_class = getattr(SystemProfiler, k)
            model = model_class(**v)
            self.sys_info[k] = model.model_dump(by_alias=True)

    def is_laptop(self) -> bool:
        try:
            pmset: str = subprocess.check_output(['pmset', '-g', 'batt'], text=True)
            return 'Battery' in pmset
        except subprocess.CalledProcessError:
            return False


async def get_target_system_profiler_data(data_type):
    """
    Asynchronously runs `system_profiler` with the specified data type, retrieves the JSON output, and parses it into a Python dictionary.
    """
    res = await asyncio.create_subprocess_exec('system_profiler', data_type, '-json', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, _ = await res.communicate()
    if res.returncode != 0:
        raise RuntimeError(f"system_profiler failed with return code: {res.returncode}")
    return json.loads(stdout)
