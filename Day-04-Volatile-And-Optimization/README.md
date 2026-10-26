# Day 04: Volatile Keyword & Compiler Optimizations

Mastering the volatile keyword, memory-mapped peripheral I/O, shared ISR flags, and avoiding compiler optimization register-caching pitfalls.

---

## 📋 Program Index & Summary

| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **01** | **`01_volatile_isr_flag.c`** | Volatile Shared Flag between ISR and Main Loop | O(1) | O(1) | Without volatile, gcc -O2 caches the flag in a CPU register (e.g. R4), turning 'while(!flag)' into an infinite loop! |
| **02** | **`02_hardware_register_access.c`** | Volatile Pointer to Memory-Mapped Peripheral Registers | O(1) | O(1) | Hardware registers can change state autonomously (e.g. status flags set by silicon). Volatile prevents dead-code elimination. |

---

## 💡 Embedded Notes & Key Hardware Takeaways

### 1. Volatile Shared Flag between ISR and Main Loop
- **Key Silicon Insight:** Without volatile, gcc -O2 caches the flag in a CPU register (e.g. R4), turning 'while(!flag)' into an infinite loop!
- **Interview Follow-Up Q:** *Why does declaring a struct as volatile differ from declaring volatile struct members?*
- **Candidate Defense:** Declaring 'volatile struct MyStruct s' makes all members within the struct volatile. Declaring specific members volatile allows the compiler to optimize access to other non-volatile fields.

### 2. Volatile Pointer to Memory-Mapped Peripheral Registers
- **Key Silicon Insight:** Hardware registers can change state autonomously (e.g. status flags set by silicon). Volatile prevents dead-code elimination.
- **Interview Follow-Up Q:** *Why is a hardware register typically defined as *(volatile uint32_t *)addr?*
- **Candidate Defense:** The pointer must be volatile because peripheral registers have side effects on read/write. If non-volatile, multiple consecutive writes might be collapsed into just the last write by an optimizing compiler.

---

## 🛠 How to Compile & Run

```bash
# Compile all programs in this module with strict C99 warnings
gcc -Wall -Wextra -std=c99 -pedantic 01_volatile_isr_flag.c -o 01_volatile_isr_flag && ./01_volatile_isr_flag
gcc -Wall -Wextra -std=c99 -pedantic 02_hardware_register_access.c -o 02_hardware_register_access && ./02_hardware_register_access
```
