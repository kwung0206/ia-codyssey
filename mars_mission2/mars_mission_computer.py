# 시간 처리를 위해 time 모듈을 불러온다.
import time


# 더미 센서 클래스를 정의한다.
class DummySensor:
    # 객체가 생성될 때 실행되는 생성자 메소드이다.
    def __init__(self):
        # 현재 시간을 이용해서 난수 생성용 시드를 만든다.
        self.seed = int(time.time() * 1000) % 2147483647

        # 시드가 0이면 값의 변화가 단조로울 수 있으므로 1로 바꾼다.
        if self.seed == 0:
            self.seed = 1

    # 다음 난수 값을 만드는 내부 메소드이다.
    def _next_random(self):
        # 선형 합동 방식으로 새로운 시드를 계산한다.
        self.seed = (1103515245 * self.seed + 12345) % 2147483647

        # 계산된 시드를 반환한다.
        return self.seed

    # 최소값과 최대값 사이의 실수 값을 만드는 내부 메소드이다.
    def _make_value(self, min_value, max_value):
        # 0 이상 1 이하의 비율값을 만든다.
        ratio = self._next_random() / 2147483647

        # 비율값을 이용해 원하는 범위의 값을 계산한다.
        value = min_value + (max_value - min_value) * ratio

        # 소수 둘째 자리까지 반올림해서 반환한다.
        return round(value, 2)

    # 화성 기지 내부 온도를 반환하는 메소드이다.
    def get_mars_base_internal_temperature(self):
        # 내부 온도를 18.0도에서 30.0도 사이 값으로 반환한다.
        return self._make_value(18.0, 30.0)

    # 화성 기지 외부 온도를 반환하는 메소드이다.
    def get_mars_base_external_temperature(self):
        # 외부 온도를 -120.0도에서 5.0도 사이 값으로 반환한다.
        return self._make_value(-120.0, 5.0)

    # 화성 기지 내부 습도를 반환하는 메소드이다.
    def get_mars_base_internal_humidity(self):
        # 내부 습도를 20.0퍼센트에서 60.0퍼센트 사이 값으로 반환한다.
        return self._make_value(20.0, 60.0)

    # 화성 기지 외부 광량을 반환하는 메소드이다.
    def get_mars_base_external_illuminance(self):
        # 외부 광량을 0.0에서 100000.0 사이 값으로 반환한다.
        return self._make_value(0.0, 100000.0)

    # 화성 기지 내부 이산화탄소 농도를 반환하는 메소드이다.
    def get_mars_base_internal_co2(self):
        # 내부 이산화탄소 농도를 300.0ppm에서 2000.0ppm 사이 값으로 반환한다.
        return self._make_value(300.0, 2000.0)

    # 화성 기지 내부 산소 농도를 반환하는 메소드이다.
    def get_mars_base_internal_oxygen(self):
        # 내부 산소 농도를 18.0퍼센트에서 23.0퍼센트 사이 값으로 반환한다.
        return self._make_value(18.0, 23.0)


# 문제 조건에 맞게 DummySensor를 ds라는 이름으로 인스턴스화한다.
ds = DummySensor()


# 미션 컴퓨터 클래스를 정의한다.
class MissionComputer:
    # 객체가 생성될 때 실행되는 생성자 메소드이다.
    def __init__(self):
        # 환경값을 저장할 사전 객체를 만든다.
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None,
        }

        # 5분 평균 계산을 위한 측정값 저장 버퍼를 만든다.
        self.average_buffer = {
            'mars_base_internal_temperature': [],
            'mars_base_external_temperature': [],
            'mars_base_internal_humidity': [],
            'mars_base_external_illuminance': [],
            'mars_base_internal_co2': [],
            'mars_base_internal_oxygen': [],
        }

        # 평균 계산 시작 시각을 현재 시각으로 저장한다.
        self.average_start_time = time.time()

    # 센서값을 읽어와 env_values에 저장하는 메소드이다.
    def _load_sensor_data(self):
        # 내부 온도 값을 읽어 사전에 저장한다.
        self.env_values['mars_base_internal_temperature'] = (
            ds.get_mars_base_internal_temperature()
        )

        # 외부 온도 값을 읽어 사전에 저장한다.
        self.env_values['mars_base_external_temperature'] = (
            ds.get_mars_base_external_temperature()
        )

        # 내부 습도 값을 읽어 사전에 저장한다.
        self.env_values['mars_base_internal_humidity'] = (
            ds.get_mars_base_internal_humidity()
        )

        # 외부 광량 값을 읽어 사전에 저장한다.
        self.env_values['mars_base_external_illuminance'] = (
            ds.get_mars_base_external_illuminance()
        )

        # 내부 이산화탄소 농도 값을 읽어 사전에 저장한다.
        self.env_values['mars_base_internal_co2'] = (
            ds.get_mars_base_internal_co2()
        )

        # 내부 산소 농도 값을 읽어 사전에 저장한다.
        self.env_values['mars_base_internal_oxygen'] = (
            ds.get_mars_base_internal_oxygen()
        )

    # 딕셔너리를 JSON 형태 문자열로 만드는 메소드이다.
    def _dict_to_json_text(self, data):
        # JSON 문자열의 각 줄을 저장할 리스트를 만든다.
        lines = []

        # JSON 시작 괄호를 추가한다.
        lines.append('{')

        # 딕셔너리 항목들을 리스트로 만든다.
        items = list(data.items())

        # 각 항목을 순서대로 처리한다.
        for index, item in enumerate(items):
            # 현재 항목의 키를 가져온다.
            key = item[0]

            # 현재 항목의 값을 가져온다.
            value = item[1]

            # 마지막 항목이 아니면 쉼표를 붙인다.
            if index < len(items) - 1:
                comma = ','
            else:
                comma = ''

            # 값이 실수이면 소수 둘째 자리까지 문자열로 만든다.
            if isinstance(value, float):
                value_text = '%.2f' % value

            # 값이 None이면 null 문자열로 만든다.
            elif value is None:
                value_text = 'null'

            # 그 외에는 일반 문자열로 바꾼다.
            else:
                value_text = str(value)

            # JSON 한 줄 형태로 만들어 리스트에 추가한다.
            lines.append('    "%s": %s%s' % (key, value_text, comma))

        # JSON 끝 괄호를 추가한다.
        lines.append('}')

        # 각 줄을 줄바꿈 문자로 합쳐 반환한다.
        return '\n'.join(lines)

    # 현재 환경값을 출력하는 메소드이다.
    def _print_env_values(self):
        # 환경값 사전을 JSON 문자열로 변환한다.
        json_text = self._dict_to_json_text(self.env_values)

        # JSON 문자열을 화면에 출력한다.
        print(json_text)

        # 보기 좋게 빈 줄을 하나 출력한다.
        print('')

    # 현재 환경값을 평균 계산 버퍼에 저장하는 메소드이다.
    def _save_average_data(self):
        # 내부 온도 값을 평균 버퍼에 추가한다.
        self.average_buffer['mars_base_internal_temperature'].append(
            self.env_values['mars_base_internal_temperature']
        )

        # 외부 온도 값을 평균 버퍼에 추가한다.
        self.average_buffer['mars_base_external_temperature'].append(
            self.env_values['mars_base_external_temperature']
        )

        # 내부 습도 값을 평균 버퍼에 추가한다.
        self.average_buffer['mars_base_internal_humidity'].append(
            self.env_values['mars_base_internal_humidity']
        )

        # 외부 광량 값을 평균 버퍼에 추가한다.
        self.average_buffer['mars_base_external_illuminance'].append(
            self.env_values['mars_base_external_illuminance']
        )

        # 내부 이산화탄소 농도 값을 평균 버퍼에 추가한다.
        self.average_buffer['mars_base_internal_co2'].append(
            self.env_values['mars_base_internal_co2']
        )

        # 내부 산소 농도 값을 평균 버퍼에 추가한다.
        self.average_buffer['mars_base_internal_oxygen'].append(
            self.env_values['mars_base_internal_oxygen']
        )

    # 리스트의 평균을 계산하는 메소드이다.
    def _calculate_average(self, values):
        # 값이 하나도 없으면 0.0을 반환한다.
        if len(values) == 0:
            return 0.0

        # 합계를 저장할 변수를 만든다.
        total = 0.0

        # 리스트의 값을 하나씩 더한다.
        for value in values:
            total = total + value

        # 평균을 계산해서 소수 둘째 자리까지 반올림한다.
        return round(total / len(values), 2)

    # 5분 평균값을 출력하는 메소드이다.
    def _print_five_minute_average(self):
        # 평균값을 저장할 사전을 만든다.
        average_values = {}

        # 내부 온도 평균값을 계산한다.
        average_values['mars_base_internal_temperature'] = (
            self._calculate_average(
                self.average_buffer['mars_base_internal_temperature']
            )
        )

        # 외부 온도 평균값을 계산한다.
        average_values['mars_base_external_temperature'] = (
            self._calculate_average(
                self.average_buffer['mars_base_external_temperature']
            )
        )

        # 내부 습도 평균값을 계산한다.
        average_values['mars_base_internal_humidity'] = (
            self._calculate_average(
                self.average_buffer['mars_base_internal_humidity']
            )
        )

        # 외부 광량 평균값을 계산한다.
        average_values['mars_base_external_illuminance'] = (
            self._calculate_average(
                self.average_buffer['mars_base_external_illuminance']
            )
        )

        # 내부 이산화탄소 농도 평균값을 계산한다.
        average_values['mars_base_internal_co2'] = (
            self._calculate_average(
                self.average_buffer['mars_base_internal_co2']
            )
        )

        # 내부 산소 농도 평균값을 계산한다.
        average_values['mars_base_internal_oxygen'] = (
            self._calculate_average(
                self.average_buffer['mars_base_internal_oxygen']
            )
        )

        # 5분 평균값 안내 문구를 출력한다.
        print('5분 평균값')

        # 평균값을 JSON 형태로 출력한다.
        print(self._dict_to_json_text(average_values))

        # 보기 좋게 빈 줄을 하나 출력한다.
        print('')

        # 평균 출력 후 버퍼를 초기화한다.
        self.average_buffer = {
            'mars_base_internal_temperature': [],
            'mars_base_external_temperature': [],
            'mars_base_internal_humidity': [],
            'mars_base_external_illuminance': [],
            'mars_base_internal_co2': [],
            'mars_base_internal_oxygen': [],
        }

        # 다음 평균 계산을 위해 시작 시각을 다시 저장한다.
        self.average_start_time = time.time()

    # 종료 여부를 확인하는 메소드이다.
    def _check_stop(self):
        # 사용자에게 종료 여부를 입력받는다.
        user_input = input(
            '종료하려면 q 를 입력하고, 계속하려면 Enter를 누르세요: '
        )

        # 입력값의 앞뒤 공백을 제거하고 소문자로 바꾼다.
        command = user_input.strip().lower()

        # q가 입력되면 True를 반환한다.
        if command == 'q':
            return True

        # 그 외의 경우는 False를 반환한다.
        return False

    # 센서 데이터를 반복해서 읽고 출력하는 메소드이다.
    def get_sensor_data(self):
        # 프로그램 시작 안내 문구를 출력한다.
        print('화성 기지 환경 정보를 출력합니다.')

        # 종료 방법 안내 문구를 출력한다.
        print('5초마다 다음 측정을 진행하며, 각 출력 뒤에 종료 여부를 확인합니다.')

        # 보기 좋게 빈 줄을 하나 출력한다.
        print('')

        # 무한 반복을 시작한다.
        while True:
            # 센서값을 읽어 env_values에 저장한다.
            self._load_sensor_data()

            # 현재 환경값을 JSON 형태로 출력한다.
            self._print_env_values()

            # 평균 계산을 위해 현재 값을 버퍼에 저장한다.
            self._save_average_data()

            # 평균 계산 시작 후 5분이 지났는지 확인한다.
            if time.time() - self.average_start_time >= 300:
                # 5분이 지났으면 평균값을 출력한다.
                self._print_five_minute_average()

            # 5초 동안 대기한다.
            time.sleep(5)

            # 종료 여부를 확인한다.
            should_stop = self._check_stop()

            # 종료 요청이 들어오면 반복을 종료한다.
            if should_stop:
                # 종료 메시지를 출력한다.
                print('Sytem stoped....')

                # 반복문을 빠져나간다.
                break


# 현재 파일이 직접 실행될 때만 아래 코드를 실행한다.
if __name__ == '__main__':
    # MissionComputer 클래스를 RunComputer라는 이름으로 인스턴스화한다.
    RunComputer = MissionComputer()

    # RunComputer 인스턴스의 get_sensor_data 메소드를 호출한다.
    RunComputer.get_sensor_data()
