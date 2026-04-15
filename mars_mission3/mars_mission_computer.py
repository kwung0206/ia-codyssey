import os
import time


class SystemInfo:
    @staticmethod
    def _read_first_line(path):
        try:
            file = open(path, 'r', encoding='utf-8')
            line = file.readline()
            file.close()
            return line.strip()
        except Exception:
            return ''

    @staticmethod
    def _read_all_lines(path):
        try:
            file = open(path, 'r', encoding='utf-8')
            lines = file.readlines()
            file.close()
            return lines
        except Exception:
            return []

    @staticmethod
    def _get_uname():
        try:
            return os.uname()
        except Exception:
            return None

    @classmethod
    def get_operating_system(cls):
        try:
            uname_info = cls._get_uname()

            if uname_info is not None:
                return uname_info.sysname

            return os.name
        except Exception:
            return '확인 불가'

    @classmethod
    def get_operating_system_version(cls):
        try:
            uname_info = cls._get_uname()

            if uname_info is not None:
                return uname_info.release

            return '확인 불가'
        except Exception:
            return '확인 불가'

    @classmethod
    def get_cpu_type(cls):
        try:
            lines = cls._read_all_lines('/proc/cpuinfo')

            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)

                    if key.strip().lower() == 'model name':
                        return value.strip()

            uname_info = cls._get_uname()

            if uname_info is not None:
                return uname_info.machine

            return '확인 불가'
        except Exception:
            return '확인 불가'

    @staticmethod
    def get_cpu_core_count():
        try:
            core_count = os.cpu_count()

            if core_count is None:
                return '확인 불가'

            return core_count
        except Exception:
            return '확인 불가'

    @staticmethod
    def _read_meminfo():
        meminfo = {}

        try:
            lines = SystemInfo._read_all_lines('/proc/meminfo')

            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    parts = value.strip().split()

                    if len(parts) > 0 and parts[0].isdigit():
                        meminfo[key.strip()] = int(parts[0])

            return meminfo
        except Exception:
            return {}

    @classmethod
    def get_memory_size(cls):
        try:
            meminfo = cls._read_meminfo()
            total_kb = meminfo.get('MemTotal', 0)

            if total_kb == 0:
                return '확인 불가'

            total_gb = total_kb / 1024 / 1024
            return round(total_gb, 2)
        except Exception:
            return '확인 불가'

    @staticmethod
    def _read_cpu_times():
        try:
            first_line = SystemInfo._read_first_line('/proc/stat')

            if not first_line:
                return None, None

            parts = first_line.split()

            if len(parts) < 5:
                return None, None

            values = []
            index = 1

            while index < len(parts):
                values.append(int(parts[index]))
                index += 1

            idle = values[3]

            if len(values) > 4:
                idle += values[4]

            total = 0

            for value in values:
                total += value

            return total, idle
        except Exception:
            return None, None

    @classmethod
    def get_cpu_usage_percent(cls):
        try:
            total_1, idle_1 = cls._read_cpu_times()

            if total_1 is None or idle_1 is None:
                return '확인 불가'

            time.sleep(1)

            total_2, idle_2 = cls._read_cpu_times()

            if total_2 is None or idle_2 is None:
                return '확인 불가'

            total_diff = total_2 - total_1
            idle_diff = idle_2 - idle_1

            if total_diff <= 0:
                return 0.0

            cpu_usage = (total_diff - idle_diff) / total_diff * 100
            return round(cpu_usage, 2)
        except Exception:
            return '확인 불가'

    @classmethod
    def get_memory_usage_percent(cls):
        try:
            meminfo = cls._read_meminfo()

            total_kb = meminfo.get('MemTotal', 0)
            available_kb = meminfo.get('MemAvailable', 0)

            if total_kb == 0:
                return '확인 불가'

            if available_kb == 0:
                free_kb = meminfo.get('MemFree', 0)
                buffers_kb = meminfo.get('Buffers', 0)
                cached_kb = meminfo.get('Cached', 0)
                available_kb = free_kb + buffers_kb + cached_kb

            used_kb = total_kb - available_kb
            memory_usage = used_kb / total_kb * 100

            return round(memory_usage, 2)
        except Exception:
            return '확인 불가'


class MissionComputer:
    def __init__(self, setting_path='setting.txt'):
        self.setting_path = setting_path
        self.default_settings = {
            'operating_system': True,
            'operating_system_version': True,
            'cpu_type': True,
            'cpu_core_count': True,
            'memory_size': True,
            'cpu_usage_percent': True,
            'memory_usage_percent': True
        }
        self.settings = self._load_settings()

    def _load_settings(self):
        settings = {}

        for key in self.default_settings:
            settings[key] = self.default_settings[key]

        try:
            if not os.path.exists(self.setting_path):
                return settings

            file = open(self.setting_path, 'r', encoding='utf-8')
            lines = file.readlines()
            file.close()

            for line in lines:
                text = line.strip()

                if text == '':
                    continue

                if text.startswith('#'):
                    continue

                if '=' not in text:
                    continue

                key, value = text.split('=', 1)
                key = key.strip()
                value = value.strip().lower()

                if key in settings:
                    if value in ('true', '1', 'yes', 'y'):
                        settings[key] = True
                    elif value in ('false', '0', 'no', 'n'):
                        settings[key] = False

            return settings
        except Exception:
            return settings

    @staticmethod
    def _escape_json_string(text):
        result = str(text)
        result = result.replace('\\', '\\\\')
        result = result.replace('"', '\\"')
        result = result.replace('\n', '\\n')
        result = result.replace('\t', '\\t')
        return result

    @classmethod
    def _value_to_json(cls, value):
        if isinstance(value, bool):
            if value:
                return 'true'
            return 'false'

        if value is None:
            return 'null'

        if isinstance(value, int):
            return str(value)

        if isinstance(value, float):
            return str(value)

        return '"' + cls._escape_json_string(value) + '"'

    @classmethod
    def _dict_to_json(cls, data):
        lines = []
        lines.append('{')

        keys = list(data.keys())
        index = 0

        while index < len(keys):
            key = keys[index]
            value = data[key]

            line = '    "' + cls._escape_json_string(key) + '": '
            line += cls._value_to_json(value)

            if index != len(keys) - 1:
                line += ','

            lines.append(line)
            index += 1

        lines.append('}')
        return '\n'.join(lines)

    def _collect_data(self, method_map):
        result = {}

        for key in method_map:
            if self.settings.get(key, True) is False:
                continue

            method_name = method_map[key]

            try:
                method = getattr(SystemInfo, method_name)
                result[key] = method()
            except Exception as error:
                result[key] = '오류 발생: ' + str(error)

        return result

    def get_mission_computer_info(self):
        info_methods = {
            'operating_system': 'get_operating_system',
            'operating_system_version': 'get_operating_system_version',
            'cpu_type': 'get_cpu_type',
            'cpu_core_count': 'get_cpu_core_count',
            'memory_size': 'get_memory_size'
        }

        info = self._collect_data(info_methods)
        json_text = self._dict_to_json(info)
        print(json_text)
        return info

    def get_mission_computer_load(self):
        load_methods = {
            'cpu_usage_percent': 'get_cpu_usage_percent',
            'memory_usage_percent': 'get_memory_usage_percent'
        }

        load = self._collect_data(load_methods)
        json_text = self._dict_to_json(load)
        print(json_text)
        return load


runComputer = MissionComputer()
runComputer.get_mission_computer_info()
runComputer.get_mission_computer_load()
