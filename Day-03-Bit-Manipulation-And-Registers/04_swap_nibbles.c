/*
 * ============================================================================
 * Problem: Swap Nibbles in an 8-bit Byte
 * 
 * Objective:
 *   Swap the higher 4 bits (nibble) with the lower 4 bits in a single byte:
 *   Example: 0x4B (0b0100_1011) becomes 0xB4 (0b1011_0100).
 * 
 * Embedded Hardware Insight:
 *   - Used constantly in 4-bit parallel display drivers (such as the ubiquitous
 *     Hitachi HD44780 LCD controller) where an 8-bit command byte must be split
 *     into two 4-bit nibbles sent sequentially over 4 GPIO data lines (D4-D7).
 *   - Critical C standard catch: Always cast to 'uint8_t'. If a developer uses
 *     'char' and the MCU defaults to 'signed char', right-shifting a byte with the
 *     MSB set (e.g., 0x80) causes arithmetic sign extension, shifting in 1s instead
 *     of 0s and corrupting the upper nibble!
 * 
 * Complexity:
 *   - Time Complexity: O(1) single-cycle shift and bitwise OR.
 *   - Space Complexity: O(1) in-place register operation.
 * 
 * Interview Follow-Up:
 *   Q: Why does '((byte & 0x0F) << 4) | (byte >> 4)' sometimes trigger compiler warnings?
 *   A: In C, integer promotion converts 'byte' to signed int before arithmetic operations.
 *      The result of the bitwise OR is an 'int'. When assigning back to 'uint8_t',
 *      strict compilers (-Wconversion) flag an implicit narrowing conversion.
 *      Explicit casting '(uint8_t)' avoids this warning completely.
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>

/* Swapping high and low 4-bit nibbles */
static uint8_t swap_nibbles(uint8_t byte)
{
    return (uint8_t)(((byte & 0x0FU) << 4) | ((byte & 0xF0U) >> 4));
}

int main(void)
{
    printf("=== Day 03: 8-Bit Nibble Swap (LCD / Protocol Utilities) ===\n\n");

    uint8_t test_cases[] = {
        0x4B, /* 0b0100_1011 -> Expected: 0xB4 (0b1011_0100) */
        0x12, /* 0b0001_0010 -> Expected: 0x21 (0b0010_0001) */
        0xF0, /* 0b1111_0000 -> Expected: 0x0F (0b0000_1111) */
        0xAA, /* 0b1010_1010 -> Expected: 0xAA (0b1010_1010) */
        0x01  /* 0b0000_0001 -> Expected: 0x10 (0b0001_0000) */
    };

    size_t num_tests = sizeof(test_cases) / sizeof(test_cases[0]);

    for (size_t i = 0; i < num_tests; i++) {
        uint8_t original = test_cases[i];
        uint8_t swapped  = swap_nibbles(original);

        printf("Test %zu: Original: 0x%02X (0b%d%d%d%d_%d%d%d%d) -> Swapped: 0x%02X (0b%d%d%d%d_%d%d%d%d)\n",
               i + 1,
               original,
               (original >> 7) & 1, (original >> 6) & 1, (original >> 5) & 1, (original >> 4) & 1,
               (original >> 3) & 1, (original >> 2) & 1, (original >> 1) & 1, (original >> 0) & 1,
               swapped,
               (swapped >> 7) & 1, (swapped >> 6) & 1, (swapped >> 5) & 1, (swapped >> 4) & 1,
               (swapped >> 3) & 1, (swapped >> 2) & 1, (swapped >> 1) & 1, (swapped >> 0) & 1);
    }

    return 0;
}
