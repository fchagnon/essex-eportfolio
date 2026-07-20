import sys
import time

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def main():
    # Check for exactly two arguments (plus the script name)
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input_file> <output_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        # Load data from input file
        with open(input_path, 'r') as f:
            # Converts all strings in the file into a list of integers
            data = [int(item) for item in f.read().split()]
    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
        sys.exit(1)
    except ValueError:
        print(f"Error: The input file must contain only integers.")
        sys.exit(1)

    # Benchmarking the execution
    start_time = time.perf_counter()
    quick_sort(data)
    end_time = time.perf_counter()

    execution_time = end_time - start_time

    # Write results to output file
    with open(output_path, 'w') as f:
        f.write("Sorted Array in Ascending Order:\n")
        f.write(str(data))

    print(f"Sort complete. Results saved to: {output_path}")
    print(f"Execution time: {execution_time:.6f} seconds")

if __name__ == "__main__":
    main()
