import math
import multiprocessing
import os
import queue
import time
import zipfile
import zlib


CHARSET = '0123456789abcdefghijklmnopqrstuvwxyz'
PASSWORD_LENGTH = 6
DEFAULT_ZIP_PATH = 'emergency_storage_key.zip'
DEFAULT_OUTPUT_PATH = 'password.txt'
DEFAULT_CPU_RATIO = 1.0
PROGRESS_INTERVAL = 10
PROGRESS_BATCH = 500000
READ_SIZE = 65536


def _number_to_password(number):
    chars = ['0'] * PASSWORD_LENGTH
    base = len(CHARSET)

    for index in range(PASSWORD_LENGTH - 1, -1, -1):
        number, remainder = divmod(number, base)
        chars[index] = CHARSET[remainder]

    return ''.join(chars)


def _read_member(archive, member, password):
    with archive.open(member, 'r', pwd=password) as file:
        while file.read(READ_SIZE):
            pass


def _looks_like_password(archive, member, password):
    try:
        with archive.open(member, 'r', pwd=password) as file:
            file.read(1)
        return True
    except (RuntimeError, zipfile.BadZipFile, zlib.error, EOFError):
        return False


def _verify_password(zip_path, password):
    try:
        with zipfile.ZipFile(zip_path, 'r') as archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue
                _read_member(archive, member, password)
        return True
    except (RuntimeError, zipfile.BadZipFile, zlib.error, EOFError, OSError):
        return False


def _worker(
        zip_path,
        first_member_name,
        worker_index,
        worker_count,
        total_count,
        found_event,
        attempts,
        result_queue,
        progress_batch):
    local_attempts = 0

    try:
        with zipfile.ZipFile(zip_path, 'r') as archive:
            first_member = archive.getinfo(first_member_name)

            for number in range(worker_index, total_count, worker_count):
                if found_event.is_set():
                    break

                password_text = _number_to_password(number)
                password = password_text.encode('utf-8')
                local_attempts += 1

                if _looks_like_password(archive, first_member, password):
                    if _verify_password(zip_path, password):
                        found_event.set()
                        result_queue.put(password_text)
                        break

                if local_attempts >= progress_batch:
                    with attempts.get_lock():
                        attempts.value += local_attempts
                    local_attempts = 0
    except (FileNotFoundError, zipfile.BadZipFile, OSError) as error:
        result_queue.put({'error': str(error)})
        found_event.set()
    finally:
        if local_attempts:
            with attempts.get_lock():
                attempts.value += local_attempts


def _get_file_members(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as archive:
            return [
                member.filename
                for member in archive.infolist()
                if not member.is_dir()
            ]
    except FileNotFoundError:
        print(f'zip 파일을 찾을 수 없습니다: {zip_path}')
    except zipfile.BadZipFile:
        print(f'올바른 zip 파일이 아닙니다: {zip_path}')
    except OSError as error:
        print(f'zip 파일을 여는 중 오류가 발생했습니다: {error}')

    return []



def _get_multiprocessing_context():
    methods = multiprocessing.get_all_start_methods()

    if 'fork' in methods:
        return multiprocessing.get_context('fork')

    return multiprocessing.get_context()


def _get_worker_count(cpu_ratio):
    cpu_count = os.cpu_count() or 1
    safe_ratio = max(0.1, min(cpu_ratio, 1.0))
    worker_count = math.floor(cpu_count * safe_ratio)

    return max(1, worker_count)


def _format_seconds(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)

    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


def _print_progress(start_time, attempts, total_count):
    elapsed = time.time() - start_time
    done_count = attempts.value
    percent = done_count / total_count * 100
    speed = done_count / elapsed if elapsed > 0 else 0

    print(
        f'반복 회수: {done_count:,} / {total_count:,} '
        f'({percent:.6f}%), 진행 시간: {_format_seconds(elapsed)}, '
        f'속도: {speed:,.2f}회/초',
        flush=True
    )


def _save_password(password, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(password + '\n')
        return True
    except OSError as error:
        print(f'비밀번호 저장 실패: {error}')
        return False


def unlock_zip(
        zip_path=DEFAULT_ZIP_PATH,
        output_path=DEFAULT_OUTPUT_PATH,
        cpu_ratio=DEFAULT_CPU_RATIO):
    members = _get_file_members(zip_path)

    if not members:
        print('zip 파일 안에 검사할 파일이 없습니다.')
        return None

    total_count = len(CHARSET) ** PASSWORD_LENGTH
    worker_count = min(_get_worker_count(cpu_ratio), total_count)
    first_member_name = members[0]
    manager_context = _get_multiprocessing_context()
    found_event = manager_context.Event()
    attempts = manager_context.Value('Q', 0)
    result_queue = manager_context.Queue()
    processes = []
    start_time = time.time()
    start_text = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))

    print(f'시작 시간: {start_text}', flush=True)
    print(f'대상 파일: {zip_path}', flush=True)
    print(f'암호 규칙: 숫자와 소문자 알파벳으로 구성된 {PASSWORD_LENGTH}자리', flush=True)
    print(f'전체 경우의 수: {total_count:,}', flush=True)
    print(f'사용 프로세스 수: {worker_count}개, 목표 사용률: {cpu_ratio * 100:.0f}%', flush=True)

    try:
        for worker_index in range(worker_count):
            process = manager_context.Process(
                target=_worker,
                args=(
                    zip_path,
                    first_member_name,
                    worker_index,
                    worker_count,
                    total_count,
                    found_event,
                    attempts,
                    result_queue,
                    PROGRESS_BATCH
                )
            )
            process.start()
            processes.append(process)

        password = None

        while any(process.is_alive() for process in processes):
            try:
                result = result_queue.get(timeout=PROGRESS_INTERVAL)
                if isinstance(result, dict) and 'error' in result:
                    error_message = result.get('error')
                    print(f'작업 중 오류가 발생했습니다: {error_message}')
                    found_event.set()
                    break
                password = result
                found_event.set()
                break
            except queue.Empty:
                _print_progress(start_time, attempts, total_count)

        for process in processes:
            process.join()

        while not result_queue.empty() and password is None:
            result = result_queue.get_nowait()
            if isinstance(result, str):
                password = result

        _print_progress(start_time, attempts, total_count)

        if password is None:
            print('암호를 찾지 못했습니다.')
            return None

        if _save_password(password, output_path):
            print(f'암호 해제 성공: {password}')
            print(f'암호 저장 완료: {output_path}')

        return password
    except KeyboardInterrupt:
        found_event.set()
        print('사용자 요청으로 작업을 중단합니다.')

        for process in processes:
            if process.is_alive():
                process.terminate()
            process.join()

        return None


if __name__ == '__main__':
    multiprocessing.freeze_support()
    unlock_zip()
