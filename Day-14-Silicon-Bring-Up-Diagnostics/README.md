# Day 14: Silicon Bring-Up & Board Diagnostics

The senior 5-step board bring-up sequence: cold resistance inspection, current-limited power up, crystal verification, and SWD connection.

---

## 📋 Program Index & Summary

| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **01** | **`01_board_bringup_checklist.c`** | Deterministic 5-Step Bring-Up State Verification | O(1) | O(1) | Never power a prototype board directly from mains or an unconstrained battery; always set current limits to 50mA to prevent silicon destruction. |

---

## 💡 Embedded Notes & Key Hardware Takeaways

### 1. Deterministic 5-Step Bring-Up State Verification
- **Key Silicon Insight:** Never power a prototype board directly from mains or an unconstrained battery; always set current limits to 50mA to prevent silicon destruction.
- **Technical Design Question:** *What is the very first thing you check when a newly assembled PCB doesn't enumerate on SWD?*
- **Engineering Rationale:** Check VDD/GND voltages, reset pin voltage (must be high for active-low NRST), and verify crystal oscillation with a 10x oscilloscope probe.

---

## 🛠 How to Compile & Run

```bash
# Compile all programs in this module with strict C99 warnings
gcc -Wall -Wextra -std=c99 -pedantic 01_board_bringup_checklist.c -o 01_board_bringup_checklist && ./01_board_bringup_checklist
```
