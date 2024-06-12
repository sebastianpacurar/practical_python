import re


def set_wmi_data_attribute(entity, attr):
    """ set attribute if there is one, else add horizontal dash """
    attr_val = getattr(entity, attr, '-')
    if attr_val is None or attr_val == '':
        res = '-'
    else:
        res = attr_val
    return res


def prettify_wmi_class_name(name):
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
