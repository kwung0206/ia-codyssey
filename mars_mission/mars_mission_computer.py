import random
from datetime import datetime


class DummySensor:
    # DummySensor 클래스의 생성자
    # 환경값을 저장할 사전 객체를 초기화한다.
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None,
        }

        # 로그 파일 이름을 저장한다.
        self.log_file = 'mars_base_env_log.txt'

    # 환경값을 무작위로 생성하여 env_values에 저장하는 메소드
    def set_env(self):
        # 화성 기지 내부 온도: 18 ~ 30도
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)

        # 화성 기지 외부 온도: 0 ~ 21도
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)

        # 화성 기지 내부 습도: 50 ~ 60%
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)

        # 화성 기지 외부 광량: 500 ~ 715 W/m2
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)

        # 화성 기지 내부 이산화탄소 농도: 0.02 ~ 0.1%
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.10), 3)

        # 화성 기지 내부 산소 농도: 4.0 ~ 7.0%
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 3)

    # 로그 파일이 비어 있거나 존재하지 않으면 헤더를 작성하는 메소드
    def _write_log_header(self):
        # 기록할 항목명을 한 줄 문자열로 만든다.
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
            # 기존 파일 내용을 읽어서 비어 있는지 확인한다.
            with open(self.log_file, 'r', encoding='utf-8') as file:
                content = file.read()

            # 파일이 비어 있으면 헤더를 추가한다.
            if not content:
                with open(self.log_file, 'a', encoding='utf-8') as file:
                    file.write(header)

        except FileNotFoundError:
            # 파일이 없으면 새로 만들고 헤더를 작성한다.
            with open(self.log_file, 'w', encoding='utf-8') as file:
                file.write(header)

    # 환경값을 반환하고 로그 파일에 저장하는 메소드
    def get_env(self):
        # 로그 파일 헤더를 먼저 확인하고 필요하면 작성한다.
        self._write_log_header()

        # 현재 날짜와 시간을 문자열로 생성한다.
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 환경값과 시간을 CSV 형식의 한 줄 문자열로 만든다.
        log_line = (
            f'{current_time},'
            f'{self.env_values["mars_base_internal_temperature"]},'
            f'{self.env_values["mars_base_external_temperature"]},'
            f'{self.env_values["mars_base_internal_humidity"]},'
            f'{self.env_values["mars_base_external_illuminance"]},'
            f'{self.env_values["mars_base_internal_co2"]},'
            f'{self.env_values["mars_base_internal_oxygen"]}\n'
        )

        # 로그 파일에 한 줄 추가한다.
        with open(self.log_file, 'a', encoding='utf-8') as file:
            file.write(log_line)

        # 현재 환경값 사전을 반환한다.
        return self.env_values


# DummySensor 클래스의 인스턴스를 ds라는 이름으로 생성한다.
ds = DummySensor()

# 무작위 환경값을 생성한다.
ds.set_env()

# 생성된 환경값을 가져오고 로그 파일에도 저장한다.
env_data = ds.get_env()

# 반환된 환경값을 화면에 출력한다.
for key, value in env_data.items():
    print(f'{key}: {value}')
