/*
 * Problem: Calculate factorial of N iteratively.
 *
 * Recursion is avoided in embedded systems to protect against stack overflow
 * in memory-constrained microcontrollers (MISRA-C Rule 17.2).
 */

#define __USE_MINGW_ANSI_STDIO 1
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

static bool factorial(uint32_t n, uint64_t *res)
{
    if (!res) {
        return false;
    }

    /* 64-bit uint64_t overflows at 21! */
    if (n > 20) {
        return false;
    }

    uint64_t val = 1;
    for (uint32_t i = 2; i <= n; i++) {
        val *= i;
    }

    *res = val;
    return true;
}

int main(void)
{
    uint32_t tests[] = {0, 1, 5, 10, 15, 20, 21};
    int count = sizeof(tests) / sizeof(tests[0]);

    for (int i = 0; i < count; i++) {
        uint64_t result = 0;
        if (factorial(tests[i], &result)) {
            printf("%2u! = %llu\n", tests[i], (unsigned long long)result);
        } else {
            printf("%2u! = Overflow (> 64-bit)\n", tests[i]);
        }
    }

    return 0;
}
