/*
 * ============================================================================
 * Problem: Bit Packing and Unpacking for Communication Telemetry & CAN Frames
 * 
 * Scenario:
 *   Industrial telemetry frames cannot waste bandwidth. Instead of sending
 *   multiple 32-bit variables, pack 4 sub-system fields into one 16-bit payload:
 *     - Relay ID  : 3 bits (values 0 - 7)       [bits 2:0]
 *     - Mode      : 2 bits (values 0 - 3)       [bits 4:3]
 *     - Fault Flag: 1 bit  (0 = OK, 1 = Fault)  [bit 5]
 *     - Delay Sec : 10 bits (values 0 - 1023)   [bits 15:6]
 * 
 * Embedded Hardware Insight:
 *   - Why manual shift-and-mask over C struct bitfields?
 *     In ANSI C (ISO/IEC 9899), the bitfield allocation order (high-to-low vs
 *     low-to-high) and alignment padding are implementation-defined. If one MCU
 *     is little-endian and compiler-packs from LSB, while another compiler-packs
 *     from MSB, communication fails silently!
 *     Manual bit shifts guarantee 100% deterministic, portable serialization.
 * 
 * Complexity:
 *   - Time Complexity: O(1) single-cycle bit shifting and masking.
 *   - Space Complexity: O(1) zero dynamic memory allocation.
 * 
 * Interview Follow-Up:
 *   Q: What happens if a developer tries to pack a 4-bit value into a 3-bit slot
 *      without masking the input value first?
 *   A: If the input value exceeds the maximum capacity of the field (e.g., value 9
 *      = 0b1001 into a 3-bit field), the unmasked upper bits spill over into the
 *      adjacent field, corrupting neighboring data! Always mask: (val & MASK) << SHIFT.
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

/* --- Bitfield Position Shifts & Width Masks --- */
#define RELAY_ID_SHIFT      0U
#define RELAY_ID_MASK       0x07U   /* 3 bits: 0b111 */

#define MODE_SHIFT          3U
#define MODE_MASK           0x03U   /* 2 bits: 0b011 */

#define FAULT_FLAG_SHIFT    5U
#define FAULT_FLAG_MASK     0x01U   /* 1 bit : 0b001 */

#define DELAY_SEC_SHIFT     6U
#define DELAY_SEC_MASK      0x03FFU /* 10 bits: 0b11_1111_1111 */

/* Packs fields into a 16-bit register word */
static uint16_t pack_telemetry(uint8_t relay_id, uint8_t mode, bool fault, uint16_t delay_s)
{
    uint16_t packet = 0U;

    packet |= ((uint16_t)(relay_id & RELAY_ID_MASK))       << RELAY_ID_SHIFT;
    packet |= ((uint16_t)(mode     & MODE_MASK))           << MODE_SHIFT;
    packet |= ((uint16_t)(fault    & FAULT_FLAG_MASK))     << FAULT_FLAG_SHIFT;
    packet |= ((uint16_t)(delay_s  & DELAY_SEC_MASK))      << DELAY_SEC_SHIFT;

    return packet;
}

/* Extracts fields from a 16-bit register word */
static void unpack_telemetry(uint16_t packet, uint8_t *relay_id, uint8_t *mode, bool *fault, uint16_t *delay_s)
{
    if (!relay_id || !mode || !fault || !delay_s) {
        return; /* Pointer guard */
    }

    *relay_id = (uint8_t)((packet >> RELAY_ID_SHIFT)   & RELAY_ID_MASK);
    *mode     = (uint8_t)((packet >> MODE_SHIFT)       & MODE_MASK);
    *fault    = (bool)   ((packet >> FAULT_FLAG_SHIFT) & FAULT_FLAG_MASK);
    *delay_s  = (uint16_t)((packet >> DELAY_SEC_SHIFT) & DELAY_SEC_MASK);
}

int main(void)
{
    printf("=== Day 03: Telemetry Bit Packing & Extraction ===\n\n");

    /* Simulated input parameters */
    uint8_t  in_relay = 5U;      /* Max 7 */
    uint8_t  in_mode  = 2U;      /* Max 3 */
    bool     in_fault = true;    /* 1 bit */
    uint16_t in_delay = 750U;    /* Max 1023 */

    printf("Original Fields:\n");
    printf(" - Relay ID  : %u (Capacity: 0-7)\n", in_relay);
    printf(" - Mode      : %u (Capacity: 0-3)\n", in_mode);
    printf(" - Fault Flag: %s\n", in_fault ? "TRUE (1)" : "FALSE (0)");
    printf(" - Delay Sec : %u s (Capacity: 0-1023)\n\n", in_delay);

    /* Pack into single 16-bit word */
    uint16_t packed_word = pack_telemetry(in_relay, in_mode, in_fault, in_delay);
    printf("Packed 16-bit Word: 0x%04X (Decimal: %u)\n\n", packed_word, packed_word);

    /* Unpack and verify */
    uint8_t  out_relay = 0;
    uint8_t  out_mode  = 0;
    bool     out_fault = false;
    uint16_t out_delay = 0;

    unpack_telemetry(packed_word, &out_relay, &out_mode, &out_fault, &out_delay);

    printf("Unpacked Verification:\n");
    printf(" - Relay ID  : %u [%s]\n", out_relay, (out_relay == in_relay) ? "MATCH" : "MISMATCH");
    printf(" - Mode      : %u [%s]\n", out_mode,  (out_mode == in_mode)   ? "MATCH" : "MISMATCH");
    printf(" - Fault Flag: %s [%s]\n", out_fault ? "TRUE" : "FALSE", (out_fault == in_fault) ? "MATCH" : "MISMATCH");
    printf(" - Delay Sec : %u s [%s]\n", out_delay, (out_delay == in_delay) ? "MATCH" : "MISMATCH");

    return 0;
}
