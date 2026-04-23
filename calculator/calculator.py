# calculator.py

# 파이썬 기본 라이브러리인 sys를 불러온다.
import sys

# PyQt5에서 필요한 위젯 클래스를 불러온다.
from PyQt5.QtCore import Qt
# PyQt5에서 폰트 관련 클래스를 불러온다.
from PyQt5.QtGui import QFont
# PyQt5에서 애플리케이션과 UI 구성에 필요한 클래스들을 불러온다.
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
)


# 아이폰 계산기와 유사한 형태의 계산기 창을 만드는 클래스를 정의한다.
class Calculator(QWidget):
    # 클래스가 생성될 때 자동으로 실행되는 초기화 메서드이다.
    def __init__(self):
        # 부모 클래스인 QWidget의 초기화 메서드를 먼저 실행한다.
        super().__init__()

        # 현재 화면에 입력 중인 숫자를 문자열로 저장한다.
        self.current_input = '0'

        # 첫 번째 피연산자를 저장한다.
        self.left_operand = None

        # 현재 선택된 연산자(+, -, ×, ÷)를 저장한다.
        self.operator = None

        # 직전에 '=' 버튼을 눌렀는지 여부를 저장한다.
        self.just_calculated = False

        # 계산기 UI를 구성하는 메서드를 호출한다.
        self.init_ui()

    # 계산기 창의 전체 UI를 구성하는 메서드이다.
    def init_ui(self):
        # 창 제목을 설정한다.
        self.setWindowTitle('iPhone Style Calculator')

        # 창의 최소 크기를 설정한다.
        self.setMinimumSize(360, 640)

        # 전체 배경색을 검정색 계열로 지정한다.
        self.setStyleSheet('background-color: #000000;')

        # 세로 방향 메인 레이아웃을 생성한다.
        main_layout = QVBoxLayout()

        # 메인 레이아웃의 바깥 여백을 설정한다.
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 위젯들 사이의 간격을 설정한다.
        main_layout.setSpacing(12)

        # 계산 결과와 입력 숫자를 보여줄 라벨을 생성한다.
        self.display = QLabel('0')

        # 표시창의 높이를 설정한다.
        self.display.setFixedHeight(140)

        # 표시창의 글자색, 배경색, 정렬 등을 설정한다.
        self.display.setStyleSheet(
            'color: white;'
            'background-color: black;'
            'padding: 10px;'
        )

        # 표시창의 글꼴을 설정한다.
        self.display.setFont(QFont('Arial', 34))

        # 표시창의 텍스트를 오른쪽 아래 정렬로 맞춘다.
        self.display.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        # 표시창을 메인 레이아웃에 추가한다.
        main_layout.addWidget(self.display)

        # 버튼들을 배치할 격자 레이아웃을 생성한다.
        grid_layout = QGridLayout()

        # 버튼 사이 가로 간격을 설정한다.
        grid_layout.setHorizontalSpacing(12)

        # 버튼 사이 세로 간격을 설정한다.
        grid_layout.setVerticalSpacing(12)

        # 버튼 정보를 행 단위로 정의한다.
        buttons = [
            [('AC', 'function'), ('+/-', 'function'), ('%', 'function'), ('÷', 'operator')],
            [('7', 'number'), ('8', 'number'), ('9', 'number'), ('×', 'operator')],
            [('4', 'number'), ('5', 'number'), ('6', 'number'), ('-', 'operator')],
            [('1', 'number'), ('2', 'number'), ('3', 'number'), ('+', 'operator')],
        ]

        # 위에서 정의한 버튼들을 순회하면서 화면에 배치한다.
        for row_index, row_buttons in enumerate(buttons):
            # 한 줄 안의 버튼들을 다시 순회한다.
            for col_index, button_info in enumerate(row_buttons):
                # 버튼에 표시될 글자를 가져온다.
                text = button_info[0]

                # 버튼 종류를 가져온다.
                button_type = button_info[1]

                # 버튼 생성 메서드를 호출해 버튼 객체를 만든다.
                button = self.create_button(text, button_type)

                # 버튼을 지정한 위치에 배치한다.
                grid_layout.addWidget(button, row_index, col_index)

        # 마지막 줄의 0 버튼은 두 칸을 차지하도록 만든다.
        zero_button = self.create_button('0', 'number')

        # 마지막 줄의 '.' 버튼을 만든다.
        dot_button = self.create_button('.', 'number')

        # 마지막 줄의 '=' 버튼을 만든다.
        equal_button = self.create_button('=', 'operator')

        # 0 버튼을 마지막 줄 첫 번째 칸부터 두 칸 차지하도록 배치한다.
        grid_layout.addWidget(zero_button, 4, 0, 1, 2)

        # . 버튼을 마지막 줄 세 번째 칸에 배치한다.
        grid_layout.addWidget(dot_button, 4, 2)

        # = 버튼을 마지막 줄 네 번째 칸에 배치한다.
        grid_layout.addWidget(equal_button, 4, 3)

        # 모든 행의 크기가 균등하게 늘어나도록 설정한다.
        for row_index in range(5):
            # 각 행의 stretch 값을 1로 설정한다.
            grid_layout.setRowStretch(row_index, 1)

        # 모든 열의 크기가 균등하게 늘어나도록 설정한다.
        for col_index in range(4):
            # 각 열의 stretch 값을 1로 설정한다.
            grid_layout.setColumnStretch(col_index, 1)

        # 버튼 영역을 메인 레이아웃에 추가한다.
        main_layout.addLayout(grid_layout)

        # 현재 창의 메인 레이아웃으로 설정한다.
        self.setLayout(main_layout)

    # 버튼 하나를 생성해서 반환하는 메서드이다.
    def create_button(self, text, button_type):
        # QPushButton 객체를 생성한다.
        button = QPushButton(text)

        # 버튼의 높이를 설정한다.
        button.setFixedHeight(80)

        # 버튼 글꼴을 설정한다.
        button.setFont(QFont('Arial', 24))

        # 버튼 종류에 따라 스타일을 다르게 적용한다.
        if button_type == 'number':
            # 숫자 버튼 스타일을 설정한다.
            button.setStyleSheet(
                'QPushButton {'
                'background-color: #333333;'
                'color: white;'
                'border: none;'
                'border-radius: 40px;'
                '}'
                'QPushButton:pressed {'
                'background-color: #555555;'
                '}'
            )
        elif button_type == 'function':
            # 기능 버튼 스타일을 설정한다.
            button.setStyleSheet(
                'QPushButton {'
                'background-color: #A5A5A5;'
                'color: black;'
                'border: none;'
                'border-radius: 40px;'
                '}'
                'QPushButton:pressed {'
                'background-color: #C5C5C5;'
                '}'
            )
        else:
            # 연산자 버튼 스타일을 설정한다.
            button.setStyleSheet(
                'QPushButton {'
                'background-color: #FF9F0A;'
                'color: white;'
                'border: none;'
                'border-radius: 40px;'
                '}'
                'QPushButton:pressed {'
                'background-color: #FFB340;'
                '}'
            )

        # 버튼 클릭 시 처리할 메서드를 연결한다.
        button.clicked.connect(lambda checked, value=text: self.handle_button_click(value))

        # 완성된 버튼을 반환한다.
        return button

    # 버튼을 눌렀을 때 실행되는 메서드이다.
    def handle_button_click(self, value):
        # 숫자 또는 소수점 버튼인 경우를 처리한다.
        if value in '0123456789.':
            # 숫자 입력 처리 메서드를 호출한다.
            self.input_number(value)

        # AC 버튼인 경우를 처리한다.
        elif value == 'AC':
            # 전체 상태를 초기화한다.
            self.clear_all()

        # 부호 전환 버튼인 경우를 처리한다.
        elif value == '+/-':
            # 현재 숫자의 부호를 바꾼다.
            self.toggle_sign()

        # 퍼센트 버튼인 경우를 처리한다.
        elif value == '%':
            # 현재 숫자를 100으로 나눈다.
            self.apply_percent()

        # 사칙연산 버튼인 경우를 처리한다.
        elif value in ('+', '-', '×', '÷'):
            # 연산자 입력 처리 메서드를 호출한다.
            self.set_operator(value)

        # 등호 버튼인 경우를 처리한다.
        elif value == '=':
            # 계산 실행 메서드를 호출한다.
            self.calculate_result()

        # 화면 표시를 최신 상태로 갱신한다.
        self.update_display()

    # 숫자 또는 소수점을 입력하는 메서드이다.
    def input_number(self, value):
        # 직전에 계산이 끝난 상태에서 숫자를 누르면 새 입력을 시작한다.
        if self.just_calculated:
            # 새 숫자 입력을 위해 현재 입력값을 초기화한다.
            self.current_input = '0'

            # 계산 직후 상태를 해제한다.
            self.just_calculated = False

        # 소수점을 눌렀을 때를 처리한다.
        if value == '.':
            # 현재 입력값에 소수점이 없을 때만 추가한다.
            if '.' not in self.current_input:
                # 현재 입력값 뒤에 소수점을 붙인다.
                self.current_input += '.'
            # 이미 소수점이 있으면 아무 동작도 하지 않는다.
            return

        # 현재 입력값이 0이면 새 숫자로 교체한다.
        if self.current_input == '0':
            # 현재 입력값을 새 숫자로 바꾼다.
            self.current_input = value
        else:
            # 기존 입력값 뒤에 새 숫자를 이어 붙인다.
            self.current_input += value

    # AC 버튼 동작을 처리하는 메서드이다.
    def clear_all(self):
        # 현재 입력값을 0으로 초기화한다.
        self.current_input = '0'

        # 첫 번째 피연산자를 비운다.
        self.left_operand = None

        # 현재 연산자를 비운다.
        self.operator = None

        # 계산 직후 상태를 해제한다.
        self.just_calculated = False

    # 현재 숫자의 부호를 바꾸는 메서드이다.
    def toggle_sign(self):
        # 현재 입력값이 0이면 부호를 바꾸지 않는다.
        if self.current_input == '0':
            return

        # 음수라면 맨 앞의 '-'를 제거한다.
        if self.current_input.startswith('-'):
            # 첫 글자를 제외한 나머지를 저장한다.
            self.current_input = self.current_input[1:]
        else:
            # 양수라면 맨 앞에 '-'를 붙인다.
            self.current_input = '-' + self.current_input

    # 현재 숫자를 퍼센트 값으로 바꾸는 메서드이다.
    def apply_percent(self):
        # 현재 입력값을 숫자로 변환한다.
        value = float(self.current_input)

        # 100으로 나누어 퍼센트 값을 계산한다.
        value = value / 100

        # 계산된 값을 다시 문자열 형태로 저장한다.
        self.current_input = self.format_number_for_storage(value)

    # 연산자를 설정하는 메서드이다.
    def set_operator(self, operator):
        # 이미 연산자가 있고, 직전이 계산 완료 상태가 아닌 경우 중간 계산을 수행한다.
        if self.operator is not None and not self.just_calculated:
            # 현재까지의 계산을 먼저 수행한다.
            self.calculate_result()

        # 현재 입력값을 첫 번째 피연산자로 저장한다.
        self.left_operand = float(self.current_input)

        # 새 연산자를 저장한다.
        self.operator = operator

        # 다음 숫자 입력을 위해 현재 입력값을 0으로 초기화한다.
        self.current_input = '0'

        # 계산 직후 상태를 해제한다.
        self.just_calculated = False

    # '=' 버튼을 눌렀을 때 실제 계산을 수행하는 메서드이다.
    def calculate_result(self):
        # 첫 번째 피연산자나 연산자가 없으면 계산하지 않는다.
        if self.left_operand is None or self.operator is None:
            return

        # 현재 입력값을 두 번째 피연산자로 변환한다.
        right_operand = float(self.current_input)

        # 선택된 연산자에 따라 계산한다.
        if self.operator == '+':
            # 덧셈을 수행한다.
            result = self.left_operand + right_operand
        elif self.operator == '-':
            # 뺄셈을 수행한다.
            result = self.left_operand - right_operand
        elif self.operator == '×':
            # 곱셈을 수행한다.
            result = self.left_operand * right_operand
        elif self.operator == '÷':
            # 0으로 나누는 경우를 처리한다.
            if right_operand == 0:
                # 오류 메시지를 화면에 표시한다.
                self.current_input = 'Error'

                # 저장된 피연산자 정보를 초기화한다.
                self.left_operand = None

                # 저장된 연산자 정보를 초기화한다.
                self.operator = None

                # 계산 직후 상태를 켠다.
                self.just_calculated = True

                # 0으로 나누기 처리를 끝낸다.
                return

            # 나눗셈을 수행한다.
            result = self.left_operand / right_operand
        else:
            # 알 수 없는 연산자라면 아무 동작도 하지 않는다.
            return

        # 계산 결과를 화면 저장용 문자열로 변환한다.
        self.current_input = self.format_number_for_storage(result)

        # 다음 계산을 위해 첫 번째 피연산자를 비운다.
        self.left_operand = None

        # 다음 계산을 위해 연산자를 비운다.
        self.operator = None

        # 계산 직후 상태를 켠다.
        self.just_calculated = True

    # 내부 저장용 숫자 문자열 형태로 바꾸는 메서드이다.
    def format_number_for_storage(self, value):
        # 정수처럼 끝나는 실수라면 소수점 없이 처리한다.
        if value == int(value):
            # 정수 형태 문자열로 반환한다.
            return str(int(value))

        # 일반 실수는 불필요한 0을 제거해서 문자열로 만든다.
        text = '{0:.12f}'.format(value).rstrip('0').rstrip('.')

        # 결과 문자열을 반환한다.
        return text

    # 화면에 보여줄 형태로 숫자를 포맷하는 메서드이다.
    def format_number_for_display(self, text):
        # 오류 메시지라면 그대로 반환한다.
        if text == 'Error':
            return text

        # 음수인지 여부를 저장한다.
        is_negative = text.startswith('-')

        # 음수라면 부호를 제외한 본문 숫자만 분리한다.
        if is_negative:
            body = text[1:]
        else:
            body = text

        # 소수점이 있는 경우 정수부와 소수부를 나눈다.
        if '.' in body:
            integer_part, decimal_part = body.split('.')
        else:
            integer_part = body
            decimal_part = ''

        # 정수부가 비어 있으면 0으로 처리한다.
        if integer_part == '':
            integer_part = '0'

        # 정수부를 세 자리마다 콤마가 들어가게 변환한다.
        formatted_integer = format(int(integer_part), ',')

        # 소수부가 있으면 다시 소수점과 함께 붙인다.
        if decimal_part != '':
            formatted = formatted_integer + '.' + decimal_part
        else:
            formatted = formatted_integer

        # 원래 음수였다면 맨 앞에 다시 '-'를 붙인다.
        if is_negative:
            formatted = '-' + formatted

        # 최종 표시 문자열을 반환한다.
        return formatted

    # 현재 상태를 화면에 반영하는 메서드이다.
    def update_display(self):
        # 현재 입력값을 화면 표시용 문자열로 변환한다.
        display_text = self.format_number_for_display(self.current_input)

        # 변환된 텍스트를 표시창에 출력한다.
        self.display.setText(display_text)


# 프로그램의 시작 지점이다.
if __name__ == '__main__':
    # PyQt 애플리케이션 객체를 생성한다.
    app = QApplication(sys.argv)

    # 계산기 창 객체를 생성한다.
    calculator = Calculator()

    # 계산기 창을 화면에 표시한다.
    calculator.show()

    # 이벤트 루프를 실행하고 프로그램 종료 코드를 시스템에 반환한다.
    sys.exit(app.exec_())
