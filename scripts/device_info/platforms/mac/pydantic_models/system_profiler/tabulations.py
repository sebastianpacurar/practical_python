from scripts.utils_global.console_table.ConsoleTable import ConsoleTable


def tabulate_one_level_depth(json_data):
    for k, v in json_data.items():
        if len(v) == 0:
            print(f'\nNo entries found for {k}\n')
            continue
        headers = list(v.keys())
        data = []
        if 'Name' in headers:
            headers.remove('Name')
            headers.insert(0, 'Name')

        max_length = max(len(values) if isinstance(values, list) else 1 for values in v.values())
        for i in range(max_length):
            row = []
            for header in headers:
                row.append(v[header] if i == 0 else '-')
            data.append(row)
        ConsoleTable(data, title=f'{k} Info:', headers=headers).display()


def tabulate_audio_hardware_profiler(json_data):
    for key, val in json_data.items():
        headers, data = get_headers_and_data(val)
        if 'Name' in headers:
            headers.remove('Name')
            headers.insert(0, 'Name')
        ConsoleTable(data, title=f'{key} Info:', headers=headers).display()


def tabulate_storage_data_type(json_data):
    for key, val in json_data.items():
        # display the volumes info
        volume_headers, volume_data = get_headers_and_data(val, exclude_keys=['Physical Drive'])
        if 'Name' in volume_headers:
            volume_headers.remove('Name')
            volume_headers.insert(0, 'Name')
        ConsoleTable(volume_data, title=f'{key} - Volumes Info', headers=volume_headers).display()

        # display the physical drives info attached to the above volumes
        physical_headers = ["Volume Name"]
        physical_data = []
        for name in val:
            for entry in val[name]:
                if 'Physical Drive' in entry:
                    volume_name = entry.get('Name', '-')
                    physical_entry = entry['Physical Drive']
                    if len(physical_headers) == 1:
                        physical_headers += list(physical_entry.keys())
                    physical_row = [volume_name] + [physical_entry.get(h, '-') for h in physical_headers[1:]]
                    physical_data.append(physical_row)
        ConsoleTable(physical_data, title=f'{key} - Physical Drives Info', headers=physical_headers).display()


def get_headers_and_data(val, exclude_keys=None):
    headers = []
    data = []
    exclude_keys = exclude_keys or []
    for name in val:
        for entry in val[name]:
            for header in entry.keys():
                if header not in exclude_keys and header not in headers:
                    headers.append(header)
            row = [entry.get(header, '-') for header in headers]
            data.append(row)
    return headers, data
