import threading
import time


def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def compute_factorial(index, n, results, repeat=1000):
    start_time = time.time_ns()
    for _ in range(repeat):     # repeat many times for measurable timing
        factorial(n)
    end_time = time.time_ns()
    results[index] = (start_time, end_time)


def compute_factorial_seq(n, repeat=1000):
    start_time = time.time_ns()
    for _ in range(repeat):     # repeat many times for measurable timing
        factorial(n)
    end_time = time.time_ns()
    return (start_time, end_time)


def main():
    numbers = [50, 100, 200]   # Assignment factorials
    rounds = 10
    all_total_time = []
    all_total_time2 = []

    print("\nRound-by-Round Performance Comparison:")
    print("+-------------------+-----------------------------+-------------------------------+----------------------------+")
    print("| Round             | Multithreading Time (ns)    | Non-Multithreading Time (ns)  | Difference (ns)            |")
    print("+-------------------+-----------------------------+-------------------------------+----------------------------+")

    for i in range(rounds):
        results = [None] * len(numbers)
        threads = []

        for idx, num in enumerate(numbers):
            t = threading.Thread(target=compute_factorial, args=(idx, num, results))
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Calculate total time
        start_times = [r[0] for r in results]
        end_times = [r[1] for r in results]
        total_time = max(end_times) - min(start_times)
        all_total_time.append(total_time)

        # ---------------- Sequential ----------------
        results2 = [compute_factorial_seq(num) for num in numbers]
        start_times2 = [r[0] for r in results2]
        end_times2 = [r[1] for r in results2]
        total_time2 = max(end_times2) - min(start_times2)
        all_total_time2.append(total_time2)

        # ---------------- Difference ----------------
        difference = total_time - total_time2
        print(f"| {i+1:^17} | {total_time:^27,} | {total_time2:^29,} | {difference:^26,} |")

    print("+-------------------+-----------------------------+-------------------------------+----------------------------+")

    # ---------------- Summary ----------------
    total_thread = sum(all_total_time)
    total_sequential = sum(all_total_time2)
    avr_total_thread = total_thread / rounds
    avr_total_sequential = total_sequential / rounds
    total_diff = total_thread - total_sequential
    avr_total_diff = avr_total_thread - avr_total_sequential

    print("\nSummary of Results:")
    print("+-------------------+-----------------------------+-------------------------------+----------------------------+")
    print("| Metric            | With Threads (ns)           | Without Threads (ns)          | Time Difference (ns)       |")
    print("+-------------------+-----------------------------+-------------------------------+----------------------------+")
    print(f"| Total Time        | {total_thread:^27,} | {total_sequential:^29,} | {total_diff:^26,} |")
    print(f"| Average Time      | {avr_total_thread:^27,.1f} | {avr_total_sequential:^29,.1f} | {avr_total_diff:^26,.1f} |")
    print("+-------------------+-----------------------------+-------------------------------+----------------------------+")

# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    main()

