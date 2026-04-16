import os
import time


class SystemInfo:
    @staticmethod
    def _read_first_line(path):# 운영체제 관련 기능을 사용하기 위해 os 모듈을 불러온다.
import os

# 시간 지연(1초 대기)을 사용하기 위해 time 모듈을 불러온다.
import time


# 시스템 정보를 읽어오는 기능들을 모아둔 클래스이다.
class SystemInfo:
    # 파일의 첫 번째 줄만 읽어오는 정적 메서드이다.
    @staticmethod
    def _read_first_line(path):
        try:
            # 전달받은 경로의 파일을 읽기 모드로 연다.
            file = open(path, 'r', encoding='utf-8')
            # 파일의 첫 번째 줄을 읽는다.
            line = file.readline()
            # 파일을 닫는다.
            file.close()
            # 양쪽 공백과 줄바꿈 문자를 제거한 뒤 반환한다.
            return line.strip()
        except Exception:
            # 파일을 읽는 중 문제가 생기면 빈 문자열을 반환한다.
            return ''

    # 파일의 모든 줄을 리스트 형태로 읽어오는 정적 메서드이다.
    @staticmethod
    def _read_all_lines(path):
        try:
            # 전달받은 경로의 파일을 읽기 모드로 연다.
            file = open(path, 'r', encoding='utf-8')
            # 파일의 전체 줄을 리스트로 읽는다.
            lines = file.readlines()
            # 파일을 닫는다.
            file.close()
            # 읽은 줄 목록을 반환한다.
            return lines
        except Exception:
            # 파일을 읽는 중 문제가 생기면 빈 리스트를 반환한다.
            return []

    # uname 정보를 가져오는 정적 메서드이다.
    @staticmethod
    def _get_uname():
        try:
            # 운영체제 이름, 버전, 머신 정보 등을 반환하는 os.uname()을 호출한다.
            return os.uname()
        except Exception:
            # 지원되지 않거나 오류가 발생하면 None을 반환한다.
            return None

    # 운영체제 이름을 구하는 클래스 메서드이다.
    @classmethod
    def get_operating_system(cls):
        try:
            # uname 정보를 먼저 가져온다.
            uname_info = cls._get_uname()

            # uname 정보를 정상적으로 가져왔다면
            if uname_info is not None:
                # 시스템 이름(sysname)을 반환한다. 예: Linux
                return uname_info.sysname

            # uname을 사용할 수 없으면 os.name 값을 반환한다.
            return os.name
        except Exception:
            # 예외가 발생하면 확인 불가를 반환한다.
            return '확인 불가'

    # 운영체제 버전을 구하는 클래스 메서드이다.
    @classmethod
    def get_operating_system_version(cls):
        try:
            # uname 정보를 먼저 가져온다.
            uname_info = cls._get_uname()

            # uname 정보를 정상적으로 가져왔다면
            if uname_info is not None:
                # 운영체제 릴리즈 버전(release)을 반환한다.
                return uname_info.release

            # uname을 사용할 수 없으면 확인 불가를 반환한다.
            return '확인 불가'
        except Exception:
            # 예외가 발생하면 확인 불가를 반환한다.
            return '확인 불가'

    # CPU 종류(모델명)를 구하는 클래스 메서드이다.
    @classmethod
    def get_cpu_type(cls):
        try:
            # 리눅스의 /proc/cpuinfo 파일 전체 내용을 읽는다.
            lines = cls._read_all_lines('/proc/cpuinfo')

            # 파일의 각 줄을 하나씩 확인한다.
            for line in lines:
                # ':' 문자가 있는 줄만 처리한다.
                if ':' in line:
                    # ':' 기준으로 앞은 key, 뒤는 value로 나눈다.
                    key, value = line.split(':', 1)

                    # key가 model name인지 확인한다.
                    if key.strip().lower() == 'model name':
                        # CPU 모델명을 반환한다.
                        return value.strip()

            # /proc/cpuinfo에서 못 찾았으면 uname 정보를 가져온다.
            uname_info = cls._get_uname()

            # uname 정보를 정상적으로 가져왔다면
            if uname_info is not None:
                # 머신 아키텍처 정보를 반환한다. 예: x86_64
                return uname_info.machine

            # 아무 정보도 얻지 못하면 확인 불가를 반환한다.
            return '확인 불가'
        except Exception:
            # 예외가 발생하면 확인 불가를 반환한다.
            return '확인 불가'

    # CPU 코어 개수를 구하는 정적 메서드이다.
    @staticmethod
    def get_cpu_core_count():
        try:
            # 시스템의 CPU 개수를 가져온다.
            core_count = os.cpu_count()

            # CPU 개수를 알 수 없는 경우
            if core_count is None:
                # 확인 불가를 반환한다.
                return '확인 불가'

            # CPU 개수를 반환한다.
            return core_count
        except Exception:
            # 예외가 발생하면 확인 불가를 반환한다.
            return '확인 불가'

    # 메모리 정보를 /proc/meminfo에서 읽어와 딕셔너리로 만드는 정적 메서드이다.
    @staticmethod
    def _read_meminfo():
        # 메모리 정보를 저장할 빈 딕셔너리를 만든다.
        meminfo = {}

        try:
            # /proc/meminfo 파일의 모든 줄을 읽어온다.
            lines = SystemInfo._read_all_lines('/proc/meminfo')

            # 각 줄을 하나씩 확인한다.
            for line in lines:
                # ':' 문자가 포함된 줄만 처리한다.
                if ':' in line:
                    # ':' 기준으로 key와 value를 나눈다.
                    key, value = line.split(':', 1)
                    # value 부분을 공백 기준으로 나눈다.
                    parts = value.strip().split()

                    # 값이 하나 이상 있고, 첫 번째 값이 숫자인 경우
                    if len(parts) > 0 and parts[0].isdigit():
                        # key 이름을 딕셔너리 키로, 숫자 값을 정수로 저장한다.
                        meminfo[key.strip()] = int(parts[0])

            # 완성된 메모리 정보 딕셔너리를 반환한다.
            return meminfo
        except Exception:
            # 예외가 발생하면 빈 딕셔너리를 반환한다.
            return {}

    # 전체 메모리 크기를 구하는 클래스 메서드이다.
    @classmethod
    def get_memory_size(cls):
        try:
            # 메모리 정보를 읽어온다.
            meminfo = cls._read_meminfo()
            # 전체 메모리 크기(KB)를 가져온다.
            total_kb = meminfo.get('MemTotal', 0)

            # 전체 메모리 값이 0이면 정보를 얻지 못한 것이므로
            if total_kb == 0:
                # 확인 불가를 반환한다.
                return '확인 불가'

            # KB 단위를 GB 단위로 변환한다.
            total_gb = total_kb / 1024 / 1024
            # 소수 둘째 자리까지 반올림해서 반환한다.
            return round(total_gb, 2)
        except Exception:
            # 예외가 발생하면 확인 불가를 반환한다.
            return '확인 불가'

    # CPU 사용률 계산에 필요한 총 시간과 idle 시간을 읽는 정적 메서드이다.
    @staticmethod
    def _read_cpu_times():
        try:
            # /proc/stat 파일의 첫 번째 줄을 읽어온다.
            first_line = SystemInfo._read_first_line('/proc/stat')

            # 첫 줄이 비어 있으면 정보를 읽지 못한 것이다.
            if not first_line:
                # None, None을 반환한다.
                return None, None

            # 첫 줄을 공백 기준으로 분리한다.
            parts = first_line.split()

            # 최소한 필요한 값 개수가 부족하면
            if len(parts) < 5:
                # None, None을 반환한다.
                return None, None

            # CPU 시간 값들을 저장할 리스트를 만든다.
            values = []
            # 첫 번째 요소는 'cpu' 문자열이므로 1번 인덱스부터 시작한다.
            index = 1

            # parts 끝까지 반복한다.
            while index < len(parts):
                # 각 CPU 시간 값을 정수로 변환하여 리스트에 넣는다.
                values.append(int(parts[index]))
                # 다음 인덱스로 이동한다.
                index += 1

            # idle 시간은 기본적으로 values[3]이다.
            idle = values[3]

            # iowait 값이 있으면 idle 시간에 추가한다.
            if len(values) > 4:
                idle += values[4]

            # 총 CPU 시간을 저장할 변수를 만든다.
            total = 0

            # 모든 CPU 시간 값을 더한다.
            for value in values:
                total += value

            # 총 시간과 idle 시간을 반환한다.
            return total, idle
        except Exception:
            # 예외가 발생하면 None, None을 반환한다.
            return None, None

    # CPU 사용률(%)을 계산하는 클래스 메서드이다.
    @classmethod
    def get_cpu_usage_percent(cls):
        try:
            # 첫 번째 시점의 총 시간과 idle 시간을 읽는다.
            total_1, idle_1 = cls._read_cpu_times()

            # 정보를 읽지 못한 경우
            if total_1 is None or idle_1 is None:
                # 확인 불가를 반환한다.
                return '확인 불가'

            # 1초 동안 대기한다.
            time.sleep(1)

            # 두 번째 시점의 총 시간과 idle 시간을 읽는다.
            total_2, idle_2 = cls._read_cpu_times()

            # 두 번째 정보도 읽지 못한 경우
            if total_2 is None or idle_2 is None:
                # 확인 불가를 반환한다.
                return '확인 불가'

            # 총 시간 변화량을 계산한다.
            total_diff = total_2 - total_1
            # idle 시간 변화량을 계산한다.
            idle_diff = idle_2 - idle_1

            # 총 시간 변화량이 0 이하이면 계산이 비정상이므로
            if total_diff <= 0:
                # 0.0을 반환한다.
                return 0.0

            # CPU 사용률을 계산한다.
            cpu_usage = (total_diff - idle_diff) / total_diff * 100
            # 소수 둘째 자리까지 반올림하여 반환한다.
            return round(cpu_usage, 2)
        except Exception:
            # 예외가 발생하면 확인 불가를 반환한다.
            return '확인 불가'

    # 메모리 사용률(%)을 계산하는 클래스 메서드이다.
    @classmethod
    def get_memory_usage_percent(cls):
        try:
            # 메모리 정보를 읽어온다.
            meminfo = cls._read_meminfo()

            # 전체 메모리(KB)를 가져온다.
            total_kb = meminfo.get('MemTotal', 0)
            # 사용 가능한 메모리(KB)를 가져온다.
            available_kb = meminfo.get('MemAvailable', 0)

            # 전체 메모리가 0이면 계산할 수 없으므로
            if total_kb == 0:
                # 확인 불가를 반환한다.
                return '확인 불가'

            # MemAvailable 값이 없거나 0인 경우
            if available_kb == 0:
                # 남은 메모리 값을 가져온다.
                free_kb = meminfo.get('MemFree', 0)
                # 버퍼 메모리 값을 가져온다.
                buffers_kb = meminfo.get('Buffers', 0)
                # 캐시 메모리 값을 가져온다.
                cached_kb = meminfo.get('Cached', 0)
                # 사용 가능한 메모리를 직접 계산한다.
                available_kb = free_kb + buffers_kb + cached_kb

            # 사용 중인 메모리 크기를 계산한다.
            used_kb = total_kb - available_kb
            # 메모리 사용률을 계산한다.
            memory_usage = used_kb / total_kb * 100

            # 소수 둘째 자리까지 반올림하여 반환한다.
            return round(memory_usage, 2)
        except Exception:
            # 예외가 발생하면 확인 불가를 반환한다.
            return '확인 불가'


# 미션 컴퓨터 관련 설정과 정보 출력 기능을 담당하는 클래스이다.
class MissionComputer:
    # 객체가 생성될 때 실행되는 초기화 메서드이다.
    def __init__(self, setting_path='setting.txt'):
        # 설정 파일 경로를 저장한다.
        self.setting_path = setting_path
        # 기본 설정값들을 딕셔너리로 정의한다.
        self.default_settings = {
            'operating_system': True,
            'operating_system_version': True,
            'cpu_type': True,
            'cpu_core_count': True,
            'memory_size': True,
            'cpu_usage_percent': True,
            'memory_usage_percent': True
        }
        # 설정 파일을 읽어 실제 설정값을 로드한다.
        self.settings = self._load_settings()

    # 설정 파일을 읽어 사용자 설정을 반영하는 메서드이다.
    def _load_settings(self):
        # 설정값을 저장할 빈 딕셔너리를 만든다.
        settings = {}

        # 기본 설정값들을 settings에 복사한다.
        for key in self.default_settings:
            settings[key] = self.default_settings[key]

        try:
            # 설정 파일이 존재하지 않으면
            if not os.path.exists(self.setting_path):
                # 기본 설정 그대로 반환한다.
                return settings

            # 설정 파일을 읽기 모드로 연다.
            file = open(self.setting_path, 'r', encoding='utf-8')
            # 파일의 모든 줄을 읽는다.
            lines = file.readlines()
            # 파일을 닫는다.
            file.close()

            # 설정 파일의 각 줄을 하나씩 확인한다.
            for line in lines:
                # 좌우 공백과 줄바꿈을 제거한다.
                text = line.strip()

                # 빈 줄이면 건너뛴다.
                if text == '':
                    continue

                # 주석 줄이면 건너뛴다.
                if text.startswith('#'):
                    continue

                # '=' 문자가 없으면 올바른 설정 형식이 아니므로 건너뛴다.
                if '=' not in text:
                    continue

                # '=' 기준으로 key와 value를 나눈다.
                key, value = text.split('=', 1)
                # key 양쪽 공백을 제거한다.
                key = key.strip()
                # value 양쪽 공백 제거 후 소문자로 변환한다.
                value = value.strip().lower()

                # key가 settings에 존재하는 경우에만 처리한다.
                if key in settings:
                    # 참으로 해석할 수 있는 값이면 True로 저장한다.
                    if value in ('true', '1', 'yes', 'y'):
                        settings[key] = True
                    # 거짓으로 해석할 수 있는 값이면 False로 저장한다.
                    elif value in ('false', '0', 'no', 'n'):
                        settings[key] = False

            # 최종 설정값을 반환한다.
            return settings
        except Exception:
            # 예외가 발생하면 기본 설정값을 반환한다.
            return settings

    # JSON 문자열에서 특수문자를 이스케이프 처리하는 정적 메서드이다.
    @staticmethod
    def _escape_json_string(text):
        # 전달받은 값을 문자열로 변환한다.
        result = str(text)
        # 백슬래시를 JSON 형식에 맞게 이스케이프 처리한다.
        result = result.replace('\\', '\\\\')
        # 큰따옴표를 이스케이프 처리한다.
        result = result.replace('"', '\\"')
        # 줄바꿈 문자를 \n 문자열로 바꾼다.
        result = result.replace('\n', '\\n')
        # 탭 문자를 \t 문자열로 바꾼다.
        result = result.replace('\t', '\\t')
        # 변환된 문자열을 반환한다.
        return result

    # 파이썬 값을 JSON 형식 문자열로 바꾸는 클래스 메서드이다.
    @classmethod
    def _value_to_json(cls, value):
        # 값이 bool 타입인지 확인한다.
        if isinstance(value, bool):
            # True이면 JSON의 true를 반환한다.
            if value:
                return 'true'
            # False이면 JSON의 false를 반환한다.
            return 'false'

        # 값이 None이면 JSON의 null을 반환한다.
        if value is None:
            return 'null'

        # 값이 정수형이면 문자열로 변환하여 반환한다.
        if isinstance(value, int):
            return str(value)

        # 값이 실수형이면 문자열로 변환하여 반환한다.
        if isinstance(value, float):
            return str(value)

        # 그 외 문자열 등은 큰따옴표로 감싸 JSON 문자열 형태로 반환한다.
        return '"' + cls._escape_json_string(value) + '"'

    # 딕셔너리를 JSON 문자열 형태로 만드는 클래스 메서드이다.
    @classmethod
    def _dict_to_json(cls, data):
        # JSON 각 줄을 저장할 리스트를 만든다.
        lines = []
        # JSON 시작 중괄호를 추가한다.
        lines.append('{')

        # 딕셔너리의 키 목록을 리스트로 만든다.
        keys = list(data.keys())
        # 반복용 인덱스를 0으로 시작한다.
        index = 0

        # 키 개수만큼 반복한다.
        while index < len(keys):
            # 현재 키를 가져온다.
            key = keys[index]
            # 현재 키에 해당하는 값을 가져온다.
            value = data[key]

            # 현재 한 줄의 JSON 문자열을 만든다.
            line = '    "' + cls._escape_json_string(key) + '": '
            # 값도 JSON 형식 문자열로 변환하여 이어 붙인다.
            line += cls._value_to_json(value)

            # 마지막 항목이 아니면 뒤에 쉼표를 붙인다.
            if index != len(keys) - 1:
                line += ','

            # 완성한 줄을 lines에 추가한다.
            lines.append(line)
            # 다음 인덱스로 이동한다.
            index += 1

        # JSON 종료 중괄호를 추가한다.
        lines.append('}')
        # 줄바꿈 문자로 합쳐 하나의 문자열로 반환한다.
        return '\n'.join(lines)

    # 전달받은 메서드 목록을 기반으로 데이터를 수집하는 메서드이다.
    def _collect_data(self, method_map):
        # 결과를 저장할 빈 딕셔너리를 만든다.
        result = {}

        # method_map의 각 key를 순회한다.
        for key in method_map:
            # 해당 항목이 설정에서 False이면 수집하지 않고 건너뛴다.
            if self.settings.get(key, True) is False:
                continue

            # 실제 호출할 SystemInfo 메서드 이름을 가져온다.
            method_name = method_map[key]

            try:
                # 메서드 이름으로 SystemInfo 클래스의 메서드를 가져온다.
                method = getattr(SystemInfo, method_name)
                # 해당 메서드를 실행한 결과를 result에 저장한다.
                result[key] = method()
            except Exception as error:
                # 오류가 발생하면 오류 메시지를 문자열로 저장한다.
                result[key] = '오류 발생: ' + str(error)

        # 수집된 결과 딕셔너리를 반환한다.
        return result

    # 미션 컴퓨터의 기본 정보를 출력하고 반환하는 메서드이다.
    def get_mission_computer_info(self):
        # 수집할 정보 항목과 SystemInfo 메서드 이름을 매핑한다.
        info_methods = {
            'operating_system': 'get_operating_system',
            'operating_system_version': 'get_operating_system_version',
            'cpu_type': 'get_cpu_type',
            'cpu_core_count': 'get_cpu_core_count',
            'memory_size': 'get_memory_size'
        }

        # 필요한 정보를 수집한다.
        info = self._collect_data(info_methods)
        # 수집한 딕셔너리를 JSON 문자열로 변환한다.
        json_text = self._dict_to_json(info)
        # JSON 문자열을 출력한다.
        print(json_text)
        # 원본 딕셔너리를 반환한다.
        return info

    # 미션 컴퓨터의 부하 정보(CPU, 메모리 사용률)를 출력하고 반환하는 메서드이다.
    def get_mission_computer_load(self):
        # 수집할 부하 항목과 SystemInfo 메서드 이름을 매핑한다.
        load_methods = {
            'cpu_usage_percent': 'get_cpu_usage_percent',
            'memory_usage_percent': 'get_memory_usage_percent'
        }

        # 필요한 부하 정보를 수집한다.
        load = self._collect_data(load_methods)
        # 수집한 딕셔너리를 JSON 문자열로 변환한다.
        json_text = self._dict_to_json(load)
        # JSON 문자열을 출력한다.
        print(json_text)
        # 원본 딕셔너리를 반환한다.
        return load


# MissionComputer 객체를 생성한다.
runComputer = MissionComputer()

# 미션 컴퓨터의 기본 정보를 출력한다.
runComputer.get_mission_computer_info()

# 미션 컴퓨터의 부하 정보를 출력한다.
runComputer.get_mission_computer_load()
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
