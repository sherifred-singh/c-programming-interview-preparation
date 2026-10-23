/*
 * Problem: Count the number of set bits (1s) in an integer (Population Count).
 *
 * Brian Kernighan's algorithm clears the lowest set bit in each step using
 * (n &= n - 1), running in O(K) iterations where K is the number of set bits,
 * rather than looping through all 32 bits.
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

static uint32_t count_set_bits(uint32_t n)
{
    uint32_t count = 0;

    while (n > 0) {
        n &= (n - 1); /* Clears the least significant set bit */
        count++;
    }

    return count;
}

static bool is_power_of_two(uint32_t n)
{
    /* A power of two has exactly one set bit */
    return (n > 0) && ((n & (n - 1)) == 0);
}

int main(void)
{
    uint32_t tests[] = {0, 1, 7, 16, 29, 0xFF, 0x12345678};
    int count = sizeof(tests) / sizeof(tests[0]);

    printf("--- Set Bit Counter & Power of 2 Check ---\n");
    for (int i = 0; i < count; i++) {
        uint32_t val = tests[i];
        printf("Value: 0x%08X (%10u) -> Set bits: %2u | Power of 2: %s\n",
               val,
               val,
               count_set_bits(val),
               is_power_of_two(val) ? "Yes" : "No");
    }

    return 0;
}
