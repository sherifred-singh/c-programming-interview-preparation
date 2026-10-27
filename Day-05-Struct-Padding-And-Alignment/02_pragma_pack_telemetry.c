/*
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
