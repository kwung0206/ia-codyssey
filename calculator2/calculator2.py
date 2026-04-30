import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QGridLayout, QLabel, QPushButton, QWidget


class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current = '0'
        self.stored = None
        self.operator = None
        self.new_input = True
        self.error = False

    def input_number(self, number):
        if self.error:
            self.reset()

        if self.new_input:
            self.current = number
            self.new_input = False
        elif self.current == '0':
            self.current = number
        else:
            self.current += number

    def input_dot(self):
        if self.error:
            self.reset()

        if self.new_input:
            self.current = '0.'
            self.new_input = False
        elif '.' not in self.current:
            self.current += '.'

    def set_operator(self, operator):
        if self.operator is not None and not self.new_input:
            self.equal()

        self.stored = float(self.current)
        self.operator = operator
        self.new_input = True

    def add(self):
        self.set_operator('+')

    def subtract(self):
        self.set_operator('-')

    def multiply(self):
        self.set_operator('*')

    def divide(self):
        self.set_operator('/')

    def negative_positive(self):
        if self.current != '0':
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current

    def percent(self):
        value = float(self.current) / 100
        self.current = self.format_result(value)

    def equal(self):
        if self.operator is None:
            return

        try:
            current_value = float(self.current)

            if self.operator == '+':
                result = self.stored + current_value
            elif self.operator == '-':
                result = self.stored - current_value
            elif self.operator == '*':
                result = self.stored * current_value
            elif self.operator == '/':
                if current_value == 0:
                    raise ZeroDivisionError
                result = self.stored / current_value

            if abs(result) > 999999999999999:
                raise OverflowError

            self.current = self.format_result(result)

        except ZeroDivisionError:
            self.current = 'Error'
            self.error = True
        except OverflowError:
            self.current = 'Overflow'
            self.error = True

        self.operator = None
        self.stored = None
        self.new_input = True

    def format_result(self, value):
        value = round(value, 6)

        if value == int(value):
            return f'{int(value):,}'

        return f'{value:,}'


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('iPhone Calculator')
        self.setFixedSize(360, 560)
        self.setStyleSheet('background-color: black;')

        self.layout = QGridLayout()
        self.layout.setContentsMargins(20, 40, 20, 20)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.display = QLabel('0')
        self.display.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.display.setFont(QFont('Arial', 48))
        self.display.setStyleSheet('color: white; padding-right: 10px;')
        self.layout.addWidget(self.display, 0, 0, 1, 4)

        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row_index, row in enumerate(buttons):
            for col_index, text in enumerate(row):
                button = QPushButton(text)
                button.setFont(QFont('Arial', 24))
                button.setFixedHeight(70)

                if text == '0':
                    button.setFixedWidth(150)
                    button.setStyleSheet(self.dark_button_style(wide=True))
                    self.layout.addWidget(button, row_index + 1, 0, 1, 2)
                else:
                    button.setFixedSize(70, 70)

                    if text in ['AC', '+/-', '%']:
                        button.setStyleSheet(self.light_button_style())
                    elif text in ['÷', '×', '−', '+', '=']:
                        button.setStyleSheet(self.orange_button_style())
                    else:
                        button.setStyleSheet(self.dark_button_style())

                    if row_index == 4:
                        self.layout.addWidget(button, row_index + 1, col_index + 1)
                    else:
                        self.layout.addWidget(button, row_index + 1, col_index)

                button.clicked.connect(
                    lambda checked, value=text: self.handle_button(value)
                )

    def light_button_style(self):
        return '''
            QPushButton {
                background-color: #a5a5a5;
                color: black;
                border-radius: 35px;
                border: none;
            }
            QPushButton:pressed {
                background-color: #d9d9d9;
            }
        '''

    def dark_button_style(self, wide=False):
        radius = 35

        if wide:
            return f'''
                QPushButton {{
                    background-color: #333333;
                    color: white;
                    border-radius: {radius}px;
                    border: none;
                    text-align: left;
                    padding-left: 28px;
                }}
                QPushButton:pressed {{
                    background-color: #737373;
                }}
            '''

        return '''
            QPushButton {
                background-color: #333333;
                color: white;
                border-radius: 35px;
                border: none;
            }
            QPushButton:pressed {
                background-color: #737373;
            }
        '''

    def orange_button_style(self):
        return '''
            QPushButton {
                background-color: #ff9500;
                color: white;
                border-radius: 35px;
                border: none;
            }
            QPushButton:pressed {
                background-color: #ffc266;
            }
        '''

    def handle_button(self, value):
        if value.isdigit():
            self.calculator.input_number(value)
        elif value == '.':
            self.calculator.input_dot()
        elif value == 'AC':
            self.calculator.reset()
        elif value == '+/-':
            self.calculator.negative_positive()
        elif value == '%':
            self.calculator.percent()
        elif value == '+':
            self.calculator.add()
        elif value == '−':
            self.calculator.subtract()
        elif value == '×':
            self.calculator.multiply()
        elif value == '÷':
            self.calculator.divide()
        elif value == '=':
            self.calculator.equal()

        self.update_display()

    def update_display(self):
        text = self.calculator.current
        self.display.setText(text)

        if len(text) <= 7:
            font_size = 48
        elif len(text) <= 10:
            font_size = 40
        elif len(text) <= 13:
            font_size = 32
        else:
            font_size = 24

        self.display.setFont(QFont('Arial', font_size))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalculatorUI()
    window.show()
    sys.exit(app.exec())
