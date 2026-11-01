# Day 11: SPI Bus Modes (0–3) & Sensor Interfacing

Understanding CPOL/CPHA timing diagrams for SPI Modes 0, 1, 2, and 3, and PT100 RTD 3-wire bridge compensation.

---

## 📋 Program Index & Summary

| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **01** | **`01_spi_mode_config.c`** | SPI CPOL and CPHA Mode Configuration Matrix | O(1) | O(1) | Mode 0 (CPOL=0, CPHA=0) captures data on the rising clock edge while idle low. Mode 3 (CPOL=1, CPHA=1) captures on rising edge while idle high. |

---

## 💡 Embedded Notes & Key Hardware Takeaways

### 1. SPI CPOL and CPHA Mode Configuration Matrix
- **Key Silicon Insight:** Mode 0 (CPOL=0, CPHA=0) captures data on the rising clock edge while idle low. Mode 3 (CPOL=1, CPHA=1) captures on rising edge while idle high.
- **Technical Design Question:** *Why is a 33-ohm series damping resistor placed on SPI lines?*
- **Engineering Rationale:** High-speed SPI clock signals (>10 MHz) cause ringing and overshoot due to trace inductance. The 33-ohm resistor absorbs reflections and protects inputs.

---

## 🛠 How to Compile & Run

```bash
# Compile all programs in this module with strict C99 warnings
gcc -Wall -Wextra -std=c99 -pedantic 01_spi_mode_config.c -o 01_spi_mode_config && ./01_spi_mode_config
```
