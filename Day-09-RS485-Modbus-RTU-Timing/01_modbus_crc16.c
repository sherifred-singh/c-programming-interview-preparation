/*
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
