/*
 * ============================================================================
 * Problem: Circular Bit Rotation (Rotate Left / Rotate Right)
 * 
 * Objective:
 *   Implement circular bit rotation (ROL and ROR) where bits shifted out of
 *   one end wrap around and enter the opposite end without being discarded:
 *     - ROL(val, shift): Rotate bits left by 'shift' positions.
 *     - ROR(val, shift): Rotate bits right by 'shift' positions.
 * 
 * Embedded Hardware Insight:
 *   - The C programming language has no native rotation operator (only '<<' and '>>').
 *     However, almost all CPU architectures have native hardware rotation instructions:
 *     ARM has 'ROR', x86 has 'ROL'/'ROR', and PIC has 'RLCF'/'RRCF'.
 *   - Modern optimizing compilers (GCC, Clang) automatically recognize the idiom:
 *     '(val << shift) | (val >> (32 - shift))' and compile it into a single-cycle
 *     'ROR' instruction!
 *   - Crucial edge case: If 'shift == 0' or 'shift >= 32', shifting by 32 in C is
 *     undefined behavior. Always mask shift: 'shift &= 31'.
 * 
 * Complexity:
 *   - Time Complexity: O(1) single CPU instruction when optimized.
 *   - Space Complexity: O(1) in register.
 * 
 * Interview Follow-Up:
 *   Q: What is the difference between an arithmetic right shift and a logical right shift?
 *   A: Logical right shift (on unsigned integers) always shifts in 0s into the MSB.
 *      Arithmetic right shift (on signed integers) preserves the sign bit by shifting
 *      in copies of the MSB (sign extension). In embedded register programming,
 *      always use unsigned types to guarantee logical shifts.
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>

/* Circular Rotate Left for 32-bit unsigned integer */
static uint32_t rotate_left_32(uint32_t val, uint32_t shift)
{
    shift &= 31U; /* Prevent undefined shift >= 32 */
    if (shift == 0U) {
        return val;
    }
    return (val << shift) | (val >> (32U - shift));
}

/* Circular Rotate Right for 32-bit unsigned integer */
static uint32_t rotate_right_32(uint32_t val, uint32_t shift)
{
    shift &= 31U; /* Prevent undefined shift >= 32 */
    if (shift == 0U) {
        return val;
    }
    return (val >> shift) | (val << (32U - shift));
}

/* Circular Rotate Left for 8-bit unsigned integer */
static uint8_t rotate_left_8(uint8_t val, uint8_t shift)
{
    shift &= 7U;
    if (shift == 0U) {
        return val;
    }
    return (uint8_t)((val << shift) | (val >> (8U - shift)));
}

int main(void)
{
    printf("=== Day 03: Circular Bit Rotation (Cryptographic & CRC Patterns) ===\n\n");

    /* 8-Bit Rotation Test */
    uint8_t byte = 0x85; /* 0b1000_0101 */
    printf("Original 8-bit byte: 0x%02X (0b10000101)\n", byte);

    uint8_t byte_rol2 = rotate_left_8(byte, 2);
    /* 0b1000_0101 << 2 = 0b0001_0100, bits 7 and 6 wrap to bits 1 and 0 -> 0b0001_0110 (0x16) */
    printf("ROL by 2 positions : 0x%02X (Expected: 0x16)\n\n", byte_rol2);

    /* 32-Bit Rotation Test */
    uint32_t word = 0x80000001; /* MSB and LSB set */
    printf("Original 32-bit word: 0x%08X\n", word);

    uint32_t word_rol1 = rotate_left_32(word, 1);
    printf("ROL by 1 position   : 0x%08X (Expected: 0x00000003)\n", word_rol1);

    uint32_t word_ror1 = rotate_right_32(word, 1);
    printf("ROR by 1 position   : 0x%08X (Expected: 0xC0000000)\n", word_ror1);

    uint32_t word_rol4 = rotate_left_32(0x12345678, 4);
    printf("\nRotate 0x12345678 Left by 4 bits:\n");
    printf(" Result: 0x%08X (Expected: 0x23456781)\n", word_rol4);

    return 0;
}
