# Day 16: Memory Pools & Dynamic Heap Avoidance

Fixed-size block allocators preventing heap fragmentation in long-running mission-critical firmware.

---

## 📋 Program Index & Summary

| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **01** | **`01_fixed_block_pool.c`** | Fixed-Size Block Allocator (Deterministic malloc/free Alternative) | O(1) allocation and free | O(N) static memory pool | MISRA-C Rule 21.3 bans dynamic heap allocation because fragmentation causes unpredictable allocation failures after weeks of operation. |

---

## 💡 Embedded Notes & Key Hardware Takeaways

### 1. Fixed-Size Block Allocator (Deterministic malloc/free Alternative)
- **Key Silicon Insight:** MISRA-C Rule 21.3 bans dynamic heap allocation because fragmentation causes unpredictable allocation failures after weeks of operation.
- **Technical Design Question:** *How does a fixed-block memory pool achieve O(1) allocation time?*
- **Engineering Rationale:** It maintains a singly linked list of free blocks in a static array. Allocation simply pops the head of the free list in O(1) time.

---

## 🛠 How to Compile & Run

```bash
# Compile all programs in this module with strict C99 warnings
gcc -Wall -Wextra -std=c99 -pedantic 01_fixed_block_pool.c -o 01_fixed_block_pool && ./01_fixed_block_pool
```
