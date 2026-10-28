/*
 * ============================================================================
 * Problem: Week 1 Embedded C Technical Speed Drill
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define IS_POWER_OF_TWO(n)  (((n) > 0U) && (((n) & ((n) - 1U)) == 0U))
#define ISOLATE_LOWEST_BIT(n) ((n) & -(int32_t)(n))

static uint32_t fast_bswap32(uint32_t x)
{
    return ((x & 0x000000FFU) << 24) |
           ((x & 0x0000FF00U) << 8)  |
           ((x & 0x00FF0000U) >> 8)  |
           ((x & 0xFF000000U) >> 24);
}

int main(void)
{
    printf("=== Day 07: Week 1 Speed Drills & Consolidation ===\n\n");

    uint32_t test_val = 64U;
    printf("1. Is %u Power of Two? %s\n", test_val, IS_POWER_OF_TWO(test_val) ? "YES" : "NO");

    uint32_t non_pow2 = 65U;
    printf("2. Is %u Power of Two? %s\n", non_pow2, IS_POWER_OF_TWO(non_pow2) ? "YES" : "NO");

    uint32_t val = 0x00000018; /* 0b...0001_1000 */
    printf("3. Lowest set bit of 0x%08X is: 0x%08X (Expected 0x08)\n", val, ISOLATE_LOWEST_BIT(val));

    uint32_t word = 0xAABBCCDD;
    printf("4. Byte swap 0x%08X -> 0x%08X\n", word, fast_bswap32(word));

    return 0;
}
