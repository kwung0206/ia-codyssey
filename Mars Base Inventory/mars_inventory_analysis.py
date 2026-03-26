# 입력으로 사용할 원본 CSV 파일 이름
INPUT_FILE = 'Mars_Base_Inventory_List.csv'

# 위험 물질만 따로 저장할 CSV 파일 이름
DANGER_FILE = 'Mars_Base_Inventory_danger.csv'

# 정렬된 전체 목록을 바이너리 형식처럼 저장할 파일 이름
BINARY_FILE = 'Mars_Base_Inventory_List.bin'

# 인화성 위험 물질로 판단할 기준값
DANGER_THRESHOLD = 0.7


def read_text_file(file_name):
    # 텍스트 파일을 한 줄씩 읽어서 리스트로 반환하는 함수
    try:
        # 읽기 모드('r'), UTF-8 인코딩으로 파일 열기
        with open(file_name, 'r', encoding='utf-8') as file:
            # 각 줄 끝의 줄바꿈 문자('\n')를 제거한 뒤 리스트로 반환
            return [line.rstrip('\n') for line in file]

    # 파일이 존재하지 않을 때 실행
    except FileNotFoundError:
        print(f'[오류] 파일을 찾을 수 없습니다: {file_name}')

    # 파일 접근 권한이 없을 때 실행
    except PermissionError:
        print(f'[오류] 파일 접근 권한이 없습니다: {file_name}')

    # 그 외 운영체제 관련 파일 입출력 오류 처리
    except OSError as error:
        print(f'[오류] 파일 읽기 중 문제가 발생했습니다: {error}')

    # 오류가 발생하면 빈 리스트 반환
    return []


def print_file_content(lines):
    # CSV 원본 내용을 그대로 출력하는 함수
    print('[1] CSV 원본 내용 출력')

    # lines 리스트에 들어 있는 각 줄을 하나씩 출력
    for line in lines:
        print(line)

    # 출력 구분용 빈 줄
    print()


def convert_to_inventory_list(lines):
    # CSV 문자열 목록을 딕셔너리 리스트 형태로 변환하는 함수
    inventory_list = []

    # 입력 데이터가 비어 있으면 빈 리스트 그대로 반환
    if not lines:
        return inventory_list

    # 첫 번째 줄(헤더)을 쉼표 기준으로 나누고 공백 제거
    # 현재 코드에서는 header를 실제로 쓰진 않지만
    # CSV의 첫 줄이 헤더라는 점을 확인하는 의미로 저장
    header = [item.strip() for item in lines[0].split(',')]

    # 두 번째 줄부터 마지막 줄까지 반복
    # start=2는 실제 CSV 파일의 줄 번호처럼 보이게 하려는 목적
    for index, line in enumerate(lines[1:], start=2):

        # 빈 줄이면 건너뜀
        if not line.strip():
            continue

        # 한 줄을 쉼표 기준으로 분리하고 각 항목 공백 제거
        parts = [item.strip() for item in line.split(',')]

        # 데이터가 정확히 5개 항목이 아니면 잘못된 형식으로 판단
        if len(parts) != 5:
            print(f'[경고] {index}번째 줄 형식이 올바르지 않아 건너뜁니다: {line}')
            continue

        try:
            # 다섯 번째 항목(인화성 지수)을 실수(float)로 변환
            flammability = float(parts[4])

        # 숫자로 바꿀 수 없으면 경고 출력 후 건너뜀
        except ValueError:
            print(f'[경고] {index}번째 줄의 인화성 지수 변환에 실패했습니다: {line}')
            continue

        # 한 줄의 데이터를 딕셔너리 형태로 저장
        item = {
            'Substance': parts[0],              # 물질명
            'Weight (g/cm³)': parts[1],         # 밀도
            'Specific Gravity': parts[2],       # 비중
            'Strength': parts[3],               # 강도
            'Flammability': flammability,       # 인화성 지수(실수형)
        }

        # 완성된 딕셔너리를 리스트에 추가
        inventory_list.append(item)

    # 변환 완료 메시지 출력
    print('[2] CSV 내용을 리스트 객체로 변환 완료')

    # 변환된 전체 리스트 출력
    print(inventory_list)

    # 출력 구분용 빈 줄
    print()

    # 완성된 리스트 반환
    return inventory_list


def print_inventory_list(title, inventory_list):
    # 리스트 내용을 보기 좋게 출력하는 함수
    print(title)

    # 리스트가 비어 있으면 안내 문구 출력 후 종료
    if not inventory_list:
        print('데이터가 없습니다.')
        print()
        return

    # 리스트 안의 각 딕셔너리를 한 줄씩 출력
    for item in inventory_list:
        print(
            f"물질명: {item['Substance']}, "
            f"밀도: {item['Weight (g/cm³)']}, "
            f"비중: {item['Specific Gravity']}, "
            f"강도: {item['Strength']}, "
            f"인화성: {item['Flammability']}"
        )

    # 출력 구분용 빈 줄
    print()


def sort_by_flammability(inventory_list):
    # 인화성 지수를 기준으로 내림차순 정렬하는 함수
    return sorted(
        inventory_list,                        # 정렬할 대상 리스트
        key=lambda item: item['Flammability'], # 각 항목의 인화성 값을 기준으로 삼음
        reverse=True                           # 내림차순(큰 값부터)
    )


def filter_dangerous_materials(inventory_list, threshold):
    # 기준값 이상인 위험 물질만 골라내는 함수
    dangerous_list = []

    # 전체 물질 목록을 하나씩 확인
    for item in inventory_list:

        # 인화성 값이 기준 이상이면 위험 물질로 판단
        if item['Flammability'] >= threshold:
            dangerous_list.append(item)

    # 위험 물질 리스트 반환
    return dangerous_list


def save_danger_csv(file_name, inventory_list):
    # 위험 물질 목록을 CSV 파일로 저장하는 함수
    try:
        # 쓰기 모드('w'), UTF-8 인코딩으로 파일 열기
        with open(file_name, 'w', encoding='utf-8') as file:

            # CSV 헤더 한 줄 먼저 작성
            file.write(
                'Substance,Weight (g/cm³),Specific Gravity,Strength,Flammability\n'
            )

            # 위험 물질 목록을 한 줄씩 CSV 형식으로 저장
            for item in inventory_list:
                line = (
                    f"{item['Substance']},"
                    f"{item['Weight (g/cm³)']},"
                    f"{item['Specific Gravity']},"
                    f"{item['Strength']},"
                    f"{item['Flammability']}\n"
                )
                file.write(line)

        # 저장 완료 메시지 출력
        print(f'[5] 위험 물질 CSV 저장 완료: {file_name}')
        print()

    # 저장 권한이 없을 때 처리
    except PermissionError:
        print(f'[오류] 파일 저장 권한이 없습니다: {file_name}')

    # 그 외 파일 저장 중 오류 처리
    except OSError as error:
        print(f'[오류] CSV 저장 중 문제가 발생했습니다: {error}')


def save_binary_file(file_name, inventory_list):
    # 리스트 내용을 바이너리 파일 형태로 저장하는 함수
    # 실제로는 구조화된 바이너리 포맷이라기보다
    # 문자열을 UTF-8로 인코딩해서 바이너리로 저장하는 방식
    try:
        # 바이너리 쓰기 모드('wb')로 파일 열기
        with open(file_name, 'wb') as file:

            # 각 항목을 한 줄 문자열로 만든 뒤 바이트로 저장
            for item in inventory_list:
                line = (
                    f"{item['Substance']}|"
                    f"{item['Weight (g/cm³)']}|"
                    f"{item['Specific Gravity']}|"
                    f"{item['Strength']}|"
                    f"{item['Flammability']}\n"
                )

                # 문자열을 UTF-8 바이트로 변환해서 저장
                file.write(line.encode('utf-8'))

        # 저장 완료 메시지 출력
        print(f'[보너스 1] 이진 파일 저장 완료: {file_name}')
        print()

    # 저장 권한이 없을 때 처리
    except PermissionError:
        print(f'[오류] 이진 파일 저장 권한이 없습니다: {file_name}')

    # 그 외 파일 저장 중 오류 처리
    except OSError as error:
        print(f'[오류] 이진 파일 저장 중 문제가 발생했습니다: {error}')


def read_binary_file(file_name):
    # 바이너리 파일에서 데이터를 읽어 다시 리스트로 복원하는 함수
    inventory_list = []

    try:
        # 바이너리 읽기 모드('rb')로 파일 열기
        with open(file_name, 'rb') as file:
            # 파일 전체 내용을 바이트 형태로 읽음
            binary_data = file.read()

        # 바이트 데이터를 UTF-8 문자열로 디코딩
        decoded_text = binary_data.decode('utf-8')

        # 줄바꿈 기준으로 나누어 각 물질 데이터를 분리
        lines = decoded_text.strip().split('\n')

        # 각 줄을 하나씩 처리
        for line in lines:

            # 빈 줄은 건너뜀
            if not line.strip():
                continue

            # 저장할 때 | 문자로 구분했으므로 | 기준으로 분리
            parts = line.split('|')

            # 데이터 개수가 5개가 아니면 잘못된 줄로 보고 건너뜀
            if len(parts) != 5:
                continue

            try:
                # 인화성 값을 실수형으로 변환
                flammability = float(parts[4])

            # 변환 실패 시 건너뜀
            except ValueError:
                continue

            # 다시 딕셔너리 형태로 복원
            item = {
                'Substance': parts[0],
                'Weight (g/cm³)': parts[1],
                'Specific Gravity': parts[2],
                'Strength': parts[3],
                'Flammability': flammability,
            }

            # 복원된 항목을 리스트에 추가
            inventory_list.append(item)

    # 파일이 없을 때 처리
    except FileNotFoundError:
        print(f'[오류] 이진 파일을 찾을 수 없습니다: {file_name}')

    # 파일 접근 권한이 없을 때 처리
    except PermissionError:
        print(f'[오류] 이진 파일 접근 권한이 없습니다: {file_name}')

    # 일반적인 파일 입출력 오류 처리
    except OSError as error:
        print(f'[오류] 이진 파일 읽기 중 문제가 발생했습니다: {error}')

    # UTF-8 디코딩 실패 시 처리
    except UnicodeDecodeError:
        print(f'[오류] 이진 파일 디코딩에 실패했습니다: {file_name}')

    # 복원된 리스트 반환
    return inventory_list


def main():
    # 1. 원본 CSV 파일 읽기
    lines = read_text_file(INPUT_FILE)

    # 파일을 못 읽었거나 내용이 없으면 프로그램 종료
    if not lines:
        return

    # 2. CSV 원본 내용 출력
    print_file_content(lines)

    # 3. CSV 문자열 목록을 딕셔너리 리스트로 변환
    inventory_list = convert_to_inventory_list(lines)

    # 4. 인화성 기준으로 내림차순 정렬
    sorted_inventory = sort_by_flammability(inventory_list)

    # 5. 정렬 결과 출력
    print_inventory_list('[3] 인화성이 높은 순으로 정렬된 목록', sorted_inventory)

    # 6. 기준값 이상인 위험 물질만 필터링
    dangerous_inventory = filter_dangerous_materials(
        sorted_inventory,
        DANGER_THRESHOLD
    )

    # 7. 위험 물질 목록 출력
    print_inventory_list(
        f'[4] 인화성 지수 {DANGER_THRESHOLD} 이상 목록',
        dangerous_inventory
    )

    # 8. 위험 물질 목록을 CSV 파일로 저장
    save_danger_csv(DANGER_FILE, dangerous_inventory)

    # 9. 전체 정렬 목록을 바이너리 파일로 저장
    save_binary_file(BINARY_FILE, sorted_inventory)

    # 10. 바이너리 파일에서 다시 읽어서 복원
    restored_inventory = read_binary_file(BINARY_FILE)

    # 11. 복원된 목록 출력
    print_inventory_list('[보너스 2] 이진 파일에서 다시 읽어온 목록', restored_inventory)


# 현재 파일이 직접 실행된 경우에만 main() 함수 실행
# 다른 파일에서 import 하면 main()은 자동 실행되지 않음
if __name__ == '__main__':
    main()
