# Day 08: UART Peripheral & Circular FIFO Ring Buffer

Implementing a lock-free Single-Producer Single-Consumer (SPSC) circular byte ring buffer for interrupt-driven serial communication.

---

## 📋 Program Index & Summary

| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **01** | **`01_uart_ring_buffer.c`** | Lock-Free SPSC Circular FIFO Ring Buffer | O(1) push and pop | O(N) static buffer | By using power-of-two buffer sizes, modulo '%' (20-40 cycles) is replaced with bitwise '& (SIZE - 1)' (1 cycle)! |

---

## 💡 Embedded Notes & Key Hardware Takeaways

### 1. Lock-Free SPSC Circular FIFO Ring Buffer
- **Key Silicon Insight:** By using power-of-two buffer sizes, modulo '%' (20-40 cycles) is replaced with bitwise '& (SIZE - 1)' (1 cycle)!
- **Technical Design Question:** *Why is an SPSC ring buffer lock-free between an ISR and main loop?*
- **Engineering Rationale:** The producer (ISR) only writes to 'head', and the consumer (main) only writes to 'tail'. Because neither modifies the other's index, no mutex or critical section is needed if reads/writes are atomic.

---

## 🛠 How to Compile & Run

```bash
# Compile all programs in this module with strict C99 warnings
gcc -Wall -Wextra -std=c99 -pedantic 01_uart_ring_buffer.c -o 01_uart_ring_buffer && ./01_uart_ring_buffer
```
