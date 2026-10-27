import csv
import random
import statistics
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from inversion import count_inversions

SIZES = [1000, 2000, 4000, 8000, 16000]
TRIALS = 5
SEED = 42


def brute_force(a):
    n = len(a)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] > a[j]:
                count += 1
    return count


def time_ms(func, data):
    copy = data[:]
    start = time.perf_counter()
    result = func(copy)
    elapsed = (time.perf_counter() - start) * 1000
    return result, elapsed


def main():
    rng = random.Random(SEED)
    rows = []

    print(f"{'n':>7} {'divide_conquer_ms':>18} {'brute_force_ms':>15}")
    for n in SIZES:
        data = [rng.randint(0, 10**6) for _ in range(n)]
        original = data[:]

        if count_inversions(data[:]) != brute_force(data):
            raise SystemExit(f"Mismatch in inversion counts at n={n}")

        dc_times = []
        bf_times = []
        for _ in range(TRIALS):
            _, t = time_ms(count_inversions, data)
            dc_times.append(t)
            _, t = time_ms(brute_force, data)
            bf_times.append(t)

        assert data == original, "input array was modified"

        dc_ms = statistics.median(dc_times)
        bf_ms = statistics.median(bf_times)
        rows.append((n, dc_ms, bf_ms))
        print(f"{n:>7} {dc_ms:>18.3f} {bf_ms:>15.3f}")

    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "divide_conquer_ms", "brute_force_ms"])
        for n, dc_ms, bf_ms in rows:
            writer.writerow([n, f"{dc_ms:.3f}", f"{bf_ms:.3f}"])

    print("Results saved to results.csv")

    ns = [r[0] for r in rows]
    plt.plot(ns, [r[1] for r in rows], marker="o", label="Divide and conquer (O(n log n))")
    plt.plot(ns, [r[2] for r in rows], marker="s", label="Brute force (O(n^2))")
    plt.xlabel("Array size n")
    plt.ylabel("Median runtime (ms)")
    plt.title(f"Inversion counting runtime (median of {TRIALS} trials)")
    plt.legend()
    plt.grid(True)
    plt.yscale("log")
    plt.savefig("runtime_comparison.png", dpi=150, bbox_inches="tight")
    print("Graph saved to runtime_comparison.png")


if __name__ == "__main__":
    main()
