import time
import random
import sys

# 1. Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# 2. Quick Sort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# 3. Insertion Sort
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Setup Data
# Get data_size from CLI or default to 2000
try:
    data_size = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
except ValueError:
    print("Error: Argument must be an integer. Defaulting to 2000.")
    data_size = 2000

# Benchmark function
def benchmark(func, data, name):
    start = time.perf_counter()
    func(data.copy())
    end = time.perf_counter()
    print(f"{name:15}: {end - start:.5f} seconds")

# Dictionary of scenarios
scenarios = {
    "Random": [random.randint(0, 10000) for _ in range(data_size)],
    "Sorted": list(range(data_size)),
    "Reverse": list(range(data_size, 0, -1))
}

for label, data in scenarios.items():
    print(f"\nScenario: {label}")
    print("-" * 30)
    benchmark(bubble_sort, data, "Bubble Sort")
    benchmark(insertion_sort, data, "Insertion Sort")
    benchmark(quick_sort, data, "Quick Sort")
    benchmark(sorted, data, "Python Timsort")

