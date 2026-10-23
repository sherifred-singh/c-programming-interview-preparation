# C Programming Interview Preparation

[![Language](https://img.shields.io/badge/Language-Embedded%20C%20(C99)-00599C?style=for-the-badge&logo=c&logoColor=white)](https://en.wikipedia.org/wiki/C_(programming_language))
[![Target](https://img.shields.io/badge/Target-ARM%20Cortex--M%20%2F%20Embedded%20Systems-032347?style=for-the-badge&logo=arm&logoColor=white)](https://developer.arm.com)
[![Standard](https://img.shields.io/badge/Standard-MISRA--C%20Mindset-2E8B57?style=for-the-badge)](https://en.wikipedia.org/wiki/MISRA_C)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

> **Curated daily repository of essential C programming interview questions, memory architecture concepts, bitwise techniques, and compilable implementations tailored for Embedded Firmware and Systems Engineers.**

---

## 🎯 Repository Purpose & Engineering Philosophy

Firmware and embedded systems interviews evaluate foundational C knowledge with an emphasis on **hardware awareness**, **memory efficiency**, and **deterministic execution**. 

Every program in this repository adheres to three core tenets:
1. **Natural, Human-Written Code:** Clean, standard C99 with meaningful identifier names, sensible input boundaries, and zero artificial bloat or overengineering.
2. **Embedded Hardware Insight:** Concrete explanations of how each algorithm interacts with hardware (register allocation, cycle costs on MCUs without hardware dividers, avoidance of stack explosion, cache/memory alignment, and volatile/const qualification).
3. **Structured Daily Progression:** Modular daily folders allowing continuous daily practice without breaking or altering previous sessions.

---

## 📅 Daily Curriculum & Roadmap

| Module | Topic Focus | Key Concepts & Hardware Insights | Status |
| :---: | :--- | :--- | :---: |
| **[Day 01](./Day-01-Basic-C-Programs/)** | **Basic C Programs & Bitwise Foundations** | Bitwise `& 1` vs `% 2`, integer overflow guards, integer square root, Kernighan set bits, string pointers vs arrays | ✅ Complete (11 Programs) |
| **[Day 02](./Day-02-Pointers-And-Memory/)** | **Pointers & Memory Architecture** | Pointer arithmetic scaling (`sizeof(*ptr)`), `const` qualifier matrix, register access patterns | ✅ Complete (2 Programs) |
| **Day 03** | **Bit Manipulation & Register Mapping** | Setting, clearing, toggling, bitfields, register masks, endianness detection | ⏳ In Progress |
| **Day 04** | **Structs, Unions & Memory Alignment** | Struct padding, `#pragma pack`, `attribute((packed))`, hardware overlay unions | ⏳ Upcoming |
| **Day 05** | **Storage Classes & Linker Scopes** | `volatile`, `static`, `extern`, `.data`, `.bss`, `.rodata`, stack memory layouts | ⏳ Upcoming |
| **Day 06** | **Embedded Data Structures** | Lock-free SPSC circular ring buffers, static allocation without dynamic heap (`malloc`) | ⏳ Upcoming |
| **Day 07** | **State Machines & Concurrency** | Table-driven Finite State Machines (FSM), interrupt-safe flags, critical sections | ⏳ Upcoming |

---

## 📋 Master Program Index

### Day 01 — Basic C Programs
1. **`01_even_or_odd.c`** — Check even or odd via bitwise `num & 1` (1 CPU cycle) vs modulo `num % 2` (20–40 cycles on Cortex-M0).
2. **`02_reverse_integer.c`** — Reverse 32-bit signed integer with proactive overflow boundary detection (`INT32_MAX / 10`).
3. **`03_palindrome_number.c`** — Palindrome detection using half-reversal to eliminate integer overflow risk completely.
4. **`04_factorial.c`** — Iterative 64-bit factorial calculation up to 20! (avoids MISRA-C Rule 17.2 recursion stack exhaustion).
5. **`05_prime_number.c`** — Integer-only prime check (`i * i <= n`) preventing heavy software floating-point emulation (`sqrt()`).
6. **`06_min_max_array.c`** — Single-pass linear scan with `NULL` pointer and boundary guards.
7. **`07_reverse_string.c`** — In-place two-pointer string reversal (distinguishing mutable RAM buffers from `.rodata` string literals).
8. **`08_count_vowels_consonants.c`** — Character categorization with safe `(unsigned char)` casting for `<ctype.h>` compliance.
9. **`09_fibonacci_series.c`** — Three-register state shift generating Fibonacci sequence in $O(N)$ time and $O(1)$ stack space.
10. **`10_swap_without_temp.c`** — XOR and arithmetic swapping with critical pointer aliasing protection (`ptr_a != ptr_b`).
11. **`11_count_set_bits.c`** — Brian Kernighan's algorithm ($O(K)$ loop clearing lowest set bit) and $O(1)$ power-of-two verification.

### Day 02 — Pointers & Memory Architecture
1. **`01_pointer_arithmetic.c`** — Demonstrating pointer increment scaling: `ptr + 1` advances by `sizeof(*ptr)` bytes across `uint8_t`, `uint16_t`, and `uint32_t`.
2. **`02_const_pointers.c`** — The "Clockwise / Right-to-Left" rule for `const int *`, `int * const`, and `const int * const` in peripheral driver design.

---

## 🛠 Compilation & Validation

All programs are written in standard C99 and compile cleanly with strict compiler warning flags:

```bash
# Compile any specific program with warnings enabled
gcc -Wall -Wextra -std=c99 -pedantic Day-01-Basic-C-Programs/01_even_or_odd.c -o test_bin
./test_bin

# Batch compilation check across all C files
for f in Day-*/*.c; do gcc -Wall -Wextra -std=c99 -pedantic "$f" -o /dev/null && echo "Compiled: $f"; done
```

---

## 👤 Author & Maintainer

- **Engineer:** Sherifred Singh (Embedded Firmware Engineer)
- **GitHub:** [@sherifred-singh](https://github.com/sherifred-singh)
- **Portfolio:** [sherifred-singh.github.io/PORTFOLIO](https://sherifred-singh.github.io/PORTFOLIO/)
- **LinkedIn:** [linkedin.com/in/sherifredsing](https://www.linkedin.com/in/sherifredsing/)
- **Email:** ssherifred@gmail.com
