class SimpleRandom:
    # 선형 합동 생성기(LCG) 방식으로 난수를 만드는 클래스
    # 표준 random 라이브러리를 사용하지 않고 직접 구현한다.
    def __init__(self, seed_value):
        self.modulus = 2147483648
        self.multiplier = 1103515245
        self.increment = 12345
        self.state = seed_value % self.modulus

        if self.state == 0:
            self.state = 1

    # 내부 상태를 다음 값으로 갱신한다.
    def _next(self):
        self.state = (
            (self.multiplier * self.state + self.increment) % self.modulus
        )
        return self.state

    # 0 이상 1 미만의 실수를 반환한다.
    def random(self):
        return self._next() / self.modulus

    # start 이상 end 이하의 정수를 반환한다.
    def randint(self, start, end):
        if start > end:
            start, end = end, start

        return start + int(self.random() * (end - start + 1))

    # start 이상 end 이하 범위의 실수를 반환한다.
    def uniform(self, start, end):
        if start > end:
            start, end = end, start

        return start + (end - start) * self.random()


class SimpleDateTime:
    # 날짜와 시간을 저장하는 클래스
    def __init__(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    # 윤년 여부를 판별한다.
    @staticmethod
    def is_leap_year(year):
        if year % 400 == 0:
            return True
        if year % 100 == 0:
            return False
        if year % 4 == 0:
            return True
        return False

    # 해당 연도와 월의 마지막 날짜를 반환한다.
    @staticmethod
    def days_in_month(year, month):
        if month in (1, 3, 5, 7, 8, 10, 12):
            return 31
        if month in (4, 6, 9, 11):
            return 30
        if month == 2:
            if SimpleDateTime.is_leap_year(year):
                return 29
            return 28
        return 0

    # epoch 초를 날짜/시간 객체로 변환한다.
    # timezone_offset_hours는 시차 보정용이다.
    @classmethod
    def from_epoch(cls, epoch_seconds, timezone_offset_hours=9):
        total_seconds = epoch_seconds + (timezone_offset_hours * 3600)

        if total_seconds < 0:
            total_seconds = 0

        days = total_seconds // 86400
        remain_seconds = total_seconds % 86400

        hour = remain_seconds // 3600
        remain_seconds = remain_seconds % 3600

        minute = remain_seconds // 60
        second = remain_seconds % 60

        year = 1970

        while True:
            if cls.is_leap_year(year):
                days_in_year = 366
            else:
                days_in_year = 365

            if days >= days_in_year:
                days -= days_in_year
                year += 1
            else:
                break

        month = 1

        while True:
            month_days = cls.days_in_month(year, month)

            if days >= month_days:
                days -= month_days
                month += 1
            else:
                break

        day = days + 1

        return cls(year, month, day, hour, minute, second)

    # 날짜와 시간을 문자열로 반환한다.
    def format(self):
        return (
            f'{self.year:04d}-{self.month:02d}-{self.day:02d} '
            f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
        )


class SimpleClock:
    # 현재 시간을 가져오는 클래스
    # import 없이 Linux 시스템의 파일 정보를 직접 읽어 현재 epoch를 계산한다.
    def __init__(self, timezone_offset_hours=9):
        self.timezone_offset_hours = timezone_offset_hours

    # /proc/stat 에서 시스템 부팅 시각(epoch 초)을 읽는다.
    def _read_boot_time_epoch(self):
        with open('/proc/stat', 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split()

                if len(parts) == 2 and parts[0] == 'btime':
                    return int(parts[1])

        raise RuntimeError('부팅 시간을 읽을 수 없습니다.')

    # /proc/uptime 에서 시스템 가동 시간을 초 단위로 읽는다.
    def _read_uptime_seconds(self):
        with open('/proc/uptime', 'r', encoding='utf-8') as file:
            content = file.read().strip()

        # 첫 번째 값이 uptime이다.
        first_value = content.split()[0]

        # 소수점 이하는 버리고 초 단위 정수로 사용한다.
        return int(float(first_value))

    # Linux의 정보를 이용해 현재 epoch 초를 계산한다.
    def _read_current_epoch_linux(self):
        boot_epoch = self._read_boot_time_epoch()
        uptime_seconds = self._read_uptime_seconds()
        return boot_epoch + uptime_seconds

    # 현재 날짜/시간 객체를 반환한다.
    def now(self):
        epoch_seconds = self._read_current_epoch_linux()

        return SimpleDateTime.from_epoch(
            epoch_seconds,
            self.timezone_offset_hours
        )


class DummySensor:
    # 더미 센서 클래스
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None,
        }

        self.log_file = 'mars_base_env_log.txt'
        self.clock = SimpleClock(timezone_offset_hours=9)

        # 현재 시각을 기반으로 시드를 만든다.
        # 실패할 경우 객체 id를 섞어서 기본 시드를 만든다.
        try:
            seed_value = self.clock._read_current_epoch_linux()
        except Exception:
            seed_value = (
                id(self.env_values) +
                id(self.log_file) +
                id(self.clock)
            )

        self.random_generator = SimpleRandom(seed_value)

    # 로그 헤더가 없으면 파일에 헤더를 작성한다.
    def _write_log_header(self):
        header = (
            'datetime,'
            'mars_base_internal_temperature,'
            'mars_base_external_temperature,'
            'mars_base_internal_humidity,'
            'mars_base_external_illuminance,'
            'mars_base_internal_co2,'
            'mars_base_internal_oxygen\n'
        )

        try:
            with open(self.log_file, 'r', encoding='utf-8') as file:
                first_char = file.read(1)

            if first_char == '':
                with open(self.log_file, 'a', encoding='utf-8') as file:
                    file.write(header)

        except FileNotFoundError:
            with open(self.log_file, 'w', encoding='utf-8') as file:
                file.write(header)

    # 환경값을 랜덤으로 생성한다.
    def set_env(self):
        # 화성 기지 내부 온도: 18 ~ 30도
        self.env_values['mars_base_internal_temperature'] = (
            self.random_generator.randint(18, 30)
        )

        # 화성 기지 외부 온도: 0 ~ 21도
        self.env_values['mars_base_external_temperature'] = (
            self.random_generator.randint(0, 21)
        )

        # 화성 기지 내부 습도: 50 ~ 60%
        self.env_values['mars_base_internal_humidity'] = (
            self.random_generator.randint(50, 60)
        )

        # 화성 기지 외부 광량: 500 ~ 715 W/m2
        self.env_values['mars_base_external_illuminance'] = (
            self.random_generator.randint(500, 715)
        )

        # 화성 기지 내부 이산화탄소 농도: 0.02 ~ 0.1%
        self.env_values['mars_base_internal_co2'] = round(
            self.random_generator.uniform(0.02, 0.10),
            3
        )

        # 화성 기지 내부 산소 농도: 4.0 ~ 7.0%
        self.env_values['mars_base_internal_oxygen'] = round(
            self.random_generator.uniform(4.0, 7.0),
            3
        )

    # 환경값을 로그 파일에 저장하고 반환한다.
    def get_env(self):
        self._write_log_header()

        current_time = self.clock.now().format()

        log_line = (
            f'{current_time},'
            f'{self.env_values["mars_base_internal_temperature"]},'
            f'{self.env_values["mars_base_external_temperature"]},'
            f'{self.env_values["mars_base_internal_humidity"]},'
            f'{self.env_values["mars_base_external_illuminance"]},'
            f'{self.env_values["mars_base_internal_co2"]},'
            f'{self.env_values["mars_base_internal_oxygen"]}\n'
        )

        with open(self.log_file, 'a', encoding='utf-8') as file:
            file.write(log_line)

        return self.env_values


# DummySensor 클래스의 인스턴스를 ds라는 이름으로 생성한다.
ds = DummySensor()

# 랜덤 환경값을 생성한다.
ds.set_env()

# 환경값을 가져오고 로그 파일에 저장한다.
env_data = ds.get_env()

# 현재 환경값을 화면에 출력한다.
for key, value in env_data.items():
    print(f'{key}: {value}')
