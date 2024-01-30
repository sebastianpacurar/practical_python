import platform
import subprocess
import json

# platform basic onfo
system_info = {
    'System': platform.system(),
    'Node Name': platform.node(),
    'Release': platform.release(),
    'Version': platform.version(),
    'Machine': platform.machine(),
    'Processor': platform.processor(),
}

# hardware info
if platform.system() == 'Windows':
    import wmi

    c = wmi.WMI()
    for item in c.Win32_ComputerSystem():
        system_info['Manufacturer'] = item.Manufacturer
        system_info['Model'] = item.Model
        system_info['Total Physical Memory (GB)'] = round(int(item.TotalPhysicalMemory) / (1024 ** 3), 2)

elif platform.system() == 'Linux':
    with open('/proc/cpuinfo') as f:
        cpu_info = f.read()
        system_info['CPU Info'] = cpu_info
    with open('/proc/meminfo') as f:
        mem_info = f.read()
        system_info['Memory Info'] = mem_info

elif platform.system() == 'Darwin':  # macOS
    try:
        # system profiler
        system_profiler_output = subprocess.check_output(['system_profiler', '-detailLevel', 'full', '-json'])
        system_profiler_data = json.loads(system_profiler_output)

        # hardware info
        hardware_info = system_profiler_data.get('SPHardwareDataType', [])[0]
        system_info['Model Identifier'] = hardware_info.get('machine_model', '')
        system_info['CPU Type'] = hardware_info.get('cpu_type', '')
        system_info['CPU Speed'] = hardware_info.get('current_processor_speed', '')
        system_info['Number of CPUs'] = hardware_info.get('number_processors', '')
        system_info['Total RAM (GB)'] = round(hardware_info.get('physical_memory', 0) / (1024 ** 3), 2)
    except Exception as e:
        print(f'Error: {e}')

# Print system information
for k, v in system_info.items():
    print(f'{k}: {v}')
