/*
 * ============================================================================
 * Problem: Bitwise Manipulation Macros for Hardware Silicon Registers
 * 
 * Focus:
 *   - SET_BIT(reg, bit): Set specific bit to 1.
 *   - CLEAR_BIT(reg, bit): Clear specific bit to 0.
 *   - TOGGLE_BIT(reg, bit): Invert specific bit.
 *   - CHECK_BIT(reg, bit): Test if specific bit is 1 or 0.
 *   - MODIFY_REG(reg, mask, val): Clear bitfield mask and write new value.
 * 
 * Embedded Hardware Insight:
 *   - Why '1U' instead of '1'? In standard C, integer literal '1' is of type signed int.
 *     Shifting a signed 1 into bit position 31 (or 15 on 16-bit systems) triggers undefined
 *     behavior by shifting into the sign bit. '1U' guarantees unsigned arithmetic.
 *   - Macro parenthesis rule: Every macro parameter must be parenthesized to prevent
 *     operator precedence bugs when passing expressions (e.g., bit + 1).
 * 
 * Complexity:
 *   - Time Complexity: O(1) single-cycle ALU instructions (ORR, BIC, EOR, TST on ARM Cortex-M).
 *   - Space Complexity: O(1) in-place register modification.
 * 
 * Interview Follow-Up:
 *   Q: Why do firmware engineers avoid bitwise operations directly inside non-atomic
 *      read-modify-write loops on shared peripheral registers?
 *   A: In Cortex-M, 'reg |= (1U << bit)' compiles to three instructions: LDR, ORR, STR.
 *      If an ISR preempts between LDR and STR, register updates made by the ISR get overwritten!
 *      To prevent this, use atomic bit-banding (Cortex-M3/M4) or dedicated SET/CLR registers
 *      (e.g., STM32 GPIO BSRR register).
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

/* --- Essential Embedded Bitwise Macros --- */
#define SET_BIT(reg, bit)       ((reg) |= (1U << (bit)))
#define CLEAR_BIT(reg, bit)     ((reg) &= ~(1U << (bit)))
#define TOGGLE_BIT(reg, bit)    ((reg) ^= (1U << (bit)))
#define CHECK_BIT(reg, bit)     (((reg) >> (bit)) & 1U)
#define MODIFY_REG(reg, mask, val) ((reg) = (((reg) & ~(mask)) | ((val) & (mask))))

/* Helper function to display binary representation */
static void print_binary_32(uint32_t val, const char *label)
{
    printf("%-20s: 0x%08X | ", label, val);
    for (int i = 31; i >= 0; i--) {
        printf("%d", (val >> i) & 1U);
        if (i % 8 == 0 && i != 0) {
            printf(" ");
        }
    }
    printf("\n");
}

int main(void)
{
    printf("=== Day 03: Silicon Register Bitwise Manipulation Macros ===\n\n");

    /* Simulated 32-bit hardware register (e.g., GPIO Output Data Register) */
    uint32_t simulated_odr = 0x00000000;
    print_binary_32(simulated_odr, "Initial Register");

    /* 1. Set Bit 5 (e.g., turn ON Status LED) */
    SET_BIT(simulated_odr, 5);
    print_binary_32(simulated_odr, "Set Bit 5 (LED ON)");

    /* 2. Set Bit 12 (e.g., turn ON Relay) */
    SET_BIT(simulated_odr, 12);
    print_binary_32(simulated_odr, "Set Bit 12 (Relay ON)");

    /* 3. Check Bit 5 */
    printf("Check Bit 5 status     : %s\n", CHECK_BIT(simulated_odr, 5) ? "ACTIVE (1)" : "INACTIVE (0)");

    /* 4. Toggle Bit 5 (Turn OFF Status LED) */
    TOGGLE_BIT(simulated_odr, 5);
    print_binary_32(simulated_odr, "Toggle Bit 5 (LED OFF)");

    /* 5. Clear Bit 12 (Turn OFF Relay) */
    CLEAR_BIT(simulated_odr, 12);
    print_binary_32(simulated_odr, "Clear Bit 12 (Relay OFF)");

    /* 6. Multi-bit Field Modification (e.g. Set 4-bit Prescaler field at bits [7:4] to value 0xA) */
    uint32_t prescaler_mask = (0xFU << 4); /* bits 4, 5, 6, 7 */
    uint32_t prescaler_val  = (0xAU << 4); /* value 10 (binary 1010) shifted to position */
    MODIFY_REG(simulated_odr, prescaler_mask, prescaler_val);
    print_binary_32(simulated_odr, "Modify Bits [7:4] to 0xA");

    return 0;
}
