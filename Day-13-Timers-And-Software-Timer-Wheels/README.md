# Day 13: Hardware Timers & Non-Blocking Software Timer Wheels

Non-blocking tick-based software timer arrays eliminating delay loops in embedded firmware.

---

## 📋 Program Index & Summary

| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **01** | **`01_software_timer.c`** | Non-Blocking Tick List Software Timer Engine | O(N) timer check | O(N) timer structs | Calling delay_ms() halts the CPU and starves communication protocols. Software timers decouple timekeeping from execution. |

---

## 💡 Embedded Notes & Key Hardware Takeaways

### 1. Non-Blocking Tick List Software Timer Engine
- **Key Silicon Insight:** Calling delay_ms() halts the CPU and starves communication protocols. Software timers decouple timekeeping from execution.
- **Technical Design Question:** *How do you handle 32-bit tick counter roll-over in software timers?*
- **Engineering Rationale:** Always use unsigned subtraction: '(current_tick - start_tick) >= period'. In unsigned modulo arithmetic, subtraction works correctly across roll-over.

---

## 🛠 How to Compile & Run

```bash
# Compile all programs in this module with strict C99 warnings
gcc -Wall -Wextra -std=c99 -pedantic 01_software_timer.c -o 01_software_timer && ./01_software_timer
```
