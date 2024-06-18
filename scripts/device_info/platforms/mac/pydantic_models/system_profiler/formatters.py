def format_one_level_depth(data):
    """
    Formats a dictionary with one level of depth into a flat dictionary,
    replacing hyphens with underscores in keys.

    Args:
    - data (dict): The input dictionary with one level of depth.

    Returns:
    - dict: A dictionary with flattened keys where dashes are replaced with underscores.
    """
    res = {}
    for outer_k, outer_v in data.items():
        for i in outer_v:
            for inner_k, inner_v in i.items():
                parsed = replace_dash_with_underscore(inner_k)
                res[parsed] = inner_v
    return res


def format_audio_data_type(data):
    """
    Formats audio data into a structured format suitable for tabulation or display.

    Args:
    - data (dict): The input dictionary containing audio data.

    Returns:
    - dict: A dictionary with 'audio_items' key containing formatted rows of audio data.
    """
    rows = []
    res = {}
    for outer_k, outer_v in data.items():
        for _items in outer_v:
            entry_name = _items['_name']
            del _items['_name']
            res[entry_name] = []
            for inner_k, inner_val in _items.items():
                for i in inner_val:
                    res_info = {}
                    for k, v in i.items():
                        parsed = replace_dash_with_underscore(k)
                        res_info[parsed] = v
                    rows.append(res_info)
    return {'audio_items': rows}


def format_hardware_data_type(data):
    """
    Formats hardware data into a structured format suitable for tabulation or display.

    Args:
    - data (dict): The input dictionary containing hardware data.

    Returns:
    - dict: A dictionary with 'hardware_items' key containing formatted rows of hardware data.
    """
    res = {}
    rows = []
    for outer_k, outer_v in data.items():
        for _items in outer_v:
            entry_name = _items['_name']
            res[entry_name] = []
            res_info = {}
            for k, v in _items.items():
                parsed = replace_dash_with_underscore(k)
                res_info[parsed] = v
            rows.append(res_info)
    return {'hardware_items': rows}


def format_storage_data_type(data):
    """
    Formats storage data into a structured format suitable for tabulation or display.

    Args:
    - data (dict): The input dictionary containing storage data.

    Returns:
    - dict: A dictionary with 'volume_items' key containing formatted rows of storage volume data.
    """
    rows = []
    for outer_k, outer_v in data.items():
        for _items in outer_v:
            res = {}
            for k, v in _items.items():
                parsed = replace_dash_with_underscore(k)
                res[parsed] = v
            rows.append(res)
    return {'volume_items': rows}


def replace_dash_with_underscore(item):
    return (item[1:] if item.startswith('_') else item).replace('-', '_')
