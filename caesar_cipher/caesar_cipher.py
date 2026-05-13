# caesar_cipher_decode 함수 정의
# target_text는 해독해야 할 암호문 문자열이다.
def caesar_cipher_decode(target_text):
    # 영어 알파벳은 총 26개이므로 26번 반복한다.
    alphabet_count = 26

    # shift 값을 0부터 25까지 하나씩 바꾸면서 반복한다.
    for shift in range(alphabet_count):
        # 현재 shift 값으로 해독한 결과를 저장할 빈 문자열이다.
        decoded_text = ''

        # 암호문에서 문자 하나씩 꺼내서 반복한다.
        for char in target_text:
            # 현재 문자가 소문자 a부터 z 사이인지 확인한다.
            if 'a' <= char <= 'z':
                # 소문자를 shift만큼 뒤로 밀어서 해독한 뒤 decoded_text에 추가한다.
                decoded_text += chr((ord(char) - ord('a') - shift) % alphabet_count + ord('a'))

            # 현재 문자가 대문자 A부터 Z 사이인지 확인한다.
            elif 'A' <= char <= 'Z':
                # 대문자를 shift만큼 뒤로 밀어서 해독한 뒤 decoded_text에 추가한다.
                decoded_text += chr((ord(char) - ord('A') - shift) % alphabet_count + ord('A'))

            # 알파벳이 아닌 문자라면 공백, 숫자, 특수문자 등을 그대로 둔다.
            else:
                # 알파벳이 아닌 문자는 변경하지 않고 decoded_text에 추가한다.
                decoded_text += char

        # 현재 몇 번 자리수로 해독했는지 출력한다.
        print('[' + str(shift) + '번 자리수]')

        # 현재 shift 값으로 해독한 결과를 출력한다.
        print(decoded_text)

        # 결과를 보기 좋게 구분하기 위해 빈 줄을 출력한다.
        print()


# 사전 단어를 이용해서 자동으로 해독 결과를 찾는 함수 정의
# target_text는 해독해야 할 암호문 문자열이다.
def caesar_cipher_decode_with_dictionary(target_text):
    # 해독 결과에 포함되어 있을 가능성이 있는 단어 목록이다.
    dictionary = [
        'mars',
        'base',
        'door',
        'password',
        'emergency',
        'storage',
        'key',
        'open',
        'security',
        'caesar'
    ]

    # 영어 알파벳은 총 26개이므로 26번 반복한다.
    alphabet_count = 26

    # shift 값을 0부터 25까지 하나씩 바꾸면서 반복한다.
    for shift in range(alphabet_count):
        # 현재 shift 값으로 해독한 결과를 저장할 빈 문자열이다.
        decoded_text = ''

        # 암호문에서 문자 하나씩 꺼내서 반복한다.
        for char in target_text:
            # 현재 문자가 소문자 a부터 z 사이인지 확인한다.
            if 'a' <= char <= 'z':
                # 소문자를 shift만큼 뒤로 밀어서 해독한 뒤 decoded_text에 추가한다.
                decoded_text += chr((ord(char) - ord('a') - shift) % alphabet_count + ord('a'))

            # 현재 문자가 대문자 A부터 Z 사이인지 확인한다.
            elif 'A' <= char <= 'Z':
                # 대문자를 shift만큼 뒤로 밀어서 해독한 뒤 decoded_text에 추가한다.
                decoded_text += chr((ord(char) - ord('A') - shift) % alphabet_count + ord('A'))

            # 알파벳이 아닌 문자라면 그대로 둔다.
            else:
                # 공백, 숫자, 특수문자는 변경하지 않고 추가한다.
                decoded_text += char

        # 현재 몇 번 자리수로 해독했는지 출력한다.
        print('[' + str(shift) + '번 자리수]')

        # 현재 shift 값으로 해독한 결과를 출력한다.
        print(decoded_text)

        # 결과를 보기 좋게 구분하기 위해 빈 줄을 출력한다.
        print()

        # 대소문자 구분 없이 사전 단어를 찾기 위해 해독 결과를 소문자로 바꾼다.
        lower_text = decoded_text.lower()

        # 사전에 들어 있는 단어를 하나씩 꺼내서 확인한다.
        for word in dictionary:
            # 사전 단어가 해독 결과 안에 포함되어 있는지 확인한다.
            if word in lower_text:
                # 어떤 단어가 발견되었는지 출력한다.
                print('사전 단어 "' + word + '" 발견')

                # 발견된 shift 값과 해독 결과를 반환한다.
                return shift, decoded_text

    # 모든 shift 값을 확인했는데도 사전 단어를 찾지 못한 경우 None을 반환한다.
    return None, None


# 최종 해독 결과를 result.txt 파일에 저장하는 함수 정의
# result_text는 파일에 저장할 최종 해독 문자열이다.
def save_result(result_text):
    # 파일 저장 중 오류가 날 수 있으므로 예외처리를 한다.
    try:
        # result.txt 파일을 쓰기 모드로 연다.
        file = open('result.txt', 'w', encoding='utf-8')

        # result.txt 파일에 최종 해독 결과를 쓴다.
        file.write(result_text)

        # 파일 사용이 끝났으므로 파일을 닫는다.
        file.close()

        # 저장 완료 메시지를 출력한다.
        print('result.txt 파일로 저장되었습니다.')

    # 파일 저장 중 운영체제 관련 오류가 발생했을 때 실행된다.
    except OSError:
        # 파일 저장 오류 메시지를 출력한다.
        print('result.txt 파일 저장 중 오류가 발생했습니다.')


# 프로그램의 전체 실행 흐름을 담당하는 main 함수 정의
def main():
    # password.txt 파일을 읽는 과정에서 오류가 날 수 있으므로 예외처리를 한다.
    try:
        # password.txt 파일을 읽기 모드로 연다.
        file = open('password.txt', 'r', encoding='utf-8')

        # password.txt 파일 안의 전체 내용을 읽어서 target_text에 저장한다.
        target_text = file.read()

        # 파일 사용이 끝났으므로 파일을 닫는다.
        file.close()

    # password.txt 파일이 존재하지 않을 때 실행된다.
    except FileNotFoundError:
        # 파일이 없다는 오류 메시지를 출력한다.
        print('password.txt 파일을 찾을 수 없습니다.')

        # 더 이상 진행할 수 없으므로 main 함수를 종료한다.
        return

    # 파일 읽기 중 운영체제 관련 오류가 발생했을 때 실행된다.
    except OSError:
        # 파일 읽기 오류 메시지를 출력한다.
        print('password.txt 파일을 읽는 중 오류가 발생했습니다.')

        # 더 이상 진행할 수 없으므로 main 함수를 종료한다.
        return

    # 프로그램 제목을 출력한다.
    print('카이사르 암호 해독 결과')

    # 보기 좋게 빈 줄을 출력한다.
    print()

    # 0번부터 25번까지 모든 자리수의 해독 결과를 출력한다.
    caesar_cipher_decode(target_text)

    # 사용자에게 올바르게 해독된 자리수 번호를 입력받는다.
    choice = input('해독된 자리수 번호를 입력하세요: ')

    # 입력값이 숫자로만 이루어져 있는지 확인한다.
    if not choice.isdigit():
        # 숫자가 아닌 값이 입력되었을 때 오류 메시지를 출력한다.
        print('숫자만 입력해야 합니다.')

        # 잘못된 입력이므로 main 함수를 종료한다.
        return

    # 입력받은 문자열 숫자를 정수로 변환한다.
    shift = int(choice)

    # shift 값이 0보다 작거나 25보다 큰지 확인한다.
    if shift < 0 or shift > 25:
        # 허용 범위를 벗어난 경우 오류 메시지를 출력한다.
        print('자리수는 0부터 25까지만 입력할 수 있습니다.')

        # 잘못된 입력이므로 main 함수를 종료한다.
        return

    # 사용자가 선택한 shift 값으로 다시 해독한 결과를 저장할 빈 문자열이다.
    decoded_text = ''

    # 암호문에서 문자 하나씩 꺼내서 반복한다.
    for char in target_text:
        # 현재 문자가 소문자 a부터 z 사이인지 확인한다.
        if 'a' <= char <= 'z':
            # 소문자를 사용자가 입력한 shift만큼 뒤로 밀어서 해독한다.
            decoded_text += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))

        # 현재 문자가 대문자 A부터 Z 사이인지 확인한다.
        elif 'A' <= char <= 'Z':
            # 대문자를 사용자가 입력한 shift만큼 뒤로 밀어서 해독한다.
            decoded_text += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))

        # 알파벳이 아닌 문자라면 그대로 둔다.
        else:
            # 공백, 숫자, 특수문자는 변경하지 않고 추가한다.
            decoded_text += char

    # 최종 해독 결과를 result.txt 파일에 저장한다.
    save_result(decoded_text)


# main 함수를 실행하여 프로그램을 시작한다.
main()