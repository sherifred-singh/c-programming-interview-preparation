/*
 * ============================================================================
 * Problem: Interrupt Vector Table (IVT) Architecture & Dispatch Simulator
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>

typedef void (*isr_handler_t)(void);

static void SysTick_Handler(void) {
    printf(" -> [ISR 15]: SysTick 1ms Kernel Tick Executed\n");
}

static void USART1_IRQHandler(void) {
    printf(" -> [ISR 37]: USART1 RX Byte Received & Staged\n");
}

static void EXTI0_IRQHandler(void) {
    printf(" -> [ISR 06]: External Pin E-Stop Tripped!\n");
}

/* Simulated Vector Table in Flash (.text) */
static const isr_handler_t g_vector_table[] = {
    [0]  = SysTick_Handler,
    [1]  = USART1_IRQHandler,
    [2]  = EXTI0_IRQHandler
};

int main(void)
{
    printf("=== Day 06: Interrupt Vector Table Dispatch Simulation ===\n\n");

    printf("1. Triggering SysTick Interrupt:\n");
    g_vector_table[0]();

    printf("\n2. Triggering USART1 Interrupt:\n");
    g_vector_table[1]();

    printf("\n3. Triggering EXTI0 Emergency Stop Interrupt:\n");
    g_vector_table[2]();

    return 0;
}
