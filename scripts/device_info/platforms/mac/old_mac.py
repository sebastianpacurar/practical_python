# def set_gpu_info(self) -> None:
#     self.add_sys_info_key('GPU')
#
#     def set_gpu_temperature() -> list[int]:
#         temps: list[int] = []
#         try:
#             # attempt to get GPU temperature using iStats (macOS)
#             result: str = subprocess.check_output(['istats', 'extra'], text=True)
#             temps = [int(t.split(':')[1].strip()) for t in result.splitlines() if 'GPU' in t]
#         except (subprocess.CalledProcessError, FileNotFoundError):
#             # if iStats didn't work, try using smcFanControl (macOS)
#             try:
#                 result = subprocess.check_output(['smcFanControl', '-g', 'tsdi'], text=True)
#                 temps = [int(t.split(':')[1].strip()) for t in result.splitlines() if 'GPU' in t]
#             except (subprocess.CalledProcessError, FileNotFoundError):
#                 pass
#
#         return temps
#
#     gpu_temps: list[int] = set_gpu_temperature()
#     if gpu_temps:
#         for i, temp in enumerate(gpu_temps, 1):
#             self.set_sys_info_entry_key('GPU', f'GPU {i}', {
#                 'Temperature (°C)': temp,
#             })
#     else:
#         self.set_sys_info_entry_key('GPU', 'No GPU', {
#             'Temperature (°C)': 'N/A',
#         })
#
#
# def set_disk_partition_size(self):
#     partitions = psutil.disk_partitions(all=True)
#     self.add_sys_info_key('Disks')
#     for partition in partitions:
#         usage = psutil.disk_usage(partition.mountpoint)
#         info = {
#             'Mount Point': partition.mountpoint,
#             'Total (GB)': round(usage.total / (1024 ** 3), 2),
#             'Used (GB)': round(usage.used / (1024 ** 3), 2),
#             'Free (GB)': round(usage.free / (1024 ** 3), 2),
#             'File System': partition.fstype,
#         }
#         try:
#             self.set_sys_info_entry_key('Disks', partition.device, info)
#         except Exception as ex:
#             print('here')
#
#
#     def set_network_info(self):
#         net_info = psutil.net_if_addrs()
#         network_interfaces = psutil.net_io_counters(pernic=True)
#         self.add_sys_info_key('Network')
#         for interf, addresses in net_info.items():
#             mac_addresses = [addr.address for addr in addresses if addr.family.name == AddressFamily.AF_LINK.name]
#             ipv4_addresses = [addr.address for addr in addresses if addr.family.name == AddressFamily.AF_INET.name]
#             ipv6_addresses = [addr.address for addr in addresses if addr.family.name == AddressFamily.AF_INET6.name]
#
#             ips_info = {
#                 'MAC': '\n'.join(mac_addresses) if mac_addresses else '-',
#                 'IPv4': '\n'.join(ipv4_addresses) if ipv4_addresses else '-',
#                 'IPv6': '\n'.join(ipv6_addresses) if ipv6_addresses else '-'
#             }
#
#             if interf in network_interfaces:
#                 stats = network_interfaces[interf]
#                 bandwidth_info = {
#                     'Bytes Sent': stats.bytes_sent,
#                     'Bytes Received': stats.bytes_recv,
#                     'Packets Sent': stats.packets_sent,
#                     'Packets Received': stats.packets_recv,
#                 }
#                 ips_info.update(bandwidth_info)
#
#             self.set_sys_info_entry_key('Network', interf, ips_info)
#
#     def set_storage_info(self) -> None:
#         try:
#             self.add_sys_info_key('Storage')
#             info = subprocess.check_output(['diskutil', 'list'], text=True)
#             disks = info.strip().split('\n\n')
#             for disk in disks:
#                 lines = disk.strip().split(' ')
#                 disk_name = lines[0]
#                 detail_info = subprocess.check_output(['diskutil', 'info', disk_name], text=True)
#                 details = detail_info.strip().split('\n')
#                 disk_data = {}
#                 for detail in details:
#                     key_value = detail.split(':')
#                     if len(key_value) == 2:
#                         key, value = key_value
#                         disk_data[key.strip()] = value.strip()
#
#                 self.set_sys_info_entry_key('Storage', disk_name, disk_data)
#
#         except Exception as e:
#             print(f'Error fetching storage information: {e}')
#
#     def battery_information(self) -> None:
#         try:
#             self.add_sys_info_key('Battery')
#             # basic info
#             battery_info = subprocess.check_output(['pmset', '-g', 'batt'], text=True).strip().split('\n')
#             if len(battery_info) >= 2:
#                 power_source = battery_info[0].strip()
#                 self.set_sys_info_entry_key('Battery', 'Current Status', power_source)
#
#                 battery_status = [status.strip() for status in battery_info[1].strip().split(';')]
#                 charging_status = battery_status[1]
#                 time_left = ' '.join(battery_status[2].split(' ')[:1])
#
#                 try:
#                     int(time_left[0])
#                 except ValueError:
#                     time_left = 'No Estimate'
#
#                 self.set_sys_info_entry_key('Battery', 'Charging Status', charging_status)
#                 self.set_sys_info_entry_key('Battery', 'Time Left', time_left)
#
#             # detailed info
#             ioreg_output = subprocess.check_output(["ioreg", "-r", "-c", "AppleSmartBattery"], text=True)
#             battery_data = {}
#             for line in ioreg_output.split("\n"):
#                 parts = [part.strip() for part in line.split('=')]
#                 if len(parts) == 2:
#                     key, value = parts
#                     battery_data[key.strip('"')] = value.strip()
#
#             if battery_data:
#                 for i in BatteryInfo:
#                     self.set_sys_info_entry_key('Battery', i.name, battery_data.get(i.value, 'Unknown'))
#         except subprocess.CalledProcessError as e:
#             print(f"An error occurred: {e}")


# TODO: in progress
# def get_io_kit_data(self, data_type):
#     try:
#         ioreg_output = subprocess.check_output(["ioreg", "-r", "-c", data_type], text=True)
#         io_kit_data = {}
#
#         a = self.extract_content(ioreg_output)
#
#         for line in ioreg_output.split("\n"):
#             parts = [part.strip() for part in line.split('=')]
#             if len(parts) == 2:
#                 key, value = parts
#                 io_kit_data[key.strip('"')] = value.strip()
#
#         if len(io_kit_data) > 0:
#             pass
#             for i in io_kit_objects:
#                 self.set_sys_info_entry_key('Battery', i.name, io_kit_data.get(i.value, 'Unknown'))
#
#     except subprocess.CalledProcessError as e:
#         raise RuntimeError(f"Command failed with return code {e.returncode}: {e.stderr}")
#
#
# TODO in progress
# def extract_content(self, input_string):
#     content = ""
#     inside_curly_brackets = False
#     curly_bracket_count = 0
#
#     for char in input_string:
#         if char == '{':
#             curly_bracket_count += 1
#             if curly_bracket_count == 1:
#                 inside_curly_brackets = True
#         elif char == '}':
#             curly_bracket_count -= 1
#             if curly_bracket_count == 0:
#                 inside_curly_brackets = False
#         elif inside_curly_brackets:
#             if char == '|':
#                 continue
#             content += char
#
#     return content.strip()
