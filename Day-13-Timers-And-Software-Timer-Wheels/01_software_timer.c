/*
 * ============================================================================
 * Problem: Non-Blocking Software Timer Wheel in C99
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

typedef struct {
    uint32_t start_tick;
    uint32_t interval_ms;
    bool is_active;
} sw_timer_t;

static bool sw_timer_is_expired(sw_timer_t *timer, uint32_t now_tick)
{
    if (!timer->is_active) return false;
    /* Unsigned subtraction safely handles 32-bit integer overflow roll-over */
    if ((now_tick - timer->start_tick) >= timer->interval_ms) {
        timer->start_tick = now_tick; /* Auto-reload */
        return true;
    }
    return false;
}

int main(void)
{
    printf("=== Day 13: Non-Blocking Software Timer Demonstration ===\n\n");

    sw_timer_t led_timer = {.start_tick = 0, .interval_ms = 500, .is_active = true};

    /* Simulate elapsed clock ticks */
    for (uint32_t now = 0; now <= 1500; now += 250) {
        printf("Time = %4u ms: ", now);
        if (sw_timer_is_expired(&led_timer, now)) {
            printf("[EVENT] 500ms Timer Expired! Toggling LED.\n");
        } else {
            printf("Idle.\n");
        }
    }
    return 0;
}
