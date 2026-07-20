import sys
import time

def bubbleSort(array):
    """
    Original algorithm provided by instructor.
    Complexity: O(n^2) - The nested loop structure results in quadratic growth,
    making this inefficient for large datasets like CPUPI.txt.
    """
    for i in range(len(array)):
        for j in range(0, len(array) - i - 1):
            if array[j] > array[j + 1]:
                # Standard swap logic
                temp = array[j]
                array[j] = array[j+1]
                array[j+1] = temp

def main():
    # Modification: Professional argument validation for CLI usage
    if len(sys.argv) != 3:
        print("Usage: python bubsort_mod.py <input_file> <output_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        # Modification: Dynamic file reading to replace hardcoded baseline data.
        # This allows the script to process the 800,000+ integers in the Pi dataset.
        with open(input_path, 'r') as f:
            data = [int(item) for item in f.read().split()]
    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
        sys.exit(1)
    except ValueError:
        print(f"Error: The input file must contain only integers.")
        sys.exit(1)

    # Modification: Using high-resolution perf_counter for accurate benchmarking.
    start_time = time.perf_counter()
    bubbleSort(data)
    end_time = time.perf_counter()

    execution_time = end_time - start_time

    # Modification: Output redirected to file to satisfy assignment requirements.
    with open(output_path, 'w') as f:
        f.write("Sorted Array in Ascending Order:\n")
        f.write(str(data))

    print(f"Sort complete. Results saved to: {output_path}")
    print(f"Execution time: {execution_time:.6f} seconds")

if __name__ == "__main__":
    main()
