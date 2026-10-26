/*
 * ============================================================================
 * Problem: Accessing Memory-Mapped Hardware Peripheral Registers via Volatile Pointers
 * 
 * Embedded Hardware Insight:
 *   Hardware peripheral registers exist at fixed 32-bit physical addresses:
 *   e.g. STM32 GPIOA_ODR = 0x40020014.
 *   Writing to hardware requires exact memory writes:
 *       #define GPIOA_ODR  (*(volatile uint32_t *)0x40020014)
 *   If 'volatile' is omitted, an optimizing compiler that sees:
 *       GPIOA_ODR = 0x01;
 *       GPIOA_ODR = 0x00;
 *   will remove the first write as 'redundant dead code', and the pin never pulses!
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>

/* Simulated Hardware Register Bank in RAM */
static uint32_t s_mock_peripheral_memory[4] = {0};

#define SIM_STATUS_REG  (*(volatile uint32_t *)&s_mock_peripheral_memory[0])
#define SIM_CONTROL_REG (*(volatile uint32_t *)&s_mock_peripheral_memory[1])
#define SIM_DATA_REG    (*(volatile uint32_t *)&s_mock_peripheral_memory[2])

#define STATUS_TX_EMPTY_BIT (1U << 0)
#define CONTROL_ENABLE_BIT  (1U << 0)

int main(void)
{
    printf("=== Day 04: Volatile Memory-Mapped Peripheral Register Access ===\n\n");

    /* 1. Initialize peripheral control */
    SIM_CONTROL_REG |= CONTROL_ENABLE_BIT;
    printf("Control register configured: 0x%08X\n", SIM_CONTROL_REG);

    /* 2. Simulate hardware setting TX_EMPTY status bit */
    SIM_STATUS_REG |= STATUS_TX_EMPTY_BIT;

    /* 3. Wait for hardware status register to indicate TX is ready */
    if (SIM_STATUS_REG & STATUS_TX_EMPTY_BIT) {
        printf("Hardware TX buffer is ready. Writing payload to DATA register...\n");
        SIM_DATA_REG = 0x55;
        printf("Payload written: 0x%02X\n", SIM_DATA_REG);
    }

    return 0;
}
