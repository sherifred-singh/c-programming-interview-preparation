# Day 09: RS-485 Modbus RTU Framing & Transceiver Timing

Half-duplex RS-485 DE/RE transceiver timing, the TRMT vs TXIF shift-register trap, and table-driven CRC-16 calculation.

---

## 📋 Program Index & Summary

| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **01** | **`01_modbus_crc16.c`** | Standard Modbus CRC-16 Calculation (Polynomial 0xA001) | O(N) message length | O(1) | Modbus transmits CRC LSB first, unlike standard network protocols which transmit MSB first. |

---

## 💡 Embedded Notes & Key Hardware Takeaways

### 1. Standard Modbus CRC-16 Calculation (Polynomial 0xA001)
- **Key Silicon Insight:** Modbus transmits CRC LSB first, unlike standard network protocols which transmit MSB first.
- **Technical Design Question:** *Why does checking TXIF instead of TRMT corrupt RS-485 packets?*
- **Engineering Rationale:** TXIF signals the transmit data buffer is empty, but the byte is still actively shifting out the wire via the shift register! Flipping DE pin immediately cuts off the stop bit and corrupts the packet.

---

## 🛠 How to Compile & Run

```bash
# Compile all programs in this module with strict C99 warnings
gcc -Wall -Wextra -std=c99 -pedantic 01_modbus_crc16.c -o 01_modbus_crc16 && ./01_modbus_crc16
```
