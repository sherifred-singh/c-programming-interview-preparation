# Day 12: ADC Mechanics, Calibration & Digital Filters

Fixed-point Q8 Exponential Moving Average (EMA) and Median-3 filter implementations to reject electrical noise without floating-point FPU overhead.

---

## 📋 Program Index & Summary

| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **01** | **`01_fixed_point_ema_filter.c`** | Integer-Only Q8 Fixed-Point EMA Filter | O(1) | O(1) | Floating-point math on MCUs without hardware FPU bloats code with emulation routines. Fixed-point division by 256 is a 1-cycle bit-shift (>> 8). |

---

## 💡 Embedded Notes & Key Hardware Takeaways

### 1. Integer-Only Q8 Fixed-Point EMA Filter
- **Key Silicon Insight:** Floating-point math on MCUs without hardware FPU bloats code with emulation routines. Fixed-point division by 256 is a 1-cycle bit-shift (>> 8).
- **Technical Design Question:** *How do you choose alpha in an EMA filter?*
- **Engineering Rationale:** A smaller alpha gives stronger high-frequency noise smoothing but introduces lag. A larger alpha tracks rapid signal changes with less delay.

---

## 🛠 How to Compile & Run

```bash
# Compile all programs in this module with strict C99 warnings
gcc -Wall -Wextra -std=c99 -pedantic 01_fixed_point_ema_filter.c -o 01_fixed_point_ema_filter && ./01_fixed_point_ema_filter
```
