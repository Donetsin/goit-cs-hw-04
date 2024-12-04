import multiprocessing
import os
import time

def search_keywords_in_files(files, keywords, result_queue):
    local_results = {}
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().lower()
                for keyword in keywords:
                    if keyword.lower() in content:
                        if keyword not in local_results:
                            local_results[keyword] = []
                        if file_path not in local_results[keyword]:
                            local_results[keyword].append(file_path)
        except Exception as e:
            print(f"Помилка обробки файлу {file_path}: {e}")
    result_queue.put(local_results)

def main_multiprocessing(files, keywords, num_processes=4):
    start_time = time.time()
    # Split files into equal parts for each process
    chunk_size = len(files) // num_processes
    processes = []
    result_queue = multiprocessing.Queue()

    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_processes - 1 else len(files)
        thread_files = files[start:end]
        process = multiprocessing.Process(target=search_keywords_in_files, args=(thread_files, keywords, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    final_results = {}
    while not result_queue.empty():
        local_results = result_queue.get()
        for keyword, file_list in local_results.items():
            if keyword not in final_results:
                final_results[keyword] = []
            final_results[keyword].extend(file_list)

    print("Результати багатопроцесорного підходу:")
    print(final_results)
    print(f"Час виконання: {time.time() - start_time} секунд")

if __name__ == "__main__":
    # Example usage
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']
    keywords = ['python', 'threading', 'multiprocessing','Error']
    main_multiprocessing(files, keywords, num_processes=2)