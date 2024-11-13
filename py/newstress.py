import argparse
import multiprocessing
import time
import psutil
import threading
import numpy as np

def heavy_stress_test(stop_event):
    while not stop_event.is_set():
        n = 1000
        matrix_a = np.random.rand(n, n)
        matrix_b = np.random.rand(n, n)
        result = np.dot(matrix_a, matrix_b)
        _ = result

def display_cpu_usage(stop_event, interval=1):
    while not stop_event.is_set():
        cpu_percent = psutil.cpu_percent(interval=interval)
        print(f"CPU Usage: {cpu_percent}%")
        time.sleep(interval)

def run_stress_test(workers=None, all_cores=True):
    if workers is None:
        workers = multiprocessing.cpu_count() if all_cores else 1
    
    print(f"Starting stress test using {workers} CPU cores.")
    processes = []
    stop_event = multiprocessing.Event()

    cpu_thread = threading.Thread(target=display_cpu_usage, args=(stop_event,))
    cpu_thread.start()

    for _ in range(workers):
        p = multiprocessing.Process(target=heavy_stress_test, args=(stop_event,))
        p.start()
        processes.append(p)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stress test manually interrupted.")
    finally:
        print("Stopping the stress test.")
        stop_event.set()
        for p in processes:
            p.terminate()
        cpu_thread.join()
        print("Stress test completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stress test your CPU by utilizing multiple cores.")
    parser.add_argument('-c', '--cpu', type=int, help="Number of CPU cores to use.", default=None)
    parser.add_argument('--all-cores', action='store_true', help="Use all available CPU cores.")
    
    args = parser.parse_args()

    run_stress_test(workers=args.cpu, all_cores=args.all_cores)
