import argparse
import multiprocessing
import time
import psutil
import threading
import numpy as np
import curses

def heavy_stress_test(stop_event):
    while not stop_event.is_set():
        n = 15000
        matrix_a = np.random.rand(n, n)
        matrix_b = np.random.rand(n, n)
        while True:
            np.dot(matrix_a, matrix_b)

        find_primes_infinite()

        fibonacci_infinite()

def fibonacci_infinite():
    n = 50
    while True:
        fibonacci(n)
        n += 1

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def find_primes_infinite():
    num = 2
    while True:
        if is_prime(num):
            pass
        num += 1

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def display_cpu_usage(stdscr, stop_event, interval=1):
    curses.curs_set(0)
    stdscr.nodelay(1)
    height, width = stdscr.getmaxyx()
    stdscr.clear()
    while not stop_event.is_set():
        cpu_percent = psutil.cpu_percent(interval=interval)
        stdscr.clear()
        stdscr.addstr(0, 0, f"CPU Usage: {cpu_percent}%")
        stdscr.refresh()
        time.sleep(interval)

def run_stress_test(workers=None, all_cores=True):
    if workers is None:
        workers = multiprocessing.cpu_count() if all_cores else 1
    
    print(f"Starting stress test using {workers} CPU cores.")
    processes = []
    stop_event = multiprocessing.Event()
    
    cpu_thread = threading.Thread(target=lambda: curses.wrapper(display_cpu_usage, stop_event))
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
