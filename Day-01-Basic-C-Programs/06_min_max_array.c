/*
 * Problem: Find minimum and maximum elements in an array in a single pass.
 */

#include <stdio.h>
#include <stdbool.h>
#include <stddef.h>

static bool find_min_max(const int *arr, size_t size, int *min, int *max)
{
    if (!arr || !min || !max || size == 0) {
        return false;
    }

    *min = arr[0];
    *max = arr[0];

    for (size_t i = 1; i < size; i++) {
        if (arr[i] > *max) {
            *max = arr[i];
        } else if (arr[i] < *min) {
            *min = arr[i];
        }
    }

    return true;
}

int main(void)
{
    int data[] = {34, -5, 89, 12, 0, 77};
    size_t size = sizeof(data) / sizeof(data[0]);
    int min_val, max_val;

    if (find_min_max(data, size, &min_val, &max_val)) {
        printf("Array: [34, -5, 89, 12, 0, 77]\n");
        printf("Min: %d, Max: %d\n", min_val, max_val);
    }

    return 0;
}
