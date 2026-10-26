/*
 * ============================================================================
 * Problem: Endianness Detection and Byte Swapping (REV16 / REV32)
 * 
 * Objective:
 *   1. Detect whether the target CPU is Little-Endian or Big-Endian at runtime.
 *   2. Implement 16-bit and 32-bit byte-reversal functions for network/fieldbus
 *      protocols (Modbus RTU, CAN, Ethernet) without relying on non-standard libraries.
 * 
 * Embedded Hardware Insight:
 *   - ARM Cortex-M cores are almost universally configured in Little-Endian mode
 *     (LSB stored at the lowest address).
 *   - Industrial fieldbuses (e.g., Modbus, TCP/IP) use Network Byte Order (Big-Endian).
 *     When an ARM MCU reads a 16-bit Modbus register from RS-485, the high byte arrives
 *     first and must be swapped before arithmetic calculation.
 *   - GCC provides '__builtin_bswap16' and '__builtin_bswap32', which compile into
 *     single-cycle ARM assembly instructions: 'REV16' and 'REV'.
 * 
 * Complexity:
 *   - Time Complexity: O(1) single-cycle shifts and bitwise OR operations.
 *   - Space Complexity: O(1) in CPU registers.
 * 
 * Interview Follow-Up:
 *   Q: Can endianness be checked at compile time using preprocessor '#if' directives?
 *   A: In GCC/Clang, yes: '#if __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__'.
 *      However, the pointer casting technique '*(uint8_t *)&test' is the classic
 *      portable runtime method evaluated in interview technical rounds.
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

/* Runtime Endianness Check via Byte Pointer Inspection */
static bool is_little_endian(void)
{
    uint16_t test_val = 0x0001;
    uint8_t *byte_ptr = (uint8_t *)&test_val;

    /* If the lowest memory address holds 0x01, it is Little Endian */
    return (*byte_ptr == 0x01);
}

/* 16-bit Byte Swap (Equivalent to ARM REV16) */
static uint16_t swap_bytes_16(uint16_t val)
{
    return (uint16_t)(((val & 0x00FFU) << 8) |
                      ((val & 0xFF00U) >> 8));
}

/* 32-bit Byte Swap (Equivalent to ARM REV) */
static uint32_t swap_bytes_32(uint32_t val)
{
    return (((val & 0x000000FFU) << 24) |
            ((val & 0x0000FF00U) << 8)  |
            ((val & 0x00FF0000U) >> 8)  |
            ((val & 0xFF000000U) >> 24));
}

int main(void)
{
    printf("=== Day 03: Endianness Detection & Byte Swapping ===\n\n");

    /* 1. Runtime Detection */
    if (is_little_endian()) {
        printf("Target CPU Architecture: LITTLE-ENDIAN (LSB at lowest memory address)\n");
    } else {
        printf("Target CPU Architecture: BIG-ENDIAN (MSB at lowest memory address)\n");
    }

    /* 2. Visual Memory Inspection */
    uint32_t sample = 0x12345678;
    uint8_t *p = (uint8_t *)&sample;
    printf("\nMemory layout of 0x%08X:\n", sample);
    for (size_t i = 0; i < sizeof(sample); i++) {
        printf(" Address %p: [0x%02X]\n", (void *)(p + i), *(p + i));
    }

    /* 3. 16-bit Modbus Packet Swap Demo */
    uint16_t modbus_raw = 0x1234;
    uint16_t modbus_swapped = swap_bytes_16(modbus_raw);
    printf("\n16-Bit Swap (e.g. Modbus register incoming conversion):\n");
    printf(" - Raw Input : 0x%04X\n", modbus_raw);
    printf(" - Swapped   : 0x%04X\n", modbus_swapped);

    /* 4. 32-Bit Telemetry Swap Demo */
    uint32_t tel_raw = 0xAABBCCDD;
    uint32_t tel_swapped = swap_bytes_32(tel_raw);
    printf("\n32-Bit Swap (e.g. CAN payload endianness conversion):\n");
    printf(" - Raw Input : 0x%08X\n", tel_raw);
    printf(" - Swapped   : 0x%08X\n", tel_swapped);

    return 0;
}
