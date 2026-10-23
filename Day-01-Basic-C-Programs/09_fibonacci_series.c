/*
 * Problem: Generate the first N Fibonacci numbers iteratively.
 *
 * Uses constant O(1) space with 2 tracking variables instead of recursive O(2^N).
 */

#define __USE_MINGW_ANSI_STDIO 1
#include <stdio.h>
#include <stdint.h>

static void print_fibonacci(uint32_t n)
{
    uint64_t a = 0;
    uint64_t b = 1;

    for (uint32_t i = 0; i < n; i++) {
        printf("%llu ", (unsigned long long)a);
        uint64_t next = a + b;
        a = b;
        b = next;
    }
    printf("\n");
}

int main(void)
{
    printf("First 10 Fibonacci numbers:\n");
    print_fibonacci(10);

    return 0;
}
