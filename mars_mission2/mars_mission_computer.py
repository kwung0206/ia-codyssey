import time
import threading


class DummySensor:
    def __init__(self):
        self._seed = int(time.time() * 1000) % 2147483647
        if self._seed == 0:
            self._seed = 1

    def _next_seed(self):
        self._seed = (1103515245 * self._seed + 12345) % 2147483647
        return self._seed

    def _make_value(self, min_value, max_value):
        ratio = self._next_seed() / 2147483647
        value = min_value + (max_value - min_value) * ratio
        return round(value, 2)

    def get_mars_base_internal_temperature(self):
        return self._make_value(18.0, 30.0)

    def get_mars_base_external_temperature(self):
        return self._make_value(-120.0, 5.0)

    def get_mars_base_internal_humidity(self):
        return self._make_value(20.0, 60.0)

    def get_mars_base_external_illuminance(self):
        return self._make_value(0.0, 100000.0)

    def get_mars_base_internal_co2(self):
        return self._make_value(300.0, 2000.0)

    def get_mars_base_internal_oxygen(self):
        return self._make_value(18.0, 23.0)


ds = DummySensor()


class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None,
        }
        self.stop_requested = False
        self.stop_key = 'q'
        self.average_start_time = time.time()
        self.average_buffer = {
            'mars_base_internal_temperature': [],
            'mars_base_external_temperature': [],
            'mars_base_internal_humidity': [],
            'mars_base_external_illuminance': [],
            'mars_base_internal_co2': [],
            'mars_base_internal_oxygen': [],
        }

    def _listen_for_stop(self):
        try:
            while not self.stop_requested:
                user_input = input()
                if user_input.strip().lower() == self.stop_key:
                    self.stop_requested = True
                    break
        except EOFError:
            return

    def _update_env_values(self):
        self.env_values['mars_base_internal_temperature'] = (
            ds.get_mars_base_internal_temperature()
        )
        self.env_values['mars_base_external_temperature'] = (
            ds.get_mars_base_external_temperature()
        )
        self.env_values['mars_base_internal_humidity'] = (
            ds.get_mars_base_internal_humidity()
        )
        self.env_values['mars_base_external_illuminance'] = (
            ds.get_mars_base_external_illuminance()
        )
        self.env_values['mars_base_internal_co2'] = (
            ds.get_mars_base_internal_co2()
        )
        self.env_values['mars_base_internal_oxygen'] = (
            ds.get_mars_base_internal_oxygen()
        )

    def _format_json(self, data):
        lines = ['{']
        items = list(data.items())

        for index, (key, value) in enumerate(items):
            comma = ',' if index < len(items) - 1 else ''

            if value is None:
                value_text = 'null'
            elif isinstance(value, float):
                value_text = f'{value:.2f}'
            else:
                value_text = str(value)

            lines.append(f'    "{key}": {value_text}{comma}')

        lines.append('}')
        return '\n'.join(lines)

    def _print_env_values(self):
        print(self._format_json(self.env_values))
        print()

    def _save_average_data(self):
        for key, value in self.env_values.items():
            self.average_buffer[key].append(value)

    def _print_average_values(self):
        average_values = {}

        for key, values in self.average_buffer.items():
            if values:
                average_values[key] = round(sum(values) / len(values), 2)
            else:
                average_values[key] = 0.0

        print('5분 평균값')
        print(self._format_json(average_values))
        print()

        self.average_buffer = {
            'mars_base_internal_temperature': [],
            'mars_base_external_temperature': [],
            'mars_base_internal_humidity': [],
            'mars_base_external_illuminance': [],
            'mars_base_internal_co2': [],
            'mars_base_internal_oxygen': [],
        }
        self.average_start_time = time.time()

    def _wait_five_seconds(self):
        for _ in range(50):
            if self.stop_requested:
                break
            time.sleep(0.1)

    def get_sensor_data(self):
        print('화성 기지 환경 정보를 5초마다 출력합니다.')
        print(f"종료하려면 '{self.stop_key}'를 입력한 뒤 Enter를 누르세요.")
        print()

        input_thread = threading.Thread(
            target=self._listen_for_stop,
            daemon=True,
        )
        input_thread.start()

        try:
            while not self.stop_requested:
                self._update_env_values()
                self._print_env_values()
                self._save_average_data()

                if time.time() - self.average_start_time >= 300:
                    self._print_average_values()

                self._wait_five_seconds()
        except KeyboardInterrupt:
            self.stop_requested = True

        print('Sytem stoped....')


if __name__ == '__main__':
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()
