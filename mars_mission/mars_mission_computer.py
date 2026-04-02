# 간단한 난수 생성기를 만드는 클래스이다.
class SimpleRandom:
    # 표준 random 라이브러리 대신 사용할 간단한 난수 생성기라는 설명이다.
    # 선형 합동 생성기(LCG) 방식으로 구현한다는 설명이다.

    # 객체가 생성될 때 초기 시드값을 받아 내부 상태를 준비하는 생성자이다.
    def __init__(self, seed):
        # 난수 계산에 사용할 나머지 기준값(모듈러)을 저장한다.
        self.modulus = 2147483647

        # 난수 계산에 사용할 곱셈 상수를 저장한다.
        self.multiplier = 1103515245

        # 난수 계산에 사용할 증가값을 저장한다.
        self.increment = 12345

        # 전달받은 시드를 모듈러 값으로 나눈 나머지로 초기 상태를 만든다.
        self.state = seed % self.modulus

        # 만약 계산된 상태값이 0이면,
        if self.state == 0:
            # 상태값을 1로 바꿔서 0 고정 상태를 피한다.
            self.state = 1

    # 다음 난수 상태를 만든다는 설명이다.
    def _next(self):
        # 선형 합동 공식으로 다음 상태값을 계산하여 저장한다.
        self.state = (
            # multiplier * state + increment 값을 modulus로 나눈 나머지를 구한다.
            (self.multiplier * self.state + self.increment) % self.modulus
        )

        # 새로 계산된 상태값을 반환한다.
        return self.state

    # 0 이상 1 미만의 실수를 반환한다는 설명이다.
    def random(self):
        # 다음 상태값을 modulus로 나누어 0~1 사이 실수 형태로 반환한다.
        return self._next() / self.modulus

    # start 이상 end 이하의 정수를 반환한다는 설명이다.
    def randint(self, start, end):
        # start가 end보다 크면,
        if start > end:
            # start 값을 임시 변수에 저장한다.
            temp = start

            # start에 end 값을 넣는다.
            start = end

            # end에 원래 start 값을 넣는다.
            end = temp

        # 0~1 미만 실수를 이용해 start~end 범위의 정수를 만들어 반환한다.
        return start + int(self.random() * (end - start + 1))

    # start 이상 end 이하의 실수를 반환한다는 설명이다.
    def uniform(self, start, end):
        # start가 end보다 크면,
        if start > end:
            # start 값을 임시 변수에 저장한다.
            temp = start

            # start에 end 값을 넣는다.
            start = end

            # end에 원래 start 값을 넣는다.
            end = temp

        # 0~1 미만 실수를 비율로 사용해 start~end 범위의 실수를 만들어 반환한다.
        return start + (end - start) * self.random()


# 더미 센서를 표현하는 클래스이다.
class DummySensor:
    # 더미 센서 클래스라는 설명이다.
    # env_values 사전에 환경 데이터를 저장한다는 설명이다.

    # 객체가 생성될 때 환경값 저장소와 난수 생성기를 준비하는 생성자이다.
    def __init__(self):
        # 환경 데이터를 저장할 딕셔너리를 만든다.
        self.env_values = {
            # 내부 온도 항목을 만들고 초기값은 None으로 둔다.
            'mars_base_internal_temperature': None,

            # 외부 온도 항목을 만들고 초기값은 None으로 둔다.
            'mars_base_external_temperature': None,

            # 내부 습도 항목을 만들고 초기값은 None으로 둔다.
            'mars_base_internal_humidity': None,

            # 외부 조도 항목을 만들고 초기값은 None으로 둔다.
            'mars_base_external_illuminance': None,

            # 내부 이산화탄소 항목을 만들고 초기값은 None으로 둔다.
            'mars_base_internal_co2': None,

            # 내부 산소 항목을 만들고 초기값은 None으로 둔다.
            'mars_base_internal_oxygen': None,
        }

        # import 없이 시드 값을 만들기 위해 객체 id 값을 조합한다는 설명이다.
        seed_value = (
            # 현재 객체 자신의 id 값을 더한다.
            id(self) +
            # 환경값 딕셔너리 객체의 id 값을 더한다.
            id(self.env_values) +
            # 딕셔너리 키 목록 뷰의 id 값을 더한다.
            id(self.env_values.keys()) +
            # 딕셔너리 값 목록 뷰의 id 값을 더한다.
            id(self.env_values.values())
        )

        # 위에서 만든 seed_value를 이용해 SimpleRandom 객체를 생성한다.
        self.random_generator = SimpleRandom(seed_value)

    # 문제에서 요구한 범위에 맞춰 환경값을 랜덤으로 생성한다는 설명이다.
    def set_env(self):
        # 내부 온도를 18~30 범위 정수로 생성하여 저장한다.
        self.env_values['mars_base_internal_temperature'] = (
            # randint를 사용해 18 이상 30 이하 정수를 만든다.
            self.random_generator.randint(18, 30)
        )

        # 외부 온도를 0~21 범위 정수로 생성하여 저장한다.
        self.env_values['mars_base_external_temperature'] = (
            # randint를 사용해 0 이상 21 이하 정수를 만든다.
            self.random_generator.randint(0, 21)
        )

        # 내부 습도를 50~60 범위 정수로 생성하여 저장한다.
        self.env_values['mars_base_internal_humidity'] = (
            # randint를 사용해 50 이상 60 이하 정수를 만든다.
            self.random_generator.randint(50, 60)
        )

        # 외부 조도를 500~715 범위 정수로 생성하여 저장한다.
        self.env_values['mars_base_external_illuminance'] = (
            # randint를 사용해 500 이상 715 이하 정수를 만든다.
            self.random_generator.randint(500, 715)
        )

        # 내부 이산화탄소 농도를 0.02~0.10 범위 실수로 생성하고 소수 셋째 자리까지 반올림해 저장한다.
        self.env_values['mars_base_internal_co2'] = round(
            # uniform을 사용해 0.02 이상 0.10 이하 실수를 만든다.
            self.random_generator.uniform(0.02, 0.10),
            # 소수점 셋째 자리까지 남기도록 반올림 자릿수를 지정한다.
            3
        )

        # 내부 산소 농도를 4.0~7.0 범위 실수로 생성하고 소수 셋째 자리까지 반올림해 저장한다.
        self.env_values['mars_base_internal_oxygen'] = round(
            # uniform을 사용해 4.0 이상 7.0 이하 실수를 만든다.
            self.random_generator.uniform(4.0, 7.0),
            # 소수점 셋째 자리까지 남기도록 반올림 자릿수를 지정한다.
            3
        )

    # 현재 환경값 사전을 반환한다는 설명이다.
    def get_env(self):
        # 현재 저장된 환경값 딕셔너리를 그대로 반환한다.
        return self.env_values


# 미션 컴퓨터를 표현하는 클래스이다.
class MissionComputer:
    # 미션 컴퓨터 클래스라는 설명이다.

    # 객체가 생성될 때 마지막 센서 데이터를 저장할 공간을 만드는 생성자이다.
    def __init__(self):
        # 아직 읽은 센서 데이터가 없으므로 None으로 초기화한다.
        self.last_sensor_data = None

    # DummySensor 객체를 인자로 전달받아 데이터를 읽어온다는 설명이다.
    # 전달 방법은 "메소드 매개변수 전달 방식"이라는 설명이다.
    def get_sensor_data(self, sensor):
        # 전달받은 sensor 객체에서 새 환경값을 생성하도록 set_env를 호출한다.
        sensor.set_env()

        # sensor 객체의 환경값을 가져와 last_sensor_data에 저장한다.
        self.last_sensor_data = sensor.get_env()

        # 마지막으로 저장한 센서 데이터를 반환한다.
        return self.last_sensor_data

    # 문자열을 JSON 문자열 규칙에 맞게 이스케이프 처리한다는 설명이다.
    def _escape_json_string(self, text):
        # 변환된 결과를 담을 빈 문자열을 준비한다.
        result = ''

        # 입력 문자열의 각 문자를 하나씩 꺼내 반복한다.
        for char in text:
            # 현재 문자가 역슬래시라면,
            if char == '\\':
                # JSON 문자열 규칙에 맞게 역슬래시 두 개로 바꿔 추가한다.
                result += '\\\\'

            # 현재 문자가 큰따옴표라면,
            elif char == '"':
                # JSON 문자열 규칙에 맞게 이스케이프된 큰따옴표로 바꿔 추가한다.
                result += '\\"'

            # 현재 문자가 줄바꿈 문자라면,
            elif char == '\n':
                # JSON 문자열 규칙에 맞게 \n 형태로 추가한다.
                result += '\\n'

            # 현재 문자가 탭 문자라면,
            elif char == '\t':
                # JSON 문자열 규칙에 맞게 \t 형태로 추가한다.
                result += '\\t'

            # 위 특수문자들에 해당하지 않으면,
            else:
                # 원래 문자를 그대로 결과 문자열에 추가한다.
                result += char

        # 변환이 끝난 문자열을 반환한다.
        return result

    # 값 하나를 JSON 문자열 형태로 바꾼다는 설명이다.
    def _value_to_json_text(self, value):
        # 값이 None이면,
        if value is None:
            # JSON의 null 문자열을 반환한다.
            return 'null'

        # 값이 불리언(bool) 타입이면,
        if isinstance(value, bool):
            # 값이 True이면,
            if value:
                # JSON의 true 문자열을 반환한다.
                return 'true'

            # 값이 False이면 false 문자열을 반환한다.
            return 'false'

        # 값이 문자열(str) 타입이면,
        if isinstance(value, str):
            # 문자열 내부 특수문자를 JSON 규칙에 맞게 이스케이프 처리한다.
            escaped_text = self._escape_json_string(value)

            # 큰따옴표로 감싼 JSON 문자열 형태로 반환한다.
            return f'"{escaped_text}"'

        # 위의 경우가 아니면 숫자 등 일반 값을 문자열로 바꿔 반환한다.
        return str(value)

    # 딕셔너리를 json 모듈 없이 직접 JSON 문자열로 만든다는 설명이다.
    def dict_to_json_text(self, data):
        # JSON 문자열 시작 부분인 여는 중괄호와 줄바꿈을 먼저 넣는다.
        json_text = '{\n'

        # 딕셔너리 항목 개수를 저장한다.
        item_count = len(data)

        # 현재 몇 번째 항목을 처리 중인지 세기 위한 변수를 0으로 시작한다.
        current_index = 0

        # 딕셔너리의 각 키를 하나씩 반복한다.
        for key in data:
            # 현재 처리 중인 항목 번호를 1 증가시킨다.
            current_index += 1

            # 키를 문자열로 바꾸고 JSON 규칙에 맞게 이스케이프 처리한다.
            key_text = self._escape_json_string(str(key))

            # 해당 키의 값을 JSON 문자열 형태로 변환한다.
            value_text = self._value_to_json_text(data[key])

            # "키": 값 형식의 한 줄을 JSON 문자열에 추가한다.
            json_text += f'  "{key_text}": {value_text}'

            # 현재 항목이 마지막 항목이 아니라면,
            if current_index < item_count:
                # JSON 문법에 맞게 뒤에 쉼표를 붙인다.
                json_text += ','

            # 각 항목 뒤에 줄바꿈을 추가한다.
            json_text += '\n'

        # JSON 문자열 끝 부분인 닫는 중괄호를 붙인다.
        json_text += '}'

        # 완성된 JSON 문자열을 반환한다.
        return json_text

    # 센서 데이터를 JSON 형식으로 화면에 출력한다는 설명이다.
    def print_sensor_data(self, sensor):
        # 전달받은 센서 객체에서 최신 센서 데이터를 읽어온다.
        sensor_data = self.get_sensor_data(sensor)

        # 읽어온 딕셔너리 데이터를 JSON 문자열로 변환한다.
        json_text = self.dict_to_json_text(sensor_data)

        # JSON 문자열을 화면에 출력한다.
        print(json_text)


# MissionComputer 클래스를 RunComputer로 인스턴스화한다.
RunComputer = MissionComputer()

# DummySensor 클래스를 ds로 인스턴스화한다.
ds = DummySensor()

# RunComputer의 get_sensor_data() 메소드에 ds를 전달한다.
# 즉, DummySensor 전달 방식은 "메소드 인자 전달"이다.
sensor_data = RunComputer.get_sensor_data(ds)

# 받아온 데이터를 json 형식 문자열로 직접 만들어 화면에 출력한다.
print('초기 센서 데이터')

# sensor_data 딕셔너리를 JSON 문자열로 변환한 뒤 출력한다.
print(RunComputer.dict_to_json_text(sensor_data))

# 줄바꿈 후 print_sensor_data() 호출 결과라는 안내 문구를 출력한다.
print('\nprint_sensor_data() 호출 결과')

# print_sensor_data()를 호출하여 새 센서값을 다시 읽고 JSON 형식으로 출력한다.
RunComputer.print_sensor_data(ds)
