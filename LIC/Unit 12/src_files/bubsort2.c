#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/* * Original Algorithm: Bubble Sort (O(n^2))
 * This remains unmodified to serve as the performance baseline for 
 * comparison against the Python Quicksort implementation.
 */
void bubbleSort(int array[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (array[j] > array[j + 1]) {
                int temp = array[j];
                array[j] = array[j + 1];
                array[j + 1] = temp;
            }
        }
    }
}

int main(int argc, char *argv[]) {
    // Ensuring professional command-line usage for input/output targets
    if (argc != 3) {
        printf("Usage: %s <input_file> <output_file>\n", argv[0]);
        return 1;
    }

    FILE *inputFile = fopen(argv[1], "r");
    if (inputFile == NULL) {
        perror("Error opening input file");
        return 1;
    }

    /* * Modification: Dynamic Memory Management
     * Using malloc and realloc allows the program to handle the 800,000+ 
     * entries in CPUPI.txt without risking a stack overflow.
     */
    int *data = NULL;
    int capacity = 100; // Initial small allocation
    int size = 0;
    data = malloc(capacity * sizeof(int));

    int value;
    // Modification: File ingestion loop to parse the Pi dataset
    while (fscanf(inputFile, "%d", &value) == 1) {
        if (size >= capacity) {
            capacity *= 2; // Geometric growth minimizes expensive realloc calls
            int *temp = realloc(data, capacity * sizeof(int));
            if (temp == NULL) {
                fprintf(stderr, "Memory allocation failed\n");
                free(data);
                fclose(inputFile);
                return 1;
            }
            data = temp;
        }
        data[size++] = value;
    }
    fclose(inputFile);

    /* * Modification: Precision Benchmarking
     * We use clock() to isolate the algorithm's runtime from the 
     * file I/O overhead for accurate Big O growth comparison.
     */
    clock_t start = clock();
    bubbleSort(data, size);
    clock_t end = clock();

    double cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;

    // Modification: Saving sorted results to specified output file
    FILE *outputFile = fopen(argv[2], "w");
    if (outputFile != NULL) {
        fprintf(outputFile, "Sorted Array in Ascending Order:\n");
        for (int i = 0; i < size; i++) {
            fprintf(outputFile, "%d ", data[i]);
        }
        fclose(outputFile);
    }

    printf("Sort complete. Execution time: %f seconds\n", cpu_time_used);

    // Manual memory cleanup is essential in C to prevent memory leaks.
    free(data);
    return 0;
}
