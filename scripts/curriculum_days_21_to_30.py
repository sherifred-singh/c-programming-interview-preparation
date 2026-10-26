"""
Curriculum definitions for Days 21 through 30.
"""

DAYS_21_TO_30 = {
    21: {
        "folder_name": "Day-21-Safety-Interlocks-Architecture",
        "title": "Day 21: System Architecture & Safety Interlocks",
        "overview": "Break-before-make interlocking delays, capacitive power-failure brownout flushes, and hardware fault latches.",
        "programs": [
            {
                "filename": "01_break_before_make.c",
                "focus": "Break-Before-Make Contact Interlocking State Machine",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "When switching high-power contactors (e.g. Mains to Generator), an uncommanded overlapping arc causes a dead phase-to-phase short. Enforce a 2.0s dead-time delay!",
                "follow_up_q": "Why is software interlocking insufficient without hardware interlocking?",
                "follow_up_a": "Software can crash or hang if MCU clock stops. Safety-critical systems require electrical hardware interlocks (mechanical auxiliary contacts) backing software logic.",
                "code": r'''/*
 * ============================================================================
 * Problem: Break-Before-Make Relay Interlocking Controller
 * ============================================================================
 */

#include <stdio.h>
#include <stdbool.h>

typedef enum { RELAY_MAINS, RELAY_GENERATOR, RELAY_ALL_OFF } power_source_t;

static void switch_power_source(power_source_t target)
{
    printf("1. De-energizing all active contactors...\n");
    printf("2. Enforcing 2.0-second break-before-make dead-time arc suppression delay...\n");
    printf("3. Verifying auxiliary hardware feedback confirms contacts are physically OPEN...\n");

    if (target == RELAY_GENERATOR) {
        printf("4. Safely energizing Generator Contactor.\n");
    } else {
        printf("4. Safely energizing Mains Contactor.\n");
    }
}

int main(void)
{
    printf("=== Day 21: Break-Before-Make Interlocking Controller ===\n\n");
    switch_power_source(RELAY_GENERATOR);
    return 0;
}
'''
            }
        ]
    },
    22: {
        "folder_name": "Day-22-Bootloader-And-Vector-Relocation",
        "title": "Day 22: Bootloader Fundamentals & Vector Relocation",
        "overview": "Dual-slot Flash partition layouts, vector table offset register (SCB->VTOR), and safe application jump routines.",
        "programs": [
            {
                "filename": "01_bootloader_jump_simulation.c",
                "focus": "Vector Table Relocation (SCB->VTOR) & Application Jump",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "Before jumping to user application from bootloader: disable all interrupts, clear pending flags, relocate VTOR, and load Application MSP.",
                "follow_up_q": "Why does a bootloader jump crash if interrupts are left enabled?",
                "follow_up_a": "An enabled peripheral interrupt will vector through the bootloader's old IVT in low Flash instead of the application's IVT, triggering an unhandled exception.",
                "code": r'''/*
 * ============================================================================
 * Problem: Bootloader to Application Jump Sequence Simulation
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>

#define APP_START_ADDRESS 0x08008000U /* Sector 2 Flash */

typedef void (*app_entry_t)(void);

static void simulate_bootloader_jump(uint32_t app_base_addr)
{
    printf("1. Verifying application integrity (CRC check passed)...\n");
    printf("2. Disabling all peripheral interrupts (__disable_irq())...\n");
    printf("3. Relocating Vector Table Offset Register: SCB->VTOR = 0x%08X\n", app_base_addr);
    printf("4. Setting Main Stack Pointer (MSP) to *(uint32_t *)0x%08X\n", app_base_addr);
    printf("5. Fetching Reset Handler address from *(uint32_t *)(0x%08X + 4)\n", app_base_addr);
    printf("6. Branching to application reset handler!\n");
}

int main(void)
{
    printf("=== Day 22: Bootloader Jump & Vector Relocation ===\n\n");
    simulate_bootloader_jump(APP_START_ADDRESS);
    return 0;
}
'''
            }
        ]
    },
    23: {
        "folder_name": "Day-23-Watchdogs-And-Brownout-Reset",
        "title": "Day 23: Watchdog Timers & Brown-Out Reset (BOR)",
        "overview": "Independent Watchdog (IWDG) vs Window Watchdog (WWDG) and handling supply brown-out voltage events.",
        "programs": [
            {
                "filename": "01_window_watchdog_simulator.c",
                "focus": "Window Watchdog (WWDG) Timing Window Validation",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "An independent watchdog only catches deadlocks (too late). A window watchdog catches software running too fast (erratic branch or loop skip).",
                "follow_up_q": "Why does kicking a WWDG too early trigger an immediate MCU reset?",
                "follow_up_a": "WWDG enforces both an upper and lower time limit. Kicking before the window opens indicates runaway program counter execution.",
                "code": r'''/*
 * ============================================================================
 * Problem: Window Watchdog (WWDG) Refresh Window Checker
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define WWDG_WINDOW_MIN_MS 20U
#define WWDG_WINDOW_MAX_MS 80U

static bool wwdg_feed(uint32_t elapsed_since_last_feed_ms)
{
    if (elapsed_since_last_feed_ms < WWDG_WINDOW_MIN_MS) {
        printf("RESET: WWDG fed too early (%u ms < %u ms)! Software runaway!\n",
               elapsed_since_last_feed_ms, WWDG_WINDOW_MIN_MS);
        return false;
    }
    if (elapsed_since_last_feed_ms > WWDG_WINDOW_MAX_MS) {
        printf("RESET: WWDG fed too late (%u ms > %u ms)! CPU hung!\n",
               elapsed_since_last_feed_ms, WWDG_WINDOW_MAX_MS);
        return false;
    }
    printf("OK: WWDG fed cleanly within legal window (%u ms).\n", elapsed_since_last_feed_ms);
    return true;
}

int main(void)
{
    printf("=== Day 23: Window Watchdog (WWDG) Simulator ===\n\n");
    wwdg_feed(10); /* Too early */
    wwdg_feed(50); /* Valid */
    wwdg_feed(95); /* Too late */
    return 0;
}
'''
            }
        ]
    },
    24: {
        "folder_name": "Day-24-DMA-Ping-Pong-Buffering",
        "title": "Day 24: Direct Memory Access (DMA) & Double Buffering",
        "overview": "Ping-pong double-buffering architecture allowing CPU processing on Buffer A while DMA controller fills Buffer B.",
        "programs": [
            {
                "filename": "01_ping_pong_dma.c",
                "focus": "Ping-Pong Double Buffering Data Engine",
                "time_complexity": "O(1) buffer switch",
                "space_complexity": "O(2N) dual buffers",
                "insight": "Double buffering eliminates data corruption and CPU busy-wait loops during high-speed ADC sampling or audio processing.",
                "follow_up_q": "What is the role of Half-Transfer (HT) interrupt in circular DMA?",
                "follow_up_a": "In circular DMA, the Half-Transfer interrupt signals the first half of the buffer is ready for CPU processing, while Transfer-Complete signals the second half is ready.",
                "code": r'''/*
 * ============================================================================
 * Problem: DMA Ping-Pong Double Buffering Controller
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>

#define BUF_SIZE 8U

typedef struct {
    uint16_t buffer_a[BUF_SIZE];
    uint16_t buffer_b[BUF_SIZE];
    volatile uint8_t active_dma_buf; /* 0: Filling A, 1: Filling B */
} ping_pong_t;

static void process_buffer(const uint16_t *buf, const char *name)
{
    printf(" -> CPU Processing %s: Sum = ", name);
    uint32_t sum = 0;
    for (size_t i = 0; i < BUF_SIZE; i++) sum += buf[i];
    printf("%u\n", sum);
}

int main(void)
{
    printf("=== Day 24: Ping-Pong DMA Buffer Engine ===\n\n");
    ping_pong_t pp = {.active_dma_buf = 0};

    /* Fill buffer A */
    for (size_t i = 0; i < BUF_SIZE; i++) pp.buffer_a[i] = 100;
    printf("DMA finished filling Buffer A -> Triggering Half-Transfer ISR...\n");
    process_buffer(pp.buffer_a, "Buffer A");

    /* Fill buffer B */
    for (size_t i = 0; i < BUF_SIZE; i++) pp.buffer_b[i] = 200;
    printf("\nDMA finished filling Buffer B -> Triggering Transfer-Complete ISR...\n");
    process_buffer(pp.buffer_b, "Buffer B");

    return 0;
}
'''
            }
        ]
    },
    25: {
        "folder_name": "Day-25-CAN-Bus-Acceptance-Filtering",
        "title": "Day 25: CAN 2.0B Controller & Automotive Telemetry",
        "overview": "Standard 11-bit vs Extended 29-bit CAN IDs, 32-bit hardware acceptance mask filtering, and bus-off recovery states.",
        "programs": [
            {
                "filename": "01_can_filter_mask.c",
                "focus": "Hardware CAN Acceptance Filter & Mask Logic Simulator",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "Hardware acceptance filtering ensures only relevant CAN packets wake up or interrupt the MCU, saving significant CPU load on high-traffic buses.",
                "follow_up_q": "What is the difference between Filter ID and Filter Mask?",
                "follow_up_a": "The Mask defines which bit positions must be checked ('1' = must match, '0' = don't care). The ID defines the required bit values for those checked positions.",
                "code": r'''/*
 * ============================================================================
 * Problem: CAN Hardware Acceptance Filter & Mask Simulation
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

static bool can_filter_accepts(uint32_t rx_id, uint32_t filter_id, uint32_t mask)
{
    return ((rx_id & mask) == (filter_id & mask));
}

int main(void)
{
    printf("=== Day 25: CAN 2.0B Hardware Acceptance Filter Simulator ===\n\n");

    /* Target: Accept only Engine ECU CAN IDs: 0x7E0 to 0x7E7 (Mask 0x7F8) */
    uint32_t filter_id = 0x7E0;
    uint32_t mask      = 0x7F8;

    uint32_t test_ids[] = {0x7E0, 0x7E2, 0x7E7, 0x7E8, 0x123};

    for (size_t i = 0; i < sizeof(test_ids)/sizeof(test_ids[0]); i++) {
        uint32_t id = test_ids[i];
        bool accept = can_filter_accepts(id, filter_id, mask);
        printf("CAN ID 0x%03X -> %s\n", id, accept ? "ACCEPTED by Silicon Hardware" : "REJECTED (No CPU Interruption)");
    }

    return 0;
}
'''
            }
        ]
    },
    26: {
        "folder_name": "Day-26-Low-Power-Modes-And-Wakeup",
        "title": "Day 26: Low-Power Modes & Power Management",
        "overview": "Sleep, Stop, and Standby mode state machines, peripheral clock gating, and RTC alarm wake-up events.",
        "programs": [
            {
                "filename": "01_low_power_manager.c",
                "focus": "Low-Power Architecture (Sleep vs Stop vs Standby)",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "In Stop mode, high-speed clocks are gated, but SRAM and registers are preserved. Standby mode shuts off SRAM (equivalent to cold boot on wake).",
                "follow_up_q": "Why must unassigned GPIO pins never be left floating in battery-operated devices?",
                "follow_up_a": "Floating CMOS input pins drift between logic 0 and 1, causing both internal transistors to conduct simultaneously (shoot-through current), wasting microamps.",
                "code": r'''/*
 * ============================================================================
 * Problem: Low Power Architecture Modes
 * ============================================================================
 */

#include <stdio.h>

typedef enum { MODE_RUN, MODE_SLEEP, MODE_STOP, MODE_STANDBY } power_mode_t;

int main(void)
{
    printf("=== Day 26: Embedded Low-Power Architecture Comparison ===\n\n");
    printf("1. SLEEP MODE   : CPU core stopped, peripherals running. Fast wake (~1 us).\n");
    printf("2. STOP MODE    : All clocks stopped, SRAM/registers preserved. Wake via EXTI/RTC (~5 us).\n");
    printf("3. STANDBY MODE : Entire core unpowered, SRAM lost. Ultra-low leakage (<1 uA). Wake causes RESET.\n");
    return 0;
}
'''
            }
        ]
    },
    27: {
        "folder_name": "Day-27-Data-Integrity-CRC32-Checksums",
        "title": "Day 27: Data Integrity & Checksum Engines",
        "overview": "Fast table-driven CRC-32 (IEEE 802.3 Ethernet / Flash bootloader integrity) and XOR checksum frame validators.",
        "programs": [
            {
                "filename": "01_crc32_fast.c",
                "focus": "IEEE 802.3 CRC-32 Calculation for Flash Memory Integrity",
                "time_complexity": "O(N) message length",
                "space_complexity": "O(1)",
                "insight": "Hardware CRC engines in ARM Cortex-M compute 32-bit CRC in 1 CPU cycle per word. Software bitwise CRC is essential for portable fallback.",
                "follow_up_q": "Why is a simple additive checksum insufficient for firmware images?",
                "follow_up_a": "Additive checksums cannot detect byte order swapping (e.g., 0x01, 0x02 has the same sum as 0x02, 0x01) and have blind spots to bit-burst errors.",
                "code": r'''/*
 * ============================================================================
 * Problem: CRC-32 Calculation (IEEE 802.3 Polynomial 0xEDB88320)
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>

static uint32_t crc32_calculate(const uint8_t *data, size_t length)
{
    uint32_t crc = 0xFFFFFFFFU;
    for (size_t i = 0; i < length; i++) {
        crc ^= data[i];
        for (int b = 0; b < 8; b++) {
            crc = (crc >> 1) ^ (0xEDB88320U & -(int32_t)(crc & 1));
        }
    }
    return ~crc;
}

int main(void)
{
    printf("=== Day 27: CRC-32 Data Integrity Engine ===\n\n");
    uint8_t payload[] = "FIRMWARE_V1.0_IMAGE_HEADER";
    uint32_t crc = crc32_calculate(payload, sizeof(payload) - 1);
    printf("Payload String: \"%s\"\n", payload);
    printf("CRC-32 Result : 0x%08X\n", crc);
    return 0;
}
'''
            }
        ]
    },
    28: {
        "folder_name": "Day-28-MISRA-C-Safety-Defensive-Coding",
        "title": "Day 28: Defensive Programming & MISRA-C Safety",
        "overview": "Applying mandatory MISRA-C rules: explicit fixed-width types, side-effect avoidance in macros, and preventing arithmetic buffer overflows.",
        "programs": [
            {
                "filename": "01_misra_defensive_rules.c",
                "focus": "MISRA-C Compliance Patterns in Firmware",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "MISRA-C Rule 17.2 forbids recursion; Rule 11.4 forbids arbitrary pointer casting without explicit alignment and type safety.",
                "follow_up_q": "Why does MISRA-C require the 'default' case in all switch statements?",
                "follow_up_a": "Even if all enum values are handled, hardware memory corruption or electrical noise could corrupt the state variable. The default case handles illegal states safely.",
                "code": r'''/*
 * ============================================================================
 * Problem: MISRA-C Defensive Programming Guidelines
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

/* Safe bounded integer addition preventing overflow */
static bool safe_add_uint16(uint16_t a, uint16_t b, uint16_t *result)
{
    if (!result) return false;
    if (a > (UINT16_MAX - b)) {
        return false; /* Overflow detected safely without wrapping! */
    }
    *result = a + b;
    return true;
}

int main(void)
{
    printf("=== Day 28: MISRA-C Defensive Arithmetic Guard ===\n\n");

    uint16_t res = 0;
    if (safe_add_uint16(60000, 10000, &res)) {
        printf("Sum = %u\n", res);
    } else {
        printf("OVERFLOW PREVENTED: 60000 + 10000 exceeds 16-bit capacity (65535)!\n");
    }

    return 0;
}
'''
            }
        ]
    },
    29: {
        "folder_name": "Day-29-Live-Coding-Telemetry-Packet-Engine",
        "title": "Day 29: Live Coding Simulation: Telemetry Packet Engine",
        "overview": "Full 30-minute end-to-end coding test: frame builder, CRC calculation, and RS-485 byte stream serialization.",
        "programs": [
            {
                "filename": "01_telemetry_engine.c",
                "focus": "Full Telemetry Frame Encoder & Decoder Simulation",
                "time_complexity": "O(N) frame length",
                "space_complexity": "O(1) static buffer",
                "insight": "Senior technical interview coding rounds test full-stack ability: structuring a protocol header, calculating CRC, handling corrupt frames, and decoding safely.",
                "follow_up_q": "How do you detect a truncated frame in serial communication?",
                "follow_up_a": "By using a 3.5 character inter-frame timeout (Modbus RTU style) or an explicit length byte verified against received byte count before CRC checking.",
                "code": r'''/*
 * ============================================================================
 * Problem: Industrial Telemetry Frame Encoder & Decoder
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#define FRAME_START 0xAAU
#define FRAME_END   0x55U

typedef struct {
    uint8_t  start;
    uint8_t  cmd;
    uint16_t data;
    uint8_t  checksum;
    uint8_t  end;
} packet_t;

static uint8_t calc_xor_chk(uint8_t cmd, uint16_t data) {
    return (uint8_t)(cmd ^ (data & 0xFF) ^ (data >> 8));
}

int main(void)
{
    printf("=== Day 29: Live Interview Coding: Telemetry Frame Engine ===\n\n");

    /* 1. Build and encode */
    packet_t tx = {
        .start = FRAME_START,
        .cmd = 0x05, /* Set Relay */
        .data = 120, /* 120s timer */
        .checksum = calc_xor_chk(0x05, 120),
        .end = FRAME_END
    };

    printf("Encoded Frame: [0x%02X] CMD:0x%02X DATA:%u CHK:0x%02X [0x%02X]\n",
           tx.start, tx.cmd, tx.data, tx.checksum, tx.end);

    /* 2. Decode and verify */
    if (tx.start == FRAME_START && tx.end == FRAME_END) {
        uint8_t expected_chk = calc_xor_chk(tx.cmd, tx.data);
        if (expected_chk == tx.checksum) {
            printf("SUCCESS: Frame Received & Checksum Verified Cleanly!\n");
        } else {
            printf("ERROR: Checksum Mismatch!\n");
        }
    }

    return 0;
}
'''
            }
        ]
    },
    30: {
        "folder_name": "Day-30-Master-Capstone-Revision-Cheatsheet",
        "title": "Day 30: 30-Day Master Capstone & Embedded Cheatsheet",
        "overview": "Master consolidation of all 30 days: core C idioms, pointer scaling, bitwise tricks, volatile rules, protocol timings, and interview cheat sheet.",
        "programs": [
            {
                "filename": "01_embedded_interview_cheatsheet.c",
                "focus": "Top 10 Essential Embedded C Interview Code Idioms in One File",
                "time_complexity": "O(1) per idiom",
                "space_complexity": "O(1)",
                "insight": "The ultimate quick-revision compilable reference for technical screening tests and live coding rounds.",
                "follow_up_q": "What is the single most important rule in embedded firmware design?",
                "follow_up_a": "Determinism: Always know the upper bound of execution time and memory usage for every function.",
                "code": r'''/*
 * ============================================================================
 * Day 30 Master Capstone: Top 10 Embedded C Interview Idioms
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define SET_BIT(reg, bit)    ((reg) |= (1U << (bit)))
#define CLEAR_BIT(reg, bit)  ((reg) &= ~(1U << (bit)))
#define TOGGLE_BIT(reg, bit) ((reg) ^= (1U << (bit)))
#define CHECK_BIT(reg, bit)  (((reg) >> (bit)) & 1U)
#define IS_POW2(n)           (((n) > 0U) && (((n) & ((n) - 1U)) == 0U))

int main(void)
{
    printf("==============================================================\n");
    printf("   🏆 30-DAY EMBEDDED C INTERVIEW PREPARATION CAPSTONE       \n");
    printf("   Author: Sherifred Singh | Embedded Firmware Engineer       \n");
    printf("==============================================================\n\n");

    uint32_t reg = 0;
    SET_BIT(reg, 3);
    printf("1. Bit 3 set in register: 0x%02X\n", reg);
    printf("2. Is 128 Power of 2?     %s\n", IS_POW2(128) ? "YES" : "NO");
    printf("3. Pointer arithmetic scaling: ptr + 1 advances by sizeof(*ptr)\n");
    printf("4. Volatile prevents register caching in multi-threaded/ISR flows\n");
    printf("5. Table-driven FSM guarantees constant O(1) transition speed\n");
    printf("\nCONGRATULATIONS: 30-Day Embedded C Interview Suite Complete!\n");

    return 0;
}
'''
            }
        ]
    }
}
