import asyncio
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Generator


def set_wmi_data_attribute(entity: Any, attr: str) -> str:
    """
     Retrieve and set a WMI data attribute for a given entity.

     This function attempts to get the value of a specified attribute from a WMI entity.
     If the attribute does not exist, is None, or is an empty string, it returns a placeholder '-'.

     Args:
         entity (Any): The WMI entity from which to retrieve the attribute.
         attr (str): The name of the attribute to retrieve.

     Returns:
         str: The value of the specified attribute, or '-' if the attribute does not exist or is empty.
     """
    attr_val = getattr(entity, attr, '-')
    if attr_val is None or attr_val == '':
        res = '-'
    else:
        res = attr_val
        if attr == 'Size' or attr == 'Capacity' or attr == 'FreeSpace':
            res = f'{round(int(attr_val) / (1024 ** 3), 2)} GB'
    return res


async def async_set_wmi_data_attribute(item: Any, attribute_name: str) -> Any:
    """
    Asynchronously set a WMI data attribute for a given item.

    Args:
        item (Any): The WMI item from which to get the attribute.
        attribute_name (str): The name of the attribute to retrieve.

    Returns:
        Any: The value of the specified attribute or a placeholder if not found.
    """
    return await asyncio.to_thread(set_wmi_data_attribute, item, attribute_name)


def prettify_wmi_class_name(name: str) -> str:
    """
    Format class name into a readable string then return it. Treat exceptions differently (USB, OS, PnP)

    Args:
        name: a string being first parameter of a WmiClass enum value. This represents the WMI() attribute

    Examples:
        'Win32_OperatingSystem' becomes 'Operating System'
        'Win32_NetworkAdapterConfiguration' becomes 'Network Adapter Configuration'
    """
    base = name[6:]
    if base.startswith('USB'):
        base = base.replace('USB', 'Usb')
    elif base.startswith('OS'):
        base = base.replace('OS', 'Os')
    elif base.startswith('PnP'):
        base = base.replace('PnP', 'Pnp')
    spaced = re.sub(r'(?<!^)(?=[A-Z])', ' ', base)
    prettified = spaced.title()
    return prettified


async def async_wmi_iter(wmi_class: Any, executor: ThreadPoolExecutor) -> Generator[Any, None, None]:
    """
    Asynchronously iterates over the WmiClass enum entries.

    Args:
        wmi_class: WmiClass enum entry.
        executor: Thread Pool Executor.

    Yields:
        item: An item from the WMI class.
    """
    loop = asyncio.get_event_loop()
    it = iter(wmi_class)
    while True:
        item = await loop.run_in_executor(executor, next, it, None)
        if item is None:
            break  # return gracefully, without causing StopIteration or StopAsyncIteration errors
        yield item
