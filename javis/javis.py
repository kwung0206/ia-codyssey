# 음성을 녹음하기 위해 허용된 외부 라이브러리 sounddevice를 가져온다.
import sounddevice as sd

# wav 파일을 저장하기 위해 파이썬 기본 라이브러리 wave를 가져온다.
import wave

# 폴더 생성과 파일 목록 확인을 위해 파이썬 기본 라이브러리 os를 가져온다.
import os

# 날짜와 시간을 사용하기 위해 파이썬 기본 라이브러리 datetime을 가져온다.
from datetime import datetime


# 녹음 파일을 저장할 폴더 이름을 상수로 정의한다.
RECORD_DIR = 'records'

# 녹음 샘플링 주파수를 상수로 정의한다.
SAMPLE_RATE = 44100

# 녹음 채널 수를 상수로 정의한다.
CHANNELS = 1

# 녹음 데이터의 바이트 크기를 상수로 정의한다.
SAMPLE_WIDTH = 2


# records 폴더가 없으면 생성하는 함수이다.
def create_records_folder():
    # records 폴더가 존재하지 않는지 확인한다.
    if not os.path.exists(RECORD_DIR):
        # records 폴더를 생성한다.
        os.makedirs(RECORD_DIR)


# 현재 날짜와 시간을 기반으로 파일 이름을 만드는 함수이다.
def make_record_file_name():
    # 현재 날짜와 시간을 가져온다.
    now = datetime.now()

    # 년월일-시간분초 형식의 문자열을 만든다.
    file_name = now.strftime('%Y%m%d-%H%M%S')

    # 파일 이름 뒤에 wav 확장자를 붙인다.
    file_name = file_name + '.wav'

    # records 폴더 경로와 파일 이름을 합쳐 전체 경로를 만든다.
    file_path = os.path.join(RECORD_DIR, file_name)

    # 완성된 파일 경로를 반환한다.
    return file_path


# 시스템에서 사용할 수 있는 마이크 목록을 출력하는 함수이다.
def show_microphones():
    # 시스템에 연결된 오디오 장치 목록을 가져온다.
    devices = sd.query_devices()

    # 마이크 목록 제목을 출력한다.
    print('\n[마이크 목록]')

    # 장치 번호를 0부터 하나씩 증가시키며 장치 정보를 확인한다.
    for index, device in enumerate(devices):
        # 입력 채널 수가 1개 이상이면 마이크로 사용할 수 있다.
        if device['max_input_channels'] > 0:
            # 장치 번호와 장치 이름을 출력한다.
            print(str(index) + '번 - ' + device['name'])


# 사용자에게 마이크 번호를 입력받는 함수이다.
def select_microphone():
    # 마이크 목록을 출력한다.
    show_microphones()

    # 사용자에게 마이크 번호 입력을 요청한다.
    device_number = input('\n사용할 마이크 번호를 입력하세요: ')

    # 입력값이 숫자인지 확인한다.
    if not device_number.isdigit():
        # 숫자가 아니면 안내 메시지를 출력한다.
        print('숫자만 입력해야 합니다.')

        # 선택 실패를 의미하는 None을 반환한다.
        return None

    # 입력받은 문자열을 정수로 변환한다.
    device_number = int(device_number)

    # 선택한 마이크 번호를 반환한다.
    return device_number


# 실제 음성을 녹음하는 함수이다.
def record_audio():
    # records 폴더가 없으면 생성한다.
    create_records_folder()

    # 사용할 마이크 번호를 입력받는다.
    device_number = select_microphone()

    # 마이크 번호가 올바르지 않으면 함수를 종료한다.
    if device_number is None:
        # 함수 실행을 종료한다.
        return

    # 녹음 시간을 입력받는다.
    record_seconds = input('녹음 시간을 초 단위로 입력하세요: ')

    # 입력값이 숫자인지 확인한다.
    if not record_seconds.isdigit():
        # 숫자가 아니면 안내 메시지를 출력한다.
        print('녹음 시간은 숫자로 입력해야 합니다.')

        # 함수 실행을 종료한다.
        return

    # 입력받은 녹음 시간을 정수로 변환한다.
    record_seconds = int(record_seconds)

    # 녹음 시간이 0 이하인지 확인한다.
    if record_seconds <= 0:
        # 잘못된 녹음 시간 안내 메시지를 출력한다.
        print('녹음 시간은 1초 이상이어야 합니다.')

        # 함수 실행을 종료한다.
        return

    # 저장할 녹음 파일 경로를 만든다.
    file_path = make_record_file_name()

    # 녹음 시작 안내 메시지를 출력한다.
    print('\n녹음을 시작합니다.')

    # 지정한 시간만큼 마이크 입력을 녹음한다.
    audio_data = sd.rec(
        int(record_seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype='int16',
        device=device_number
    )

    # 녹음이 끝날 때까지 기다린다.
    sd.wait()

    # 녹음 종료 안내 메시지를 출력한다.
    print('녹음이 종료되었습니다.')

    # wav 파일을 쓰기 모드로 연다.
    with wave.open(file_path, 'wb') as wave_file:
        # 녹음 채널 수를 설정한다.
        wave_file.setnchannels(CHANNELS)

        # 샘플 하나의 바이트 크기를 설정한다.
        wave_file.setsampwidth(SAMPLE_WIDTH)

        # 샘플링 주파수를 설정한다.
        wave_file.setframerate(SAMPLE_RATE)

        # 녹음한 음성 데이터를 wav 파일에 저장한다.
        wave_file.writeframes(audio_data.tobytes())

    # 저장 완료 메시지를 출력한다.
    print('저장 완료:', file_path)


# 문자열 날짜를 datetime 객체로 변환하는 함수이다.
def parse_date(date_text):
    # 입력받은 날짜 문자열을 YYYYMMDD 형식으로 해석한다.
    return datetime.strptime(date_text, '%Y%m%d')


# 보너스 과제: 특정 날짜 범위의 녹음 파일을 보여주는 함수이다.
def show_records_by_date():
    # records 폴더가 없으면 생성한다.
    create_records_folder()

    # 시작 날짜를 입력받는다.
    start_text = input('시작 날짜를 입력하세요. 예: 20260520: ')

    # 종료 날짜를 입력받는다.
    end_text = input('종료 날짜를 입력하세요. 예: 20260521: ')

    # 날짜 형식 오류를 처리하기 위해 try 문을 사용한다.
    try:
        # 시작 날짜 문자열을 datetime 객체로 변환한다.
        start_date = parse_date(start_text)

        # 종료 날짜 문자열을 datetime 객체로 변환한다.
        end_date = parse_date(end_text)

    # 날짜 변환 중 오류가 발생하면 실행된다.
    except ValueError:
        # 날짜 형식 오류 안내 메시지를 출력한다.
        print('날짜는 YYYYMMDD 형식으로 입력해야 합니다.')

        # 함수 실행을 종료한다.
        return

    # 시작 날짜가 종료 날짜보다 늦은지 확인한다.
    if start_date > end_date:
        # 잘못된 날짜 범위 안내 메시지를 출력한다.
        print('시작 날짜는 종료 날짜보다 늦을 수 없습니다.')

        # 함수 실행을 종료한다.
        return

    # 조회된 파일이 있는지 확인하기 위한 변수를 만든다.
    found = False

    # 녹음 파일 목록 제목을 출력한다.
    print('\n[조회된 녹음 파일]')

    # records 폴더 안의 파일 목록을 하나씩 확인한다.
    for file_name in os.listdir(RECORD_DIR):
        # wav 파일이 아니면 건너뛴다.
        if not file_name.endswith('.wav'):
            # 다음 파일로 넘어간다.
            continue

        # 파일 이름에서 날짜 부분만 가져온다.
        file_date_text = file_name[:8]

        # 파일 이름의 날짜 부분을 datetime 객체로 변환한다.
        file_date = parse_date(file_date_text)

        # 파일 날짜가 시작 날짜와 종료 날짜 사이에 있는지 확인한다.
        if start_date <= file_date <= end_date:
            # 파일을 찾았다는 의미로 True를 저장한다.
            found = True

            # 파일 이름을 출력한다.
            print(file_name)

    # 조회된 파일이 없는지 확인한다.
    if not found:
        # 파일 없음 안내 메시지를 출력한다.
        print('해당 날짜 범위에 녹음 파일이 없습니다.')


# 메뉴를 출력하는 함수이다.
def show_menu():
    # 메뉴 제목을 출력한다.
    print('\n[JAVIS 음성 녹음 프로그램]')

    # 1번 메뉴를 출력한다.
    print('1. 마이크 목록 보기')

    # 2번 메뉴를 출력한다.
    print('2. 음성 녹음하기')

    # 3번 메뉴를 출력한다.
    print('3. 날짜 범위로 녹음 파일 조회하기')

    # 4번 메뉴를 출력한다.
    print('4. 종료하기')


# 프로그램의 시작 지점이 되는 main 함수이다.
def main():
    # records 폴더가 없으면 생성한다.
    create_records_folder()

    # 사용자가 종료하기 전까지 반복한다.
    while True:
        # 메뉴를 출력한다.
        show_menu()

        # 사용자에게 메뉴 번호를 입력받는다.
        menu = input('메뉴를 선택하세요: ')

        # 사용자가 1번을 선택했는지 확인한다.
        if menu == '1':
            # 마이크 목록을 출력한다.
            show_microphones()

        # 사용자가 2번을 선택했는지 확인한다.
        elif menu == '2':
            # 음성 녹음을 실행한다.
            record_audio()

        # 사용자가 3번을 선택했는지 확인한다.
        elif menu == '3':
            # 날짜 범위 녹음 파일 조회 기능을 실행한다.
            show_records_by_date()

        # 사용자가 4번을 선택했는지 확인한다.
        elif menu == '4':
            # 종료 안내 메시지를 출력한다.
            print('프로그램을 종료합니다.')

            # 반복문을 종료한다.
            break

        # 1, 2, 3, 4가 아닌 값을 입력한 경우이다.
        else:
            # 잘못된 메뉴 선택 안내 메시지를 출력한다.
            print('올바른 메뉴 번호를 입력하세요.')


# 이 파일이 직접 실행될 때만 main 함수를 실행한다.
if __name__ == '__main__':
    # main 함수를 호출한다.
    main()
