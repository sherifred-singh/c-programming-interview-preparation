"""
Curriculum definitions for Days 04 through 10.
"""

DAYS_04_TO_10 = {
    4: {
        "folder_name": "Day-04-Volatile-And-Optimization",
        "title": "Day 04: Volatile Keyword & Compiler Optimizations",
        "overview": "Mastering the volatile keyword, memory-mapped peripheral I/O, shared ISR flags, and avoiding compiler optimization register-caching pitfalls.",
        "programs": [
            {
                "filename": "01_volatile_isr_flag.c",
                "focus": "Volatile Shared Flag between ISR and Main Loop",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "Without volatile, gcc -O2 caches the flag in a CPU register (e.g. R4), turning 'while(!flag)' into an infinite loop!",
                "follow_up_q": "Why does declaring a struct as volatile differ from declaring volatile struct members?",
                "follow_up_a": "Declaring 'volatile struct MyStruct s' makes all members within the struct volatile. Declaring specific members volatile allows the compiler to optimize access to other non-volatile fields.",
                "code": r'''/*
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
'''
            },
            {
                "filename": "02_hardware_register_access.c",
                "focus": "Volatile Pointer to Memory-Mapped Peripheral Registers",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "Hardware registers can change state autonomously (e.g. status flags set by silicon). Volatile prevents dead-code elimination.",
                "follow_up_q": "Why is a hardware register typically defined as *(volatile uint32_t *)addr?",
                "follow_up_a": "The pointer must be volatile because peripheral registers have side effects on read/write. If non-volatile, multiple consecutive writes might be collapsed into just the last write by an optimizing compiler.",
                "code": r'''/*
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
#define SIM_CONTROL_REG (*volatile uint32_t *)&s_mock_peripheral_memory[1])
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
'''
            }
        ]
    },
    5: {
        "folder_name": "Day-05-Struct-Padding-And-Alignment",
        "title": "Day 05: Structure Padding, Memory Alignment & Packing",
        "overview": "Understanding natural boundary memory alignment, compiler struct padding, sizeof calculation, #pragma pack(1), and attribute((packed)) for serial frames.",
        "programs": [
            {
                "filename": "01_struct_padding_alignment.c",
                "focus": "Natural 32-Bit Memory Alignment & Padding Waste",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "Reordering struct members from largest to smallest eliminates padding waste and saves 33% RAM per struct instance on 32-bit MCUs.",
                "follow_up_q": "Why do 32-bit ARM cores enforce 4-byte natural alignment?",
                "follow_up_a": "Unaligned memory access (e.g. reading 32-bit integer from address 0x20000001) causes a UsageFault exception on Cortex-M0/M0+, or takes multiple bus cycles on Cortex-M3/M4.",
                "code": r'''/*
 * ============================================================================
 * Problem: Struct Member Alignment and Memory Layout Optimization
 * 
 * Embedded Hardware Insight:
 *   32-bit CPUs (ARM Cortex-M) read memory in 4-byte words.
 *   - A 4-byte uint32_t must be placed at an address divisible by 4.
 *   - A 2-byte uint16_t must be placed at an address divisible by 2.
 *   - A 1-byte uint8_t can be placed at any byte address.
 * 
 * If fields are declared naively:
 *   struct Bad { char a; int b; char c; }; -> sizeof is 12 bytes! (6 bytes wasted)
 * If reordered from largest to smallest:
 *   struct Good { int b; char a; char c; }; -> sizeof is 8 bytes! (33% memory saved)
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stddef.h>

/* Naive member ordering: generates padding */
struct SensorData_Padded {
    uint8_t  sensor_id;   /* 1 byte  + 3 bytes padding */
    uint32_t timestamp_ms;/* 4 bytes */
    uint8_t  status_flag; /* 1 byte  + 3 bytes tail padding */
};

/* Reordered member ordering: eliminates internal padding */
struct SensorData_Optimized {
    uint32_t timestamp_ms;/* 4 bytes */
    uint8_t  sensor_id;   /* 1 byte */
    uint8_t  status_flag; /* 1 byte  + 2 bytes tail padding */
};

int main(void)
{
    printf("=== Day 05: Structure Padding & Alignment Analysis ===\n\n");

    printf("Padded Struct:\n");
    printf(" - Sizeof            : %zu bytes\n", sizeof(struct SensorData_Padded));
    printf(" - Offset of sensor_id    : %zu\n", offsetof(struct SensorData_Padded, sensor_id));
    printf(" - Offset of timestamp_ms : %zu\n", offsetof(struct SensorData_Padded, timestamp_ms));
    printf(" - Offset of status_flag  : %zu\n\n", offsetof(struct SensorData_Padded, status_flag));

    printf("Optimized Struct (Reordered):\n");
    printf(" - Sizeof            : %zu bytes (Saved %zu bytes per instance!)\n",
           sizeof(struct SensorData_Optimized),
           sizeof(struct SensorData_Padded) - sizeof(struct SensorData_Optimized));
    printf(" - Offset of timestamp_ms : %zu\n", offsetof(struct SensorData_Optimized, timestamp_ms));
    printf(" - Offset of sensor_id    : %zu\n", offsetof(struct SensorData_Optimized, sensor_id));
    printf(" - Offset of status_flag  : %zu\n", offsetof(struct SensorData_Optimized, status_flag));

    return 0;
}
'''
            },
            {
                "filename": "02_pragma_pack_telemetry.c",
                "focus": "Packed Structs for Network & Fieldbus Serialization",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "#pragma pack(1) forces exact byte alignment, eliminating padding for over-the-air or RS-485 serial frames.",
                "follow_up_q": "What performance hazard occurs when accessing fields of a packed struct?",
                "follow_up_a": "Accessing unaligned fields forces the CPU or compiler to generate multiple single-byte reads and shift operations, increasing code size and cycle count.",
                "code": r'''/*
 * ============================================================================
 * Problem: Exact Byte Packing for Network / Serial Frames (#pragma pack)
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <string.h>

#pragma pack(push, 1)
struct TelemetryPacket_Packed {
    uint8_t  start_byte;  /* 1 byte */
    uint16_t node_id;     /* 2 bytes */
    uint32_t sensor_val;  /* 4 bytes */
    uint16_t checksum;    /* 2 bytes */
};
#pragma pack(pop)

int main(void)
{
    printf("=== Day 05: Packed Struct for Serial Frame Serialization ===\n\n");

    struct TelemetryPacket_Packed pkt;
    pkt.start_byte = 0xAA;
    pkt.node_id = 0x0102;
    pkt.sensor_val = 0x12345678;
    pkt.checksum = 0xFFFF;

    printf("Packed Packet Total Size: %zu bytes (Exact sum: 1 + 2 + 4 + 2 = 9)\n\n",
           sizeof(pkt));

    uint8_t raw_buffer[sizeof(pkt)];
    memcpy(raw_buffer, &pkt, sizeof(pkt));

    printf("Byte Stream on RS-485 / CAN Bus:\n");
    for (size_t i = 0; i < sizeof(pkt); i++) {
        printf(" [%02zu]: 0x%02X\n", i, raw_buffer[i]);
    }

    return 0;
}
'''
            }
        ]
    },
    6: {
        "folder_name": "Day-06-Interrupt-Lifecycle-And-ISR-Rules",
        "title": "Day 06: CPU Interrupt Lifecycle & ISR Rules",
        "overview": "Understanding interrupt vector tables (IVT), hardware context stacking, latency, reentrancy, and why printf() and malloc() are banned in ISRs.",
        "programs": [
            {
                "filename": "01_interrupt_vector_lookup.c",
                "focus": "Function Pointer Vector Table Dispatch Simulation",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "Cortex-M IVT holds 32-bit addresses of ISR functions. Hardware fetches the address directly from Flash upon interrupt assertion.",
                "follow_up_q": "Why must an ISR never call printf() or malloc()?",
                "follow_up_a": "printf() is non-reentrant, slow (milliseconds), and blocks UART. malloc() uses a non-reentrant heap lock and can cause deadlocks if an ISR interrupts a thread holding the lock.",
                "code": r'''/*
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
'''
            }
        ]
    },
    7: {
        "folder_name": "Day-07-Week-1-Speed-Drills-Consolidation",
        "title": "Day 07: Week 1 Speed Drills & Consolidation",
        "overview": "15-minute speed drills testing power-of-2 checks, endian byte swaps, set bit counting, and register bit manipulation without hesitation.",
        "programs": [
            {
                "filename": "01_week1_speed_drill.c",
                "focus": "15-Minute Blank Screen Muscle Memory Consolidation",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "Mastering the top 4 recurring bitwise and memory operations tested in live embedded screening tests.",
                "follow_up_q": "How does (x & -x) isolate the lowest set bit in two's complement?",
                "follow_up_a": "In two's complement, -x = (~x + 1). All bits above the lowest set bit are inverted, so bitwise AND keeps only that lowest set bit.",
                "code": r'''/*
 * ============================================================================
 * Problem: Week 1 Embedded C Technical Speed Drill
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define IS_POWER_OF_TWO(n)  (((n) > 0U) && (((n) & ((n) - 1U)) == 0U))
#define ISOLATE_LOWEST_BIT(n) ((n) & -(int32_t)(n))

static uint32_t fast_bswap32(uint32_t x)
{
    return ((x & 0x000000FFU) << 24) |
           ((x & 0x0000FF00U) << 8)  |
           ((x & 0x00FF0000U) >> 8)  |
           ((x & 0xFF000000U) >> 24);
}

int main(void)
{
    printf("=== Day 07: Week 1 Speed Drills & Consolidation ===\n\n");

    uint32_t test_val = 64U;
    printf("1. Is %u Power of Two? %s\n", test_val, IS_POWER_OF_TWO(test_val) ? "YES" : "NO");

    uint32_t non_pow2 = 65U;
    printf("2. Is %u Power of Two? %s\n", non_pow2, IS_POWER_OF_TWO(non_pow2) ? "YES" : "NO");

    uint32_t val = 0x00000018; /* 0b...0001_1000 */
    printf("3. Lowest set bit of 0x%08X is: 0x%08X (Expected 0x08)\n", val, ISOLATE_LOWEST_BIT(val));

    uint32_t word = 0xAABBCCDD;
    printf("4. Byte swap 0x%08X -> 0x%08X\n", word, fast_bswap32(word));

    return 0;
}
'''
            }
        ]
    },
    8: {
        "folder_name": "Day-08-UART-Ring-Buffer",
        "title": "Day 08: UART Peripheral & Circular FIFO Ring Buffer",
        "overview": "Implementing a lock-free Single-Producer Single-Consumer (SPSC) circular byte ring buffer for interrupt-driven serial communication.",
        "programs": [
            {
                "filename": "01_uart_ring_buffer.c",
                "focus": "Lock-Free SPSC Circular FIFO Ring Buffer",
                "time_complexity": "O(1) push and pop",
                "space_complexity": "O(N) static buffer",
                "insight": "By using power-of-two buffer sizes, modulo '%' (20-40 cycles) is replaced with bitwise '& (SIZE - 1)' (1 cycle)!",
                "follow_up_q": "Why is an SPSC ring buffer lock-free between an ISR and main loop?",
                "follow_up_a": "The producer (ISR) only writes to 'head', and the consumer (main) only writes to 'tail'. Because neither modifies the other's index, no mutex or critical section is needed if reads/writes are atomic.",
                "code": r'''/*
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
'''
            }
        ]
    },
    9: {
        "folder_name": "Day-09-RS485-Modbus-RTU-Timing",
        "title": "Day 09: RS-485 Modbus RTU Framing & Transceiver Timing",
        "overview": "Half-duplex RS-485 DE/RE transceiver timing, the TRMT vs TXIF shift-register trap, and table-driven CRC-16 calculation.",
        "programs": [
            {
                "filename": "01_modbus_crc16.c",
                "focus": "Standard Modbus CRC-16 Calculation (Polynomial 0xA001)",
                "time_complexity": "O(N) message length",
                "space_complexity": "O(1)",
                "insight": "Modbus transmits CRC LSB first, unlike standard network protocols which transmit MSB first.",
                "follow_up_q": "Why does checking TXIF instead of TRMT corrupt RS-485 packets?",
                "follow_up_a": "TXIF signals the transmit data buffer is empty, but the byte is still actively shifting out the wire via the shift register! Flipping DE pin immediately cuts off the stop bit and corrupts the packet.",
                "code": r'''/*
 * ============================================================================
 * Problem: Modbus RTU CRC-16 Calculation
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>

uint16_t modbus_crc16(const uint8_t *buffer, size_t length)
{
    uint16_t crc = 0xFFFFU;
    for (size_t i = 0; i < length; i++) {
        crc ^= (uint16_t)buffer[i];
        for (int bit = 0; bit < 8; bit++) {
            if (crc & 0x0001U) {
                crc = (crc >> 1U) ^ 0xA001U;
            } else {
                crc >>= 1U;
            }
        }
    }
    return crc;
}

int main(void)
{
    printf("=== Day 09: Modbus RTU CRC-16 Generator ===\n\n");

    /* Standard Modbus Query: Slave 0x01, Function 0x03, Start Reg 0x0000, 2 Regs */
    uint8_t query[] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x02};
    uint16_t crc = modbus_crc16(query, sizeof(query));

    printf("Query Packet: 01 03 00 00 00 02\n");
    printf("CRC-16 Result: 0x%04X (Transmitted on wire as: 0x%02X 0x%02X)\n",
           crc, (uint8_t)(crc & 0xFF), (uint8_t)(crc >> 8));

    return 0;
}
'''
            }
        ]
    },
    10: {
        "folder_name": "Day-10-I2C-Recovery-And-EEPROM",
        "title": "Day 10: I2C Bus Protocol, 9-Clock Recovery & EEPROM",
        "overview": "Open-drain pull-up sizing, handling I2C bus lockups with the senior 9-clock manual SCL toggling routine, and 32-byte page write boundaries.",
        "programs": [
            {
                "filename": "01_i2c_bus_recovery.c",
                "focus": "Manual 9-Clock SCL Toggling Routine for Stuck Slave SDA",
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "insight": "If a master resets during an I2C read while a slave is driving SDA low (ACK), the bus hangs forever unless SCL is clocked 9 times.",
                "follow_up_q": "What causes an I2C slave to hold SDA low indefinitely?",
                "follow_up_a": "The slave was in the middle of sending a 0 bit when the master CPU was reset. The slave is waiting for SCL clock pulses to finish its byte.",
                "code": r'''/*
 * ============================================================================
 * Problem: I2C Bus Stuck-Low Recovery via 9 SCL Clock Pulses
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

/* Simulated GPIO Bit-Banging */
static void SCL_Set(bool high) { printf(" SCL -> %s\n", high ? "HIGH" : "LOW"); }
static void SDA_Set(bool high) { printf(" SDA -> %s\n", high ? "HIGH" : "LOW"); }
static bool SDA_Read(void)     { return true; /* Assume freed */ }

static void i2c_bus_clear_recovery(void)
{
    printf("1. Configuring SCL and SDA as open-drain GPIO outputs...\n");
    SDA_Set(true);

    printf("2. Clocking SCL 9 times to force stuck slave to release SDA...\n");
    for (int i = 0; i < 9; i++) {
        SCL_Set(false);
        SCL_Set(true);
        if (SDA_Read()) {
            printf(" -> Slave released SDA line after %d clock pulses!\n", i + 1);
            break;
        }
    }

    printf("3. Generating STOP condition (SDA low -> SCL high -> SDA high)...\n");
    SDA_Set(false);
    SCL_Set(true);
    SDA_Set(true);
    printf("4. I2C Bus Restored Cleanly!\n");
}

int main(void)
{
    printf("=== Day 10: Senior I2C 9-Clock Bus Recovery Routine ===\n\n");
    i2c_bus_clear_recovery();
    return 0;
}
'''
            }
        ]
    }
}
