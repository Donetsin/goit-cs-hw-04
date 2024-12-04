import threading
import os
import time

def search_keywords_in_files(files, keywords, result_dict, lock):
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().lower()
                for keyword in keywords:
                    if keyword.lower() in content:
                        with lock:
                            if keyword not in result_dict:
                                result_dict[keyword] = []
                            if file_path not in result_dict[keyword]:
                                result_dict[keyword].append(file_path)
        except Exception as e:
            print(f"Помилка обробки файлу {file_path}: {e}")

def main_threading(files, keywords, num_threads=4):
    start_time = time.time()

    chunk_size = len(files) // num_threads
    threads = []
    result_dict = {}
    lock = threading.Lock()

    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_threads - 1 else len(files)
        thread_files = files[start:end]
        thread = threading.Thread(target=search_keywords_in_files, args=(thread_files, keywords, result_dict, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Результати багатопотокового підходу:")
    print(result_dict)
    print(f"Час виконання: {time.time() - start_time} секунд")

if __name__ == "__main__":
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']
    keywords = ['python', 'threading', 'multiprocessing', 'Error']
    main_threading(files, keywords, num_threads=2)