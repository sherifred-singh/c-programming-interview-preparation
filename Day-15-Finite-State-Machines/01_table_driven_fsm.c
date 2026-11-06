/*
 * ============================================================================
 * Problem: Table-Driven Finite State Machine (FSM)
 * ============================================================================
 */

#include <stdio.h>

typedef enum { STATE_IDLE, STATE_RUNNING, STATE_FAULT, STATE_COUNT } state_t;
typedef enum { EVENT_START, EVENT_STOP, EVENT_FAULT_TRIP, EVENT_RESET, EVENT_COUNT } event_t;

static const state_t transition_table[STATE_COUNT][EVENT_COUNT] = {
    [STATE_IDLE]    = { [EVENT_START] = STATE_RUNNING, [EVENT_FAULT_TRIP] = STATE_FAULT },
    [STATE_RUNNING] = { [EVENT_STOP]  = STATE_IDLE,    [EVENT_FAULT_TRIP] = STATE_FAULT },
    [STATE_FAULT]   = { [EVENT_RESET] = STATE_IDLE }
};

static state_t dispatch_event(state_t current, event_t evt)
{
    state_t next = transition_table[current][evt];
    return next;
}

int main(void)
{
    printf("=== Day 15: Table-Driven FSM Dispatch ===\n\n");
    state_t s = STATE_IDLE;
    printf("Initial State: IDLE\n");

    s = dispatch_event(s, EVENT_START);
    printf("Event START -> Next State: %s\n", (s == STATE_RUNNING) ? "RUNNING" : "OTHER");

    s = dispatch_event(s, EVENT_FAULT_TRIP);
    printf("Event FAULT -> Next State: %s\n", (s == STATE_FAULT) ? "FAULT" : "OTHER");

    s = dispatch_event(s, EVENT_RESET);
    printf("Event RESET -> Next State: %s\n", (s == STATE_IDLE) ? "IDLE" : "OTHER");

    return 0;
}
