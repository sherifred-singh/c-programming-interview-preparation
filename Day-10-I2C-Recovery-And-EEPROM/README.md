# Day 10: I2C Bus Protocol, 9-Clock Recovery & EEPROM

Open-drain pull-up sizing, handling I2C bus lockups with the senior 9-clock manual SCL toggling routine, and 32-byte page write boundaries.

---

## 📋 Program Index & Summary

| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **01** | **`01_i2c_bus_recovery.c`** | Manual 9-Clock SCL Toggling Routine for Stuck Slave SDA | O(1) | O(1) | If a master resets during an I2C read while a slave is driving SDA low (ACK), the bus hangs forever unless SCL is clocked 9 times. |

---

## 💡 Embedded Notes & Key Hardware Takeaways

### 1. Manual 9-Clock SCL Toggling Routine for Stuck Slave SDA
- **Key Silicon Insight:** If a master resets during an I2C read while a slave is driving SDA low (ACK), the bus hangs forever unless SCL is clocked 9 times.
- **Technical Design Question:** *What causes an I2C slave to hold SDA low indefinitely?*
- **Engineering Rationale:** The slave was in the middle of sending a 0 bit when the master CPU was reset. The slave is waiting for SCL clock pulses to finish its byte.

---

## 🛠 How to Compile & Run

```bash
# Compile all programs in this module with strict C99 warnings
gcc -Wall -Wextra -std=c99 -pedantic 01_i2c_bus_recovery.c -o 01_i2c_bus_recovery && ./01_i2c_bus_recovery
```
