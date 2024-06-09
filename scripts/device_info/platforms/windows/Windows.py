import psutil
import re

from scripts.device_info.platforms.windows.enums.WmiClass import WmiClass
from scripts.device_info.platforms.GenericPlatform import GenericPlatform


class Windows(GenericPlatform):
    _wmi = None

    def set_platform_sys_data(self):
        if self._wmi is None:
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
            self._wmi = wmi.WMI()
            # self.fetch_wmi_data(WmiClass.MEMORY_DEVICE)
            for c in WmiClass:
                self.fetch_wmi_data(c)

    def fetch_wmi_data(self, wmi_class: WmiClass):
        """entry example:
            enum = (class_name, target_enum, row_name)
            COMPUTER_SYSTEM = ('Win32_ComputerSystem', Win32ComputerSystem, Win32ComputerSystem.Caption.name)
        """
        class_name, target_enum, row_name = wmi_class.value
        header = prettify_class_name(class_name)
        try:
            self.add_sys_info_key(header)
            wmi_c = getattr(self._wmi, class_name)
            for item in wmi_c():
                info = {}
                row_value = getattr(item, row_name, '---')
                for i in target_enum:
                    if i.value == 'Caption' and len(info) > 0:
                        continue
                    info[i.value] = set_data_attribute(item, i)

                self.set_sys_info_entry_key(header, row_value, info)
        except Exception as ex:
            print(f'issues at the last key of the {self.sys_info}. exception: {ex}')
            pass

    def is_laptop(self) -> bool:
        try:
            return psutil.sensors_battery() is not None
        except AttributeError:
            return False


def prettify_class_name(name):
    """ examples:
        'Win32_OperatingSystem' becomes 'Operating System'
        'Win32_NetworkAdapterConfiguration' becomes 'Network Adapter Configuration'
    """
    base = name[6:]
    if base.startswith('USB'):
        base = base.replace('USB', 'Usb')
    spaced = re.sub(r'(?<!^)(?=[A-Z])', ' ', base)
    prettified = spaced.title()
    return prettified


# TODO: change this one to handle Win32_USBControllerDevice
def set_data_attribute(wmi_entity, attribute):
    """ set attribute if there is one, else add horizontal dash """
    attr_val = getattr(wmi_entity, attribute.name, '-')
    if attr_val is None or attr_val == '':
        res = '-'
    else:
        res = attr_val
    return res
