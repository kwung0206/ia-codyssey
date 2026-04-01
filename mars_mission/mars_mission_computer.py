class SimpleRandom:
    # 표준 random 라이브러리 대신 사용할 간단한 난수 생성기
    # 선형 합동 생성기(LCG) 방식으로 구현한다.
    def __init__(self, seed):
        self.modulus = 2147483647
        self.multiplier = 1103515245
        self.increment = 12345
        self.state = seed % self.modulus

        if self.state == 0:
            self.state = 1

    # 다음 난수 상태를 만든다.
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
            temp = start
            start = end
            end = temp

        return start + int(self.random() * (end - start + 1))

    # start 이상 end 이하의 실수를 반환한다.
    def uniform(self, start, end):
        if start > end:
            temp = start
            start = end
            end = temp

        return start + (end - start) * self.random()


class DummySensor:
    # 더미 센서 클래스
    # env_values 사전에 환경 데이터를 저장한다.
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None,
        }

        # import 없이 시드 값을 만들기 위해 객체 id 값을 조합한다.
        seed_value = (
            id(self) +
            id(self.env_values) +
            id(self.env_values.keys()) +
            id(self.env_values.values())
        )

        self.random_generator = SimpleRandom(seed_value)

    # 문제에서 요구한 범위에 맞춰 환경값을 랜덤으로 생성한다.
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = (
            self.random_generator.randint(18, 30)
        )

        self.env_values['mars_base_external_temperature'] = (
            self.random_generator.randint(0, 21)
        )

        self.env_values['mars_base_internal_humidity'] = (
            self.random_generator.randint(50, 60)
        )

        self.env_values['mars_base_external_illuminance'] = (
            self.random_generator.randint(500, 715)
        )

        self.env_values['mars_base_internal_co2'] = round(
            self.random_generator.uniform(0.02, 0.10),
            3
        )

        self.env_values['mars_base_internal_oxygen'] = round(
            self.random_generator.uniform(4.0, 7.0),
            3
        )

    # 현재 환경값 사전을 반환한다.
    def get_env(self):
        return self.env_values


class MissionComputer:
    # 미션 컴퓨터 클래스
    def __init__(self):
        self.last_sensor_data = None

    # DummySensor 객체를 인자로 전달받아 데이터를 읽어온다.
    # 전달 방법은 "메소드 매개변수 전달 방식"이다.
    def get_sensor_data(self, sensor):
        sensor.set_env()
        self.last_sensor_data = sensor.get_env()
        return self.last_sensor_data

    # 문자열을 JSON 문자열 규칙에 맞게 이스케이프 처리한다.
    def _escape_json_string(self, text):
        result = ''

        for char in text:
            if char == '\\':
                result += '\\\\'
            elif char == '"':
                result += '\\"'
            elif char == '\n':
                result += '\\n'
            elif char == '\t':
                result += '\\t'
            else:
                result += char

        return result

    # 값 하나를 JSON 문자열 형태로 바꾼다.
    def _value_to_json_text(self, value):
        if value is None:
            return 'null'

        if isinstance(value, bool):
            if value:
                return 'true'
            return 'false'

        if isinstance(value, str):
            escaped_text = self._escape_json_string(value)
            return f'"{escaped_text}"'

        return str(value)

    # 딕셔너리를 json 모듈 없이 직접 JSON 문자열로 만든다.
    def dict_to_json_text(self, data):
        json_text = '{\n'
        item_count = len(data)
        current_index = 0

        for key in data:
            current_index += 1
            key_text = self._escape_json_string(str(key))
            value_text = self._value_to_json_text(data[key])

            json_text += f'  "{key_text}": {value_text}'

            if current_index < item_count:
                json_text += ','

            json_text += '\n'

        json_text += '}'

        return json_text

    # 센서 데이터를 JSON 형식으로 화면에 출력한다.
    def print_sensor_data(self, sensor):
        sensor_data = self.get_sensor_data(sensor)
        json_text = self.dict_to_json_text(sensor_data)
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
print(RunComputer.dict_to_json_text(sensor_data))

print('\nprint_sensor_data() 호출 결과')
RunComputer.print_sensor_data(ds)
