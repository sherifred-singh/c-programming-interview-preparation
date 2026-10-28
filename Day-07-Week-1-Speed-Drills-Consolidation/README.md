# Day 07: Week 1 Speed Drills & Consolidation

15-minute speed drills testing power-of-2 checks, endian byte swaps, set bit counting, and register bit manipulation without hesitation.

---

## 📋 Program Index & Summary

| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **01** | **`01_week1_speed_drill.c`** | 15-Minute Blank Screen Muscle Memory Consolidation | O(1) | O(1) | Mastering the top 4 recurring bitwise and memory operations tested in live embedded screening tests. |

---

## 💡 Embedded Notes & Key Hardware Takeaways

### 1. 15-Minute Blank Screen Muscle Memory Consolidation
- **Key Silicon Insight:** Mastering the top 4 recurring bitwise and memory operations tested in live embedded screening tests.
- **Technical Design Question:** *How does (x & -x) isolate the lowest set bit in two's complement?*
- **Engineering Rationale:** In two's complement, -x = (~x + 1). All bits above the lowest set bit are inverted, so bitwise AND keeps only that lowest set bit.

---

## 🛠 How to Compile & Run

```bash
# Compile all programs in this module with strict C99 warnings
gcc -Wall -Wextra -std=c99 -pedantic 01_week1_speed_drill.c -o 01_week1_speed_drill && ./01_week1_speed_drill
```
