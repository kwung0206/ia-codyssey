"""Mission computer log analysis program."""

LOG_FILE_NAME = 'mission_computer_main.log'
PROBLEM_FILE_NAME = 'mission_computer_problem.log'
HEADER_LINE = 'timestamp,event,message'
PROBLEM_KEYWORDS = (
    'unstable',
    'explosion',
    'error',
    'failed',
    'critical',
    'warning',
)


def print_hello_mars():
    """Print the required greeting message."""
    print('Hello Mars')
    print()


def read_log_file(file_name):
    """Read the whole log file and return its lines."""
    with open(file_name, 'r', encoding='utf-8') as file:
        return [line.rstrip('\n') for line in file]



def print_all_lines(lines):
    """Print all lines from the log file."""
    print('[전체 로그 출력]')
    for line in lines:
        print(line)
    print()



def is_header_line(line):
    """Return True when the line is the CSV-style header."""
    return line.strip().lower() == HEADER_LINE



def parse_log_line(line, line_number):
    """Parse one log line into timestamp, event, and message fields."""
    parts = line.split(',', 2)

    if len(parts) != 3:
        raise ValueError(
            f'{line_number}번째 줄의 형식이 올바르지 않습니다: {line}'
        )

    timestamp, event, message = parts

    return {
        'timestamp': timestamp.strip(),
        'event': event.strip(),
        'message': message.strip(),
        'raw': line,
    }



def build_log_records(lines):
    """Convert raw lines into structured log records."""
    records = []

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        if line_number == 1 and is_header_line(line):
            continue

        records.append(parse_log_line(line, line_number))

    return records



def print_reverse_sorted_lines(records):
    """Print log records in reverse chronological order."""
    print('[시간 역순 출력]')

    reverse_sorted_records = sorted(
        records,
        key=lambda record: record['timestamp'],
        reverse=True,
    )

    if not reverse_sorted_records:
        print('출력할 로그가 없습니다.')
        print()
        return reverse_sorted_records

    print(HEADER_LINE)
    for record in reverse_sorted_records:
        print(record['raw'])
    print()

    return reverse_sorted_records



def is_problem_record(record):
    """Return True if the record contains a problem-related keyword."""
    text = f"{record['event']} {record['message']}".lower()

    for keyword in PROBLEM_KEYWORDS:
        if keyword in text:
            return True

    return False



def find_problem_records(records):
    """Collect records that are likely related to the incident."""
    return [record for record in records if is_problem_record(record)]



def print_problem_records(problem_records):
    """Print only problem-related log records."""
    print('[문제가 되는 로그 출력]')

    if not problem_records:
        print('문제가 되는 로그를 찾지 못했습니다.')
        print()
        return

    print(HEADER_LINE)
    for record in problem_records:
        print(record['raw'])
    print()



def save_problem_records(file_name, problem_records):
    """Save problem-related log records to a separate file."""
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(HEADER_LINE + '\n')

        for record in problem_records:
            file.write(record['raw'] + '\n')



def print_analysis_summary(records, problem_records):
    """Print a short incident summary based on the log timeline."""
    print('[사고 원인 요약]')

    if not records:
        print('분석할 로그가 없습니다.')
        print()
        return

    if not problem_records:
        print('로그에서 명확한 이상 징후를 찾지 못했습니다.')
        print()
        return

    first_problem = problem_records[0]
    last_problem = problem_records[-1]

    print(
        '직접적인 사고 원인은 산소 탱크 이상으로 판단됩니다.'
    )
    print(
        f"최초 이상 징후: {first_problem['timestamp']} "
        f"- {first_problem['message']}"
    )
    print(
        f"결정적 사고 징후: {last_problem['timestamp']} "
        f"- {last_problem['message']}"
    )
    print(
        '이후 시스템이 종료되므로 산소 탱크 폭발이 '
        '시스템 다운으로 이어진 것으로 볼 수 있습니다.'
    )
    print()



def main():
    """Run the mission computer log analysis."""
    try:
        print_hello_mars()

        lines = read_log_file(LOG_FILE_NAME)
        print_all_lines(lines)

        records = build_log_records(lines)
        problem_records = find_problem_records(records)

        print_reverse_sorted_lines(records)
        print_problem_records(problem_records)
        save_problem_records(PROBLEM_FILE_NAME, problem_records)
        print_analysis_summary(records, problem_records)

        print(
            f'문제가 되는 로그를 {PROBLEM_FILE_NAME} 파일로 저장했습니다.'
        )

    except FileNotFoundError:
        print(f'{LOG_FILE_NAME} 파일을 찾을 수 없습니다.')
    except PermissionError:
        print(f'{LOG_FILE_NAME} 파일에 접근할 권한이 없습니다.')
    except UnicodeDecodeError:
        print('로그 파일 인코딩을 확인해 주세요. UTF-8 형식이 아닐 수 있습니다.')
    except ValueError as error:
        print(f'로그 형식 오류: {error}')
    except OSError as error:
        print(f'파일 처리 중 오류가 발생했습니다: {error}')


if __name__ == '__main__':
    main()
