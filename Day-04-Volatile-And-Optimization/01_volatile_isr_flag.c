/*
 * ============================================================================
 * Problem: Volatile Shared Flag Between Interrupt Service Routine (ISR) and Main
 * 
 * Embedded Hardware Insight:
 *   When the compiler optimizes code at -O2 or -O3, it assumes variables in RAM
 *   do not change unless modified within the current thread of execution.
 *   If a flag is polled in a loop:
 *       while (!g_event_flag);
 *   The compiler optimizes this into:
 *       LDR R0, [g_event_flag]
 *   .loop:
 *       CMP R0, #0
 *       BEQ .loop   <-- Reads from CPU register R0 forever! The loop hangs!
 *   Declaring 'volatile bool g_event_flag;' forces an LDR from RAM on EVERY iteration.
 * 
 * Complexity:
 *   - Time Complexity: O(1) loop polling.
 *   - Space Complexity: O(1) in RAM (.data / .bss section).
 * 
 * Follow-Up Question:
 *   Q: Does 'volatile' make an operation atomic?
 *   A: NO! 'volatile' only guarantees physical memory reads and writes.
 *      Operations like 'g_counter++' still require 3 instructions (read, modify, write)
 *      and can still suffer race conditions without atomic instructions or critical sections.
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

/* Global flag shared between simulated ISR and main thread */
static volatile bool g_data_ready = false;
static volatile uint16_t g_adc_raw_value = 0U;

/* Simulated Hardware Timer / ADC Interrupt Service Routine */
void ADC_IRQHandler(void)
{
    /* In real hardware, this executes upon ADC Conversion Complete interrupt */
    g_adc_raw_value = 2048U; /* e.g. 1.65V mid-scale on 12-bit ADC */
    g_data_ready = true;     /* Signal main loop */
}

int main(void)
{
    printf("=== Day 04: Volatile Shared ISR Flag Demonstration ===\n\n");

    printf("1. Initial state: g_data_ready = %s\n", g_data_ready ? "TRUE" : "FALSE");
    printf("2. Waiting for ADC conversion to complete...\n");

    /* Simulate hardware triggering the interrupt after some elapsed cycles */
    ADC_IRQHandler();

    /* Main loop polls the volatile flag */
    if (g_data_ready) {
        printf("3. ISR Event Detected! ADC Reading: %u counts (%.2f V)\n",
               g_adc_raw_value, (g_adc_raw_value * 3.3f) / 4095.0f);
        
        /* Acknowledge event */
        g_data_ready = false;
        printf("4. Flag acknowledged and cleared.\n");
    }

    return 0;
}
