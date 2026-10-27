# Day 06: CPU Interrupt Lifecycle & ISR Rules

Understanding interrupt vector tables (IVT), hardware context stacking, latency, reentrancy, and why printf() and malloc() are banned in ISRs.

---

## 📋 Program Index & Summary

| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **01** | **`01_interrupt_vector_lookup.c`** | Function Pointer Vector Table Dispatch Simulation | O(1) | O(1) | Cortex-M IVT holds 32-bit addresses of ISR functions. Hardware fetches the address directly from Flash upon interrupt assertion. |

---

## 💡 Embedded Notes & Key Hardware Takeaways

### 1. Function Pointer Vector Table Dispatch Simulation
- **Key Silicon Insight:** Cortex-M IVT holds 32-bit addresses of ISR functions. Hardware fetches the address directly from Flash upon interrupt assertion.
- **Technical Design Question:** *Why must an ISR never call printf() or malloc()?*
- **Engineering Rationale:** printf() is non-reentrant, slow (milliseconds), and blocks UART. malloc() uses a non-reentrant heap lock and can cause deadlocks if an ISR interrupts a thread holding the lock.

---

## 🛠 How to Compile & Run

```bash
# Compile all programs in this module with strict C99 warnings
gcc -Wall -Wextra -std=c99 -pedantic 01_interrupt_vector_lookup.c -o 01_interrupt_vector_lookup && ./01_interrupt_vector_lookup
```
