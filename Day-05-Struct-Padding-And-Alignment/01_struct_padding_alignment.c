/*
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
