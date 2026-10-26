"""
Curriculum definitions for Days 11 through 20.
"""

DAYS_11_TO_20 = {
    11: {
        "folder_name": "Day-11-SPI-Modes-And-Sensor-Interfacing",
        "title": "Day 11: SPI Bus Modes (0–3) & Sensor Interfacing",
        "overview": "Understanding CPOL/CPHA timing diagrams for SPI Modes 0, 1, 2, and 3, and PT100 RTD 3-wire bridge compensation.",
        "programs": [
            {
                "filename": "01_spi_mode_config.c",
                "focus": "SPI CPOL and CPHA Mode Configuration Matrix",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "Mode 0 (CPOL=0, CPHA=0) captures data on the rising clock edge while idle low. Mode 3 (CPOL=1, CPHA=1) captures on rising edge while idle high.",
                "follow_up_q": "Why is a 33-ohm series damping resistor placed on SPI lines?",
                "follow_up_a": "High-speed SPI clock signals (>10 MHz) cause ringing and overshoot due to trace inductance. The 33-ohm resistor absorbs reflections and protects inputs.",
                "code": r'''/*
 * ============================================================================
 * Problem: SPI Bus Mode Configuration & Edge Timing Simulator
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>

typedef enum {
    SPI_MODE_0 = 0, /* CPOL = 0, CPHA = 0: Idle Low,  Sample on Rising  */
    SPI_MODE_1 = 1, /* CPOL = 0, CPHA = 1: Idle Low,  Sample on Falling */
    SPI_MODE_2 = 2, /* CPOL = 1, CPHA = 0: Idle High, Sample on Falling */
    SPI_MODE_3 = 3  /* CPOL = 1, CPHA = 1: Idle High, Sample on Rising  */
} spi_mode_t;

static void print_spi_mode_details(spi_mode_t mode)
{
    uint8_t cpol = (mode >> 1) & 1;
    uint8_t cpha = mode & 1;

    printf("Mode %d: CPOL=%d (%s), CPHA=%d (%s)\n",
           mode, cpol, cpol ? "Idle HIGH" : "Idle LOW",
           cpha, cpha ? "Sample 2nd Edge" : "Sample 1st Edge");
}

int main(void)
{
    printf("=== Day 11: SPI Bus Modes (0-3) Timing Matrix ===\n\n");
    for (int m = 0; m <= 3; m++) {
        print_spi_mode_details((spi_mode_t)m);
    }
    return 0;
}
'''
            }
        ]
    },
    12: {
        "folder_name": "Day-12-ADC-Digital-Filtering",
        "title": "Day 12: ADC Mechanics, Calibration & Digital Filters",
        "overview": "Fixed-point Q8 Exponential Moving Average (EMA) and Median-3 filter implementations to reject electrical noise without floating-point FPU overhead.",
        "programs": [
            {
                "filename": "01_fixed_point_ema_filter.c",
                "focus": "Integer-Only Q8 Fixed-Point EMA Filter",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "Floating-point math on MCUs without hardware FPU bloats code with emulation routines. Fixed-point division by 256 is a 1-cycle bit-shift (>> 8).",
                "follow_up_q": "How do you choose alpha in an EMA filter?",
                "follow_up_a": "A smaller alpha gives stronger high-frequency noise smoothing but introduces lag. A larger alpha tracks rapid signal changes with less delay.",
                "code": r'''/*
 * ============================================================================
 * Problem: Fixed-Point Exponential Moving Average (EMA) Digital Filter
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>

/* State: State[n] = (alpha * Sample + (256 - alpha) * State[n-1]) >> 8 */
#define EMA_ALPHA 51U /* ~20% smoothing factor (51 / 256) */

static uint16_t ema_filter(uint16_t raw_sample, uint32_t *state)
{
    *state = ((uint32_t)raw_sample * EMA_ALPHA) + (*state * (256U - EMA_ALPHA));
    *state >>= 8U;
    return (uint16_t)(*state);
}

int main(void)
{
    printf("=== Day 12: Fixed-Point Q8 EMA Filter Simulation ===\n\n");

    uint32_t filter_state = 1000U;
    uint16_t noisy_inputs[] = {1000, 1050, 980, 1200, 1020, 1010, 990};

    printf("Raw Input -> Filtered Output:\n");
    for (size_t i = 0; i < sizeof(noisy_inputs)/sizeof(noisy_inputs[0]); i++) {
        uint16_t out = ema_filter(noisy_inputs[i], &filter_state);
        printf(" [%zu]: Raw = %4u  | Filtered = %4u\n", i, noisy_inputs[i], out);
    }
    return 0;
}
'''
            }
        ]
    },
    13: {
        "folder_name": "Day-13-Timers-And-Software-Timer-Wheels",
        "title": "Day 13: Hardware Timers & Non-Blocking Software Timer Wheels",
        "overview": "Non-blocking tick-based software timer arrays eliminating delay loops in embedded firmware.",
        "programs": [
            {
                "filename": "01_software_timer.c",
                "focus": "Non-Blocking Tick List Software Timer Engine",
                "time_complexity": "O(N) timer check",
                "space_complexity": "O(N) timer structs",
                "insight": "Calling delay_ms() halts the CPU and starves communication protocols. Software timers decouple timekeeping from execution.",
                "follow_up_q": "How do you handle 32-bit tick counter roll-over in software timers?",
                "follow_up_a": "Always use unsigned subtraction: '(current_tick - start_tick) >= period'. In unsigned modulo arithmetic, subtraction works correctly across roll-over.",
                "code": r'''/*
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
'''
            }
        ]
    },
    14: {
        "folder_name": "Day-14-Silicon-Bring-Up-Diagnostics",
        "title": "Day 14: Silicon Bring-Up & Board Diagnostics",
        "overview": "The senior 5-step board bring-up sequence: cold resistance inspection, current-limited power up, crystal verification, and SWD connection.",
        "programs": [
            {
                "filename": "01_board_bringup_checklist.c",
                "focus": "Deterministic 5-Step Bring-Up State Verification",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "Never power a prototype board directly from mains or an unconstrained battery; always set current limits to 50mA to prevent silicon destruction.",
                "follow_up_q": "What is the very first thing you check when a newly assembled PCB doesn't enumerate on SWD?",
                "follow_up_a": "Check VDD/GND voltages, reset pin voltage (must be high for active-low NRST), and verify crystal oscillation with a 10x oscilloscope probe.",
                "code": r'''/*
 * ============================================================================
 * Problem: 5-Step Hardware Board Bring-Up Sequence
 * ============================================================================
 */

#include <stdio.h>
#include <stdbool.h>

typedef struct {
    bool visual_microscope_pass;
    bool cold_resistance_ok;      /* > 10 kOhm VDD to GND */
    bool current_limit_50ma_safe; /* Consumes < 50mA */
    bool crystal_osc_verified;    /* Clock frequency verified on scope */
    bool swd_debugger_locked;     /* SWD IDCODE read */
} board_bringup_t;

static bool verify_board_health(const board_bringup_t *check)
{
    if (!check->visual_microscope_pass) { printf("FAIL: Solder bridge or polarity reverse detected!\n"); return false; }
    if (!check->cold_resistance_ok)      { printf("FAIL: Short circuit detected on VDD rail!\n"); return false; }
    if (!check->current_limit_50ma_safe) { printf("FAIL: Excessive current draw (>50mA)!\n"); return false; }
    if (!check->crystal_osc_verified)    { printf("FAIL: Oscillator not oscillating!\n"); return false; }
    if (!check->swd_debugger_locked)     { printf("FAIL: SWD cannot read MCU IDCODE!\n"); return false; }
    return true;
}

int main(void)
{
    printf("=== Day 14: 5-Step Silicon Bring-Up Diagnostics ===\n\n");
    board_bringup_t board = {true, true, true, true, true};
    if (verify_board_health(&board)) {
        printf("SUCCESS: Board Bring-Up Complete. Ready for Firmware Flashing!\n");
    }
    return 0;
}
'''
            }
        ]
    },
    15: {
        "folder_name": "Day-15-Finite-State-Machines",
        "title": "Day 15: Finite State Machines (FSM)",
        "overview": "Table-driven transition matrices vs switch-case FSMs for deterministic industrial sequencers and safety controllers.",
        "programs": [
            {
                "filename": "01_table_driven_fsm.c",
                "focus": "Table-Driven Finite State Machine in C99",
                "time_complexity": "O(1) transition lookup",
                "space_complexity": "O(States x Events) in Flash",
                "insight": "Table-driven FSMs eliminate deeply nested switch statements and guarantee constant O(1) transition dispatch time.",
                "follow_up_q": "When is switch-case preferred over a table-driven FSM?",
                "follow_up_a": "When the transition matrix is sparse (few events per state), switch-case saves Flash memory by avoiding empty table entries.",
                "code": r'''/*
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
'''
            }
        ]
    },
    16: {
        "folder_name": "Day-16-Memory-Pools-Heap-Avoidance",
        "title": "Day 16: Memory Pools & Dynamic Heap Avoidance",
        "overview": "Fixed-size block allocators preventing heap fragmentation in long-running mission-critical firmware.",
        "programs": [
            {
                "filename": "01_fixed_block_pool.c",
                "focus": "Fixed-Size Block Allocator (Deterministic malloc/free Alternative)",
                "time_complexity": "O(1) allocation and free",
                "space_complexity": "O(N) static memory pool",
                "insight": "MISRA-C Rule 21.3 bans dynamic heap allocation because fragmentation causes unpredictable allocation failures after weeks of operation.",
                "follow_up_q": "How does a fixed-block memory pool achieve O(1) allocation time?",
                "follow_up_a": "It maintains a singly linked list of free blocks in a static array. Allocation simply pops the head of the free list in O(1) time.",
                "code": r'''/*
 * ============================================================================
 * Problem: Static Fixed-Size Block Memory Pool
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define BLOCK_SIZE  32U
#define BLOCK_COUNT 4U

typedef struct Block {
    struct Block *next;
} block_t;

static uint8_t s_memory_pool[BLOCK_COUNT * BLOCK_SIZE];
static block_t *s_free_list_head = NULL;

static void pool_init(void)
{
    s_free_list_head = (block_t *)&s_memory_pool[0];
    block_t *curr = s_free_list_head;
    for (size_t i = 1; i < BLOCK_COUNT; i++) {
        curr->next = (block_t *)&s_memory_pool[i * BLOCK_SIZE];
        curr = curr->next;
    }
    curr->next = NULL;
}

static void *pool_alloc(void)
{
    if (!s_free_list_head) return NULL; /* Out of memory */
    void *ptr = s_free_list_head;
    s_free_list_head = s_free_list_head->next;
    return ptr;
}

static void pool_free(void *ptr)
{
    if (!ptr) return;
    block_t *block = (block_t *)ptr;
    block->next = s_free_list_head;
    s_free_list_head = block;
}

int main(void)
{
    printf("=== Day 16: Fixed-Size Block Memory Pool ===\n\n");
    pool_init();

    void *b1 = pool_alloc();
    void *b2 = pool_alloc();
    printf("Allocated Block 1 at %p\n", b1);
    printf("Allocated Block 2 at %p\n", b2);

    pool_free(b1);
    printf("Freed Block 1.\n");

    void *b3 = pool_alloc();
    printf("Re-allocated Block 3 at %p (Reused freed block in O(1)!)\n", b3);

    return 0;
}
'''
            }
        ]
    },
    17: {
        "folder_name": "Day-17-Zero-Copy-Packet-Parsing",
        "title": "Day 17: String & Packet Parsing without Heap",
        "overview": "Zero-copy reentrant packet tokenization (strtok_r) for telemetry commands like 'R2,AUTO,1,120'.",
        "programs": [
            {
                "filename": "01_packet_parser.c",
                "focus": "In-Place Reentrant Telemetry Parser",
                "time_complexity": "O(N) linear scan",
                "space_complexity": "O(1) zero heap",
                "insight": "Standard strtok() uses a global static pointer, making it unsafe for multi-threaded or interrupt environments. Always use strtok_r()!",
                "follow_up_q": "Why does strtok_r() modify the source string?",
                "follow_up_a": "It inserts null-terminators ('\\0') in place of delimiters to allow zero-copy string references without allocating new memory.",
                "code": r'''/*
 * ============================================================================
 * Problem: Zero-Heap Packet Tokenization
 * ============================================================================
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static void parse_relay_command(char *packet)
{
    char *saveptr = NULL;
    char *token = strtok_r(packet, ",", &saveptr);
    if (!token) return;

    printf(" - Relay ID : %s\n", token);

    token = strtok_r(NULL, ",", &saveptr);
    if (token) printf(" - Mode     : %s\n", token);

    token = strtok_r(NULL, ",", &saveptr);
    if (token) printf(" - State    : %s\n", token);

    token = strtok_r(NULL, ",", &saveptr);
    if (token) printf(" - Delay (s): %s\n", token);
}

int main(void)
{
    printf("=== Day 17: Reentrant Zero-Copy Packet Tokenizer ===\n\n");
    char cmd[] = "R2,AUTO,1,120";
    printf("Parsing command string: \"%s\"\n", cmd);
    parse_relay_command(cmd);
    return 0;
}
'''
            }
        ]
    },
    18: {
        "folder_name": "Day-18-FreeRTOS-Task-Mechanics",
        "title": "Day 18: FreeRTOS Task Mechanics & TCB",
        "overview": "Understanding FreeRTOS Task Control Blocks (TCB), task priorities, preemptive scheduling, and stack watermarking.",
        "programs": [
            {
                "filename": "01_task_state_machine.c",
                "focus": "Task State Architecture (Running, Ready, Blocked, Suspended)",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "In FreeRTOS, tasks in the Blocked state consume 0% CPU time while awaiting a timer or event.",
                "follow_up_q": "How does uxTaskGetStackHighWaterMark() detect stack overflow?",
                "follow_up_a": "At creation, FreeRTOS fills task stack memory with a known byte pattern (0xA5). High water mark checks how many 0xA5 bytes remain untouched.",
                "code": r'''/*
 * ============================================================================
 * Problem: FreeRTOS Task State Transitions Simulator
 * ============================================================================
 */

#include <stdio.h>

typedef enum { TASK_RUNNING, TASK_READY, TASK_BLOCKED, TASK_SUSPENDED } task_state_t;

int main(void)
{
    printf("=== Day 18: FreeRTOS Task State Lifecycle ===\n\n");
    task_state_t state = TASK_READY;
    printf("Task Created -> State: READY\n");

    state = TASK_RUNNING;
    printf("Scheduler Dispatches -> State: RUNNING\n");

    state = TASK_BLOCKED;
    printf("Task calls vTaskDelay(100) -> State: BLOCKED (0%% CPU used)\n");

    state = TASK_READY;
    printf("Delay Expired -> State: READY (Awaiting CPU allocation)\n");

    return 0;
}
'''
            }
        ]
    },
    19: {
        "folder_name": "Day-19-FreeRTOS-Mutex-Vs-Semaphore",
        "title": "Day 19: FreeRTOS Synchronization: Mutex vs Semaphore",
        "overview": "Deep dive into Priority Inversion, Priority Inheritance protocol, Mutex ownership rules, and Binary Semaphores for task signaling.",
        "programs": [
            {
                "filename": "01_priority_inversion.c",
                "focus": "Priority Inversion and Priority Inheritance Demonstration",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "A Mutex has ownership and implements Priority Inheritance. A Binary Semaphore has NO ownership and does NOT prevent priority inversion!",
                "follow_up_q": "Can a Mutex be unlocked by an ISR?",
                "follow_up_a": "NO! A mutex can only be released by the specific task that acquired it. Semaphores, however, can be signaled from an ISR.",
                "code": r'''/*
 * ============================================================================
 * Problem: Priority Inversion & Inheritance Explanation
 * ============================================================================
 */

#include <stdio.h>

int main(void)
{
    printf("=== Day 19: Priority Inversion vs Inheritance ===\n\n");
    printf("Priority Inversion Hazard:\n");
    printf(" 1. Low-Priority Task (L) takes Shared Resource Mutex.\n");
    printf(" 2. High-Priority Task (H) preempts L and blocks waiting for Mutex.\n");
    printf(" 3. Medium-Priority Task (M) wakes up and preempts L indefinitely.\n");
    printf(" -> Result: H is starved by M! (Classic Mars Pathfinder bug).\n\n");

    printf("Solution: Priority Inheritance Protocol:\n");
    printf(" When H blocks on Mutex held by L, FreeRTOS temporarily boosts L's priority to match H!\n");
    printf(" This prevents M from preempting L until L releases the Mutex.\n");

    return 0;
}
'''
            }
        ]
    },
    20: {
        "folder_name": "Day-20-FreeRTOS-Queues-And-ISR-Rules",
        "title": "Day 20: FreeRTOS Queues & ISR Context Rules",
        "overview": "The mandatory '...FromISR' API rule, deferred interrupt processing (bottom halves), and xHigherPriorityTaskWoken context switches.",
        "programs": [
            {
                "filename": "01_queue_from_isr_pattern.c",
                "focus": "xQueueSendFromISR and Deferred Interrupt Processing Pattern",
                "time_complexity": "O(1)",
                "space_complexity": "O(N) queue storage",
                "insight": "Never call blocking FreeRTOS APIs (e.g. xQueueSend) inside an ISR. Always use the non-blocking FromISR variant with portYIELD_FROM_ISR().",
                "follow_up_q": "What does xHigherPriorityTaskWoken do?",
                "follow_up_a": "If sending to the queue unblocks a task with a higher priority than the currently running task, it triggers an immediate context switch at the end of the ISR.",
                "code": r'''/*
 * ============================================================================
 * Problem: FreeRTOS FromISR Pattern & Deferred Processing
 * ============================================================================
 */

#include <stdio.h>
#include <stdbool.h>

static void UART_ISR_Simulated(void)
{
    bool xHigherPriorityTaskWoken = false;
    printf("1. UART Byte Arrived in Hardware ISR.\n");
    printf("2. Calling xQueueSendFromISR(&uart_queue, &byte, &xHigherPriorityTaskWoken)...\n");

    xHigherPriorityTaskWoken = true; /* Higher priority worker unblocked */

    if (xHigherPriorityTaskWoken) {
        printf("3. portYIELD_FROM_ISR() invoked -> Immediate Context Switch to Processing Task!\n");
    }
}

int main(void)
{
    printf("=== Day 20: FreeRTOS ISR Context Rules ===\n\n");
    UART_ISR_Simulated();
    return 0;
}
'''
            }
        ]
    }
}
