/*
 * ============================================================================
 * Problem: Lock-Free SPSC Circular Ring Buffer for UART ISR
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define RING_BUF_SIZE 16U /* Must be power of 2 */
#define RING_BUF_MASK (RING_BUF_SIZE - 1U)

typedef struct {
    uint8_t buffer[RING_BUF_SIZE];
    volatile uint8_t head; /* Written by Producer (ISR) */
    volatile uint8_t tail; /* Written by Consumer (Main) */
} ring_buffer_t;

static void ring_buf_init(ring_buffer_t *rb) {
    rb->head = 0;
    rb->tail = 0;
}

static bool ring_buf_push(ring_buffer_t *rb, uint8_t data) {
    uint8_t next_head = (rb->head + 1U) & RING_BUF_MASK;
    if (next_head == rb->tail) {
        return false; /* Buffer Full - Drop or Flag Overflow */
    }
    rb->buffer[rb->head] = data;
    rb->head = next_head;
    return true;
}

static bool ring_buf_pop(ring_buffer_t *rb, uint8_t *data) {
    if (rb->head == rb->tail) {
        return false; /* Buffer Empty */
    }
    *data = rb->buffer[rb->tail];
    rb->tail = (rb->tail + 1U) & RING_BUF_MASK;
    return true;
}

int main(void)
{
    printf("=== Day 08: Lock-Free SPSC Ring Buffer for UART ===\n\n");

    ring_buffer_t rx_queue;
    ring_buf_init(&rx_queue);

    /* Producer: Push 5 bytes */
    for (uint8_t b = 0xA1; b <= 0xA5; b++) {
        ring_buf_push(&rx_queue, b);
        printf("Pushed: 0x%02X\n", b);
    }

    /* Consumer: Pop all bytes */
    uint8_t byte_out = 0;
    printf("\nReading from buffer:\n");
    while (ring_buf_pop(&rx_queue, &byte_out)) {
        printf("Popped: 0x%02X\n", byte_out);
    }

    return 0;
}
