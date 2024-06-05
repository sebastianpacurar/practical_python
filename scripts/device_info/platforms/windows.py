import subprocess
import psutil
import os
import wmi

from scripts.device_info.platforms.generic_platform import GenericPlatform


class Windows(GenericPlatform):
    def get_gpu_info(self) -> None:
        def get_gpu_temperature() -> list[int]:
            temps: list[int] = []
            try:
                res: str = subprocess.check_output(
                    ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'], text=True)
                temps = [int(t.strip()) for t in res.splitlines()]
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    if os.path.exists('ADL.exe'):
                        res = subprocess.check_output(['ADL.exe', 'temperature', 'get', '0'], text=True)
                        temps += [int(t.split('=')[1]) for t in res.splitlines()]
                    else:
                        print("ADL.exe does not exist. please install ADL to use this")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass

            return temps

        gpu_temps: list[int] = get_gpu_temperature()
        if gpu_temps:
            for i, temp in enumerate(gpu_temps, 1):
                self.set_sys_info_entry_key('GPU', f'GPU {i}', {
                    'Temperature (°C)': temp,
                })
        else:
            self.set_sys_info_entry_key('GPU', 'No GPU', {
                'Temperature (°C)': 'N/A',
            })

    def get_storage_info(self) -> None:
        try:
            c = wmi.WMI()
            for disk in c.Win32_DiskDrive():
                self.set_sys_info_entry_key('Storage', disk.DeviceID, {
                    'Model': disk.Model,
                    'Size (GB)': round(int(disk.Size) / (1024 ** 3), 2),
                    'Caption': disk.Caption,
                    'Description': disk.Description,
                    'Interface Type': disk.InterfaceType,
                    'Manufacturer': disk.Manufacturer,
                    'Media Type': disk.MediaType,
                    'Partitions': disk.Partitions,
                    'Serial Number': disk.SerialNumber,
                    'Status': disk.Status,
                    'Total Cylinders': disk.TotalCylinders,
                    'Total Heads': disk.TotalHeads,
                    'Total Sectors': disk.TotalSectors,
                    'Total Tracks': disk.TotalTracks,
                    'Tracks Per Cylinder': disk.TracksPerCylinder,
                    'Bytes Per Sector': disk.BytesPerSector,
                    'Config Manager Error Code': disk.ConfigManagerErrorCode,
                    'Config Manager User Config': disk.ConfigManagerUserConfig,
                    'Creation ClassName': disk.CreationClassName,
                    'Device ID': disk.DeviceID,
                    'Firmware Revision': disk.FirmwareRevision,
                    'Index': disk.Index,
                    'Media Loaded': disk.MediaLoaded,
                    'PNP Device ID': disk.PNPDeviceID,
                    'Sectors Per Track': disk.SectorsPerTrack,

                    # TODO: don't work on windows 11
                    # 'Availability': disk.Availability,
                    # 'Default Block Size': disk.DefaultBlockSize,
                    # 'Max Block Size': disk.MaxBlockSize,
                    # 'Max Media Size': disk.MaxMediaSize,
                    # 'Min Block Size': disk.MinBlockSize,
                    # 'Signature': disk.Signature
                })
        except Exception as e:
            print(f'error fetching storage information: {e}')

    def battery_information(self) -> None:
        try:
            battery = psutil.sensors_battery()
            if battery:
                if battery.secsleft == psutil.POWER_TIME_UNLIMITED:
                    time_left = "Unlimited"
                elif battery.secsleft == psutil.POWER_TIME_UNKNOWN:
                    time_left = "Unknown"
                else:
                    hours, remainder = divmod(battery.secsleft, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    time_left = f"{hours:02}:{minutes:02}:{seconds:02}"

                self.set_sys_info_entry_key('Battery', 'Percentage', f'{battery.percent}%')
                self.set_sys_info_entry_key('Battery', 'Plugged In', 'Yes' if battery.power_plugged else 'No')
                self.set_sys_info_entry_key('Battery', 'Time Left', time_left)
        except ImportError:
            pass

    def is_laptop(self) -> bool:
        try:
            return psutil.sensors_battery() is not None
        except AttributeError:
            return False
