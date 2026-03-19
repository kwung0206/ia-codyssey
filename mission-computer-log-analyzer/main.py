# "Mission computer log analysis program." 이 파일이 '미션 컴퓨터 로그 분석 프로그램'임을 설명하는 모듈 설명 문자열입니다.

LOG_FILE_NAME = 'mission_computer_main.log'  # 원본 로그 파일 이름을 상수로 저장합니다.
PROBLEM_FILE_NAME = 'mission_computer_problem.log'  # 문제가 있는 로그만 따로 저장할 파일 이름입니다.
HEADER_LINE = 'timestamp,event,message'  # CSV 형식 헤더 문자열입니다.
PROBLEM_KEYWORDS = (  # 문제 상황으로 판단할 키워드 목록입니다.
    'unstable',  # 불안정 관련 키워드입니다.
    'explosion',  # 폭발 관련 키워드입니다.
    'error',  # 오류 관련 키워드입니다.
    'failed',  # 실패 관련 키워드입니다.
    'critical',  # 치명적 문제 관련 키워드입니다.
    'warning',  # 경고 관련 키워드입니다.
)  # 튜플 종료입니다.


def print_hello_mars():  # 인사 문구를 출력하는 함수를 정의합니다.
    print('Hello Mars')  # 화면에 Hello Mars를 출력합니다.
    print()  # 줄바꿈을 한 번 더 출력해서 보기 좋게 만듭니다.


def read_log_file(file_name):  # 로그 파일을 읽는 함수를 정의합니다.
    with open(file_name, 'r', encoding='utf-8') as file:  # UTF-8 인코딩으로 파일을 읽기 모드로 엽니다.
        return [line.rstrip('\n') for line in file]  # 각 줄 끝의 개행문자를 제거한 뒤 리스트로 반환합니다.


def print_all_lines(lines):  # 전체 로그를 출력하는 함수를 정의합니다.
    print('[전체 로그 출력]')  # 구분용 제목을 출력합니다.
    for line in lines:  # lines 리스트에 들어 있는 각 줄을 하나씩 꺼냅니다.
        print(line)  # 해당 줄을 출력합니다.
    print()  # 출력 후 한 줄 띄웁니다.


def is_header_line(line):  # 현재 줄이 헤더인지 검사하는 함수를 정의합니다.
    return line.strip().lower() == HEADER_LINE  # 공백 제거 후 소문자로 바꾸고 HEADER_LINE과 같은지 비교합니다.


def parse_log_line(line, line_number):  # 한 줄의 로그를 파싱하는 함수를 정의합니다.
    parts = line.split(',', 2)  # 쉼표 기준으로 최대 3개 부분(timestamp, event, message)으로 나눕니다.

    if len(parts) != 3:  # 나눈 결과가 정확히 3개가 아니면 형식 오류입니다.
        raise ValueError(  # ValueError 예외를 발생시킵니다.
            f'{line_number}번째 줄의 형식이 올바르지 않습니다: {line}'  # 몇 번째 줄이 잘못됐는지 포함한 메시지입니다.
        )  # 예외 메시지 종료입니다.

    timestamp, event, message = parts  # 나눈 결과를 각각 timestamp, event, message 변수에 저장합니다.

    return {  # 파싱한 결과를 딕셔너리 형태로 반환합니다.
        'timestamp': timestamp.strip(),  # timestamp 앞뒤 공백을 제거해서 저장합니다.
        'event': event.strip(),  # event 앞뒤 공백을 제거해서 저장합니다.
        'message': message.strip(),  # message 앞뒤 공백을 제거해서 저장합니다.
        'raw': line,  # 원본 줄 전체도 함께 저장합니다.
    }  # 딕셔너리 반환 종료입니다.


def build_log_records(lines):  # 원본 문자열 리스트를 구조화된 로그 레코드로 바꾸는 함수를 정의합니다.
    records = []  # 결과를 저장할 빈 리스트를 생성합니다.

    for line_number, line in enumerate(lines, start=1):  # 줄 번호를 1부터 매기면서 각 줄을 순회합니다.
        if not line.strip():  # 현재 줄이 공백 줄이면
            continue  # 해당 줄은 건너뜁니다.

        if line_number == 1 and is_header_line(line):  # 첫 줄이면서 헤더라면
            continue  # 데이터가 아니므로 건너뜁니다.

        records.append(parse_log_line(line, line_number))  # 해당 줄을 파싱한 뒤 records 리스트에 추가합니다.

    return records  # 완성된 레코드 리스트를 반환합니다.


def print_reverse_sorted_lines(records):  # 로그를 시간 역순으로 출력하는 함수를 정의합니다.
    print('[시간 역순 출력]')  # 구분용 제목을 출력합니다.

    reverse_sorted_records = sorted(  # 정렬된 새 리스트를 reverse_sorted_records에 저장합니다.
        records,  # 정렬 대상은 records 리스트입니다.
        key=lambda record: record['timestamp'],  # 각 레코드의 timestamp 값을 기준으로 정렬합니다.
        reverse=True,  # 내림차순(최신순)으로 정렬합니다.
    )  # sorted 종료입니다.

    if not reverse_sorted_records:  # 정렬 결과가 비어 있다면
        print('출력할 로그가 없습니다.')  # 출력할 로그가 없다고 알립니다.
        print()  # 한 줄 띄웁니다.
        return reverse_sorted_records  # 빈 리스트를 그대로 반환합니다.

    print(HEADER_LINE)  # 헤더를 먼저 출력합니다.
    for record in reverse_sorted_records:  # 정렬된 각 레코드를 하나씩 꺼냅니다.
        print(record['raw'])  # 원본 로그 문자열을 그대로 출력합니다.
    print()  # 출력 후 한 줄 띄웁니다.

    return reverse_sorted_records  # 정렬된 레코드 리스트를 반환합니다.


def is_problem_record(record):  # 특정 로그가 문제 로그인지 판별하는 함수를 정의합니다.
    text = f"{record['event']} {record['message']}".lower()  # event와 message를 합치고 소문자로 변환합니다.

    for keyword in PROBLEM_KEYWORDS:  # 문제 키워드 목록을 하나씩 확인합니다.
        if keyword in text:  # 현재 키워드가 event/message에 포함되어 있다면
            return True  # 문제 로그라고 판단하고 True를 반환합니다.

    return False  # 어떤 키워드도 없으면 문제 로그가 아니므로 False를 반환합니다.


def find_problem_records(records):  # 문제 로그만 모으는 함수를 정의합니다.
    """Collect records that are likely related to the incident."""  # 함수 설명입니다.
    return [record for record in records if is_problem_record(record)]  # 문제 로그인 레코드만 새 리스트로 반환합니다.


def print_problem_records(problem_records):  # 문제 로그만 출력하는 함수를 정의합니다.
    print('[문제가 되는 로그 출력]')  # 구분용 제목을 출력합니다.

    if not problem_records:  # 문제 로그가 하나도 없다면
        print('문제가 되는 로그를 찾지 못했습니다.')  # 찾지 못했다고 출력합니다.
        print()  # 한 줄 띄웁니다.
        return  # 함수 실행을 종료합니다.

    print(HEADER_LINE)  # 헤더를 출력합니다.
    for record in problem_records:  # 문제 로그 목록을 순회합니다.
        print(record['raw'])  # 원본 로그 문자열을 그대로 출력합니다.
    print()  # 출력 후 한 줄 띄웁니다.


def save_problem_records(file_name, problem_records):  # 문제 로그를 파일로 저장하는 함수를 정의합니다.
    with open(file_name, 'w', encoding='utf-8') as file:  # 저장할 파일을 UTF-8 쓰기 모드로 엽니다.
        file.write(HEADER_LINE + '\n')  # 첫 줄에 헤더를 기록합니다.

        for record in problem_records:  # 문제 로그를 하나씩 순회합니다.
            file.write(record['raw'] + '\n')  # 원본 로그 한 줄씩 파일에 저장합니다.


def print_analysis_summary(records, problem_records):  # 로그 분석 요약을 출력하는 함수를 정의합니다.
    print('[사고 원인 요약]')  # 요약 제목을 출력합니다.

    if not records:  # 전체 로그 자체가 없다면
        print('분석할 로그가 없습니다.')  # 분석할 로그가 없다고 출력합니다.
        print()  # 한 줄 띄웁니다.
        return  # 함수 실행을 종료합니다.

    if not problem_records:  # 문제 로그가 없다면
        print('로그에서 명확한 이상 징후를 찾지 못했습니다.')  # 이상 징후가 없다고 출력합니다.
        print()  # 한 줄 띄웁니다.
        return  # 함수 실행을 종료합니다.

    first_problem = problem_records[0]  # 문제 로그 중 첫 번째 항목을 최초 이상 징후로 사용합니다.
    last_problem = problem_records[-1]  # 문제 로그 중 마지막 항목을 결정적 징후로 사용합니다.

    print(  # 첫 번째 요약 문장을 출력합니다.
        '직접적인 사고 원인은 산소 탱크 이상으로 판단됩니다.'  # 사고 원인 추정 문장입니다.
    )  # print 종료입니다.
    print(  # 최초 이상 징후 문장을 출력합니다.
        f"최초 이상 징후: {first_problem['timestamp']} "  # 최초 이상 발생 시각을 출력합니다.
        f"- {first_problem['message']}"  # 해당 시점의 메시지를 출력합니다.
    )  # print 종료입니다.
    print(  # 결정적 사고 징후 문장을 출력합니다.
        f"결정적 사고 징후: {last_problem['timestamp']} "  # 결정적 이상 발생 시각을 출력합니다.
        f"- {last_problem['message']}"  # 해당 시점의 메시지를 출력합니다.
    )  # print 종료입니다.
    print(  # 마지막 요약 문장을 출력합니다.
        '이후 시스템이 종료되므로 산소 탱크 폭발이 '  # 앞부분 문자열입니다.
        '시스템 다운으로 이어진 것으로 볼 수 있습니다.'  # 뒷부분 문자열입니다.
    )  # print 종료입니다.
    print()  # 마지막에 한 줄 띄웁니다.


def main():  # 프로그램 전체 실행 흐름을 담당하는 main 함수를 정의합니다.
    """Run the mission computer log analysis."""  # 함수 설명입니다.
    try:  # 예외 처리를 시작합니다.
        print_hello_mars()  # 인사 문구를 출력합니다.

        lines = read_log_file(LOG_FILE_NAME)  # 로그 파일 전체를 읽어서 lines에 저장합니다.
        print_all_lines(lines)  # 원본 로그 전체를 출력합니다.

        records = build_log_records(lines)  # 원본 줄을 구조화된 레코드 리스트로 변환합니다.
        problem_records = find_problem_records(records)  # 문제 로그만 추출합니다.

        print_reverse_sorted_lines(records)  # 전체 로그를 시간 역순으로 출력합니다.
        print_problem_records(problem_records)  # 문제 로그만 출력합니다.
        save_problem_records(PROBLEM_FILE_NAME, problem_records)  # 문제 로그를 별도 파일로 저장합니다.
        print_analysis_summary(records, problem_records)  # 분석 요약을 출력합니다.

        print(  # 마지막 안내 문장을 출력합니다.
            f'문제가 되는 로그를 {PROBLEM_FILE_NAME} 파일로 저장했습니다.'  # 저장 완료 메시지입니다.
        )  # print 종료입니다.

    except FileNotFoundError:  # 파일이 없을 때 처리합니다.
        print(f'{LOG_FILE_NAME} 파일을 찾을 수 없습니다.')  # 파일이 없다는 메시지를 출력합니다.
    except PermissionError:  # 파일 접근 권한이 없을 때 처리합니다.
        print(f'{LOG_FILE_NAME} 파일에 접근할 권한이 없습니다.')  # 권한 오류 메시지를 출력합니다.
    except UnicodeDecodeError:  # UTF-8로 읽을 수 없는 인코딩 문제일 때 처리합니다.
        print('로그 파일 인코딩을 확인해 주세요. UTF-8 형식이 아닐 수 있습니다.')  # 인코딩 오류 메시지를 출력합니다.
    except ValueError as error:  # 로그 형식이 잘못되었을 때 처리합니다.
        print(f'로그 형식 오류: {error}')  # 형식 오류 내용을 출력합니다.
    except OSError as error:  # 그 외 파일 처리 관련 OS 오류를 처리합니다.
        print(f'파일 처리 중 오류가 발생했습니다: {error}')  # 일반 파일 처리 오류 메시지를 출력합니다.


if __name__ == '__main__':  # 현재 파일을 직접 실행했을 때만 아래 코드를 실행합니다.
    main()  # main 함수를 호출하여 프로그램을 시작합니다.
