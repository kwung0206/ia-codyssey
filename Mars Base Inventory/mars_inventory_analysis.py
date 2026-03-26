INPUT_FILE = 'Mars_Base_Inventory_List.csv'
DANGER_FILE = 'Mars_Base_Inventory_danger.csv'
BINARY_FILE = 'Mars_Base_Inventory_List.bin'
DANGER_THRESHOLD = 0.7


def read_text_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return [line.rstrip('\n') for line in file]
    except FileNotFoundError:
        print(f'[오류] 파일을 찾을 수 없습니다: {file_name}')
    except PermissionError:
        print(f'[오류] 파일 접근 권한이 없습니다: {file_name}')
    except OSError as error:
        print(f'[오류] 파일 읽기 중 문제가 발생했습니다: {error}')

    return []


def print_file_content(lines):
    print('[1] CSV 원본 내용 출력')
    for line in lines:
        print(line)
    print()


def convert_to_inventory_list(lines):
    inventory_list = []

    if not lines:
        return inventory_list

    header = [item.strip() for item in lines[0].split(',')]

    for index, line in enumerate(lines[1:], start=2):
        if not line.strip():
            continue

        parts = [item.strip() for item in line.split(',')]

        if len(parts) != 5:
            print(f'[경고] {index}번째 줄 형식이 올바르지 않아 건너뜁니다: {line}')
            continue

        try:
            flammability = float(parts[4])
        except ValueError:
            print(f'[경고] {index}번째 줄의 인화성 지수 변환에 실패했습니다: {line}')
            continue

        item = {
            'Substance': parts[0],
            'Weight (g/cm³)': parts[1],
            'Specific Gravity': parts[2],
            'Strength': parts[3],
            'Flammability': flammability,
        }
        inventory_list.append(item)

    print('[2] CSV 내용을 리스트 객체로 변환 완료')
    print(inventory_list)
    print()

    return inventory_list


def print_inventory_list(title, inventory_list):
    print(title)

    if not inventory_list:
        print('데이터가 없습니다.')
        print()
        return

    for item in inventory_list:
        print(
            f"물질명: {item['Substance']}, "
            f"밀도: {item['Weight (g/cm³)']}, "
            f"비중: {item['Specific Gravity']}, "
            f"강도: {item['Strength']}, "
            f"인화성: {item['Flammability']}"
        )
    print()


def sort_by_flammability(inventory_list):
    return sorted(
        inventory_list,
        key=lambda item: item['Flammability'],
        reverse=True
    )


def filter_dangerous_materials(inventory_list, threshold):
    dangerous_list = []

    for item in inventory_list:
        if item['Flammability'] >= threshold:
            dangerous_list.append(item)

    return dangerous_list


def save_danger_csv(file_name, inventory_list):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(
                'Substance,Weight (g/cm³),Specific Gravity,Strength,Flammability\n'
            )

            for item in inventory_list:
                line = (
                    f"{item['Substance']},"
                    f"{item['Weight (g/cm³)']},"
                    f"{item['Specific Gravity']},"
                    f"{item['Strength']},"
                    f"{item['Flammability']}\n"
                )
                file.write(line)

        print(f'[5] 위험 물질 CSV 저장 완료: {file_name}')
        print()
    except PermissionError:
        print(f'[오류] 파일 저장 권한이 없습니다: {file_name}')
    except OSError as error:
        print(f'[오류] CSV 저장 중 문제가 발생했습니다: {error}')


def save_binary_file(file_name, inventory_list):
    try:
        with open(file_name, 'wb') as file:
            for item in inventory_list:
                line = (
                    f"{item['Substance']}|"
                    f"{item['Weight (g/cm³)']}|"
                    f"{item['Specific Gravity']}|"
                    f"{item['Strength']}|"
                    f"{item['Flammability']}\n"
                )
                file.write(line.encode('utf-8'))

        print(f'[보너스 1] 이진 파일 저장 완료: {file_name}')
        print()
    except PermissionError:
        print(f'[오류] 이진 파일 저장 권한이 없습니다: {file_name}')
    except OSError as error:
        print(f'[오류] 이진 파일 저장 중 문제가 발생했습니다: {error}')


def read_binary_file(file_name):
    inventory_list = []

    try:
        with open(file_name, 'rb') as file:
            binary_data = file.read()

        decoded_text = binary_data.decode('utf-8')
        lines = decoded_text.strip().split('\n')

        for line in lines:
            if not line.strip():
                continue

            parts = line.split('|')

            if len(parts) != 5:
                continue

            try:
                flammability = float(parts[4])
            except ValueError:
                continue

            item = {
                'Substance': parts[0],
                'Weight (g/cm³)': parts[1],
                'Specific Gravity': parts[2],
                'Strength': parts[3],
                'Flammability': flammability,
            }
            inventory_list.append(item)

    except FileNotFoundError:
        print(f'[오류] 이진 파일을 찾을 수 없습니다: {file_name}')
    except PermissionError:
        print(f'[오류] 이진 파일 접근 권한이 없습니다: {file_name}')
    except OSError as error:
        print(f'[오류] 이진 파일 읽기 중 문제가 발생했습니다: {error}')
    except UnicodeDecodeError:
        print(f'[오류] 이진 파일 디코딩에 실패했습니다: {file_name}')

    return inventory_list


def main():
    lines = read_text_file(INPUT_FILE)

    if not lines:
        return

    print_file_content(lines)

    inventory_list = convert_to_inventory_list(lines)

    sorted_inventory = sort_by_flammability(inventory_list)
    print_inventory_list('[3] 인화성이 높은 순으로 정렬된 목록', sorted_inventory)

    dangerous_inventory = filter_dangerous_materials(
        sorted_inventory,
        DANGER_THRESHOLD
    )
    print_inventory_list(
        f'[4] 인화성 지수 {DANGER_THRESHOLD} 이상 목록',
        dangerous_inventory
    )

    save_danger_csv(DANGER_FILE, dangerous_inventory)

    save_binary_file(BINARY_FILE, sorted_inventory)

    restored_inventory = read_binary_file(BINARY_FILE)
    print_inventory_list('[보너스 2] 이진 파일에서 다시 읽어온 목록', restored_inventory)


if __name__ == '__main__':
    main()
