# C Programming Interview Preparation (30-Day Master Track)

[![Language](https://img.shields.io/badge/Language-Embedded%20C%20(C99)-00599C?style=for-the-badge&logo=c&logoColor=white)](https://en.wikipedia.org/wiki/C_(programming_language))
[![Target](https://img.shields.io/badge/Target-ARM%20Cortex--M%20%2F%20Embedded%20Systems-032347?style=for-the-badge&logo=arm&logoColor=white)](https://developer.arm.com)
[![Standard](https://img.shields.io/badge/Standard-MISRA--C%20Mindset-2E8B57?style=for-the-badge)](https://en.wikipedia.org/wiki/MISRA_C)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

> **Curated 30-day repository of essential C programming interview questions, memory architecture concepts, bitwise techniques, and compilable implementations tailored for Embedded Firmware and Systems Engineers.**

---

## 🎯 Repository Purpose & Engineering Philosophy

Firmware and embedded systems interviews evaluate foundational C knowledge with an emphasis on **hardware awareness**, **memory efficiency**, and **deterministic execution**. 


---

## 📅 30-Day Master Curriculum & Roadmap

### 🧱 Week 1: Core C, Bitwise & Silicon Registers (Days 01 – 07)
| Module | Topic Focus | Key Concepts & Hardware Insights | Status |
| :---: | :--- | :--- | :---: |
| **[Day 01](./Day-01-Basic-C-Programs/)** | **Basic C Programs & Bitwise Foundations** | Bitwise `& 1` vs `% 2`, integer overflow guards, integer square root, Kernighan set bits, string pointers vs arrays | ✅ Complete (11 Programs) |
| **[Day 02](./Day-02-Pointers-And-Memory/)** | **Pointers & Memory Architecture** | Pointer arithmetic scaling (`sizeof(*ptr)`), `const` qualifier matrix, register access patterns | ✅ Complete (2 Programs) |
| **[Day 03](./Day-03-Bit-Manipulation-And-Registers/)** | **Bit Manipulation & Silicon Register Mapping** | SET_BIT, CLEAR_BIT, TOGGLE_BIT, CHECK_BIT macros, bitfield packing, endianness detection | ✅ Complete (5 Programs) |
| **[Day 04](./Day-04-Volatile-And-Optimization/)** | **Volatile Keyword & Compiler Optimizations** | Memory-mapped I/O, ISR shared flags, `-O2` register caching pitfalls, read-modify-write | ✅ Complete (2 Programs) |
| **[Day 05](./Day-05-Struct-Padding-And-Alignment/)** | **Structure Padding, Memory Alignment & Packing** | Natural memory alignment, `#pragma pack(1)`, `__attribute__((packed))`, offset calculation | ✅ Complete (2 Programs) |
| **[Day 06](./Day-06-Interrupt-Lifecycle-And-ISR-Rules/)** | **CPU Interrupt Lifecycle & ISR Rules** | IVT vectors, context save/restore, hardware flag clearing, latency & reentrancy | ✅ Complete (1 Program) |
| **[Day 07](./Day-07-Week-1-Speed-Drills-Consolidation/)** | **Week 1 Speed Drills & Consolidation** | 15-minute speed drills: power-of-2, byte swaps, reverse words, bit count benchmarks | ✅ Complete (1 Program) |

### 🔌 Week 2: Serial Protocols, Buffers & Peripheral Drivers (Days 08 – 14)
| Module | Topic Focus | Key Concepts & Hardware Insights | Status |
| :---: | :--- | :--- | :---: |
| **[Day 08](./Day-08-UART-Ring-Buffer/)** | **UART Peripheral & Circular FIFO Ring Buffer** | Lock-free SPSC circular buffer, overflow protection, atomic head/tail pointers | ✅ Complete (1 Program) |
| **Day 09** | **RS-485 Modbus RTU Framing & Transceiver Timing** | Half-duplex DE/RE timing, `TRMT` vs `TXIF` shift-register trap, fast CRC-16 table | ⏳ Next Up |
| **Day 10** | **I2C Bus Protocol, 9-Clock Recovery & EEPROM** | Open-drain pull-up sizing, page boundary rollovers, 9-clock bus-clear recovery routine | ⏳ Upcoming |
| **Day 11** | **SPI Bus Modes (0–3) & Sensor Interfacing** | CPOL/CPHA timing, PT100 RTD 3-wire bridge compensation, series damping resistors | ⏳ Upcoming |
| **Day 12** | **ADC Mechanics, Calibration & Digital Filters** | Resolution step size, sampling capacitor acquisition time, fixed-point EMA & Median-3 | ⏳ Upcoming |
| **Day 13** | **Hardware Timers, PWM & Software Timer Wheels** | Prescalers, capture/compare, tick-list non-blocking software timers | ⏳ Upcoming |
| **Day 14** | **Week 2 Silicon Bring-Up & Board Diagnostics** | 5-step hardware bring-up sequence, cold resistance, oscilloscope probing, current limit | ⏳ Upcoming |

### ⚙️ Week 3: Data Structures, RTOS & State Machines (Days 15 – 21)
| Module | Topic Focus | Key Concepts & Hardware Insights | Status |
| :---: | :--- | :--- | :---: |
| **Day 15** | **Finite State Machines (FSM)** | Table-driven transition matrices vs switch-case, deterministic event dispatch | ⏳ Upcoming |
| **Day 16** | **Memory Pools & Heap Avoidance** | Fixed-size block allocators, avoiding heap fragmentation and non-deterministic `malloc` | ⏳ Upcoming |
| **Day 17** | **String & Packet Parsing without Heap** | Reentrant tokenizers (`strtok_r`), zero-copy frame slicing, checksum validation | ⏳ Upcoming |
| **Day 18** | **FreeRTOS Task Mechanics & TCB** | Task states, priority preemptive scheduling, stack watermarking (`uxTaskGetStackHighWaterMark`) | ⏳ Upcoming |
| **Day 19** | **FreeRTOS Synchronization: Mutex vs Semaphore** | Priority Inversion, Priority Inheritance protocol, binary vs counting semaphores | ⏳ Upcoming |
| **Day 20** | **FreeRTOS Queues & ISR Context Rules** | `xQueueSendFromISR`, yield from ISR flag, deferred interrupt processing (bottom halves) | ⏳ Upcoming |
| **Day 21** | **System Architecture & Safety Interlocks** | Break-before-make interlocks, capacitive power-fail brownout flush, fault latches | ⏳ Upcoming |

### 🚀 Week 4: Advanced Scenarios & Offer Conversion (Days 22 – 30)
| Module | Topic Focus | Key Concepts & Hardware Insights | Status |
| :---: | :--- | :--- | :---: |
| **Day 22** | **Bootloader Fundamentals & Vector Relocation** | Flash dual-banking, vector table offset (`SCB->VTOR`), application jump validation | ⏳ Upcoming |
| **Day 23** | **Watchdog Timers (IWDG / WWDG) & Brown-Out Reset** | Independent vs window watchdog, windowed kicking loops, brown-out voltage trips | ⏳ Upcoming |
| **Day 24** | **Direct Memory Access (DMA) & Double Buffering** | Ping-pong buffer architectures, DMA transfer complete interrupts, cache coherency | ⏳ Upcoming |
| **Day 25** | **CAN 2.0B Controller & Automotive Telemetry** | 11-bit vs 29-bit identifiers, bit timing, acceptance filters, bus-off auto recovery | ⏳ Upcoming |
| **Day 26** | **Low-Power Modes & Power Management** | Sleep / Stop / Standby modes, clock gating, RTC wake-up interrupts | ⏳ Upcoming |
| **Day 27** | **Data Integrity & Checksum Engines** | Fast lookup-table CRC-32, modular arithmetic check, anti-tampering checksums | ⏳ Upcoming |
| **Day 28** | **Defensive Programming & MISRA-C Safety** | Mandatory type sizes, side-effect avoidance, pointer aliasing, defensive assertions | ⏳ Upcoming |
| **Day 29** | **Live Coding Simulation: Telemetry Packet Engine** | Full 30-minute end-to-end coding test: frame builder, CRC calculation, UART dispatch | ⏳ Upcoming |
| **Day 30** | **30-Day Master Capstone & Cheatsheet** | Complete consolidated embedded interview revision package and quick reference | ⏳ Upcoming |

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

### Day 03 — Bit Manipulation & Silicon Register Mapping
1. **`01_bitwise_macros.c`** — Standard embedded register macros (`SET`, `CLEAR`, `TOGGLE`, `CHECK`, `MODIFY`) and why `1U` avoids signed overflow.
2. **`02_bit_packing_extract.c`** — Bit packing and extraction for telemetry words; why manual masking is preferred over non-portable struct bitfields.
3. **`03_endianness_check_swap.c`** — Runtime Little-Endian vs Big-Endian check; 16-bit and 32-bit byte reversal (`REV16`, `REV32`) for Modbus/CAN.
4. **`04_swap_nibbles.c`** — Swapping upper and lower 4-bit nibbles in an 8-bit byte for 4-bit parallel display buses (e.g. HD44780 LCD).
5. **`05_circular_bit_rotation.c`** — Circular left and right bit rotation (ROL, ROR) for 8-bit and 32-bit words without bit loss.

---


### Day 04 — Volatile Keyword & Compiler Optimizations
1. **`01_volatile_isr_flag.c`** — Volatile Shared Flag between ISR and Main Loop. Without volatile, gcc -O2 caches the flag in a CPU register (e.g. R4), turning 'while(!flag)' into an infinite loop!
2. **`02_hardware_register_access.c`** — Volatile Pointer to Memory-Mapped Peripheral Registers. Hardware registers can change state autonomously (e.g. status flags set by silicon). Volatile prevents dead-code elimination.

---


### Day 05 — Structure Padding, Memory Alignment & Packing
1. **`01_struct_padding_alignment.c`** — Natural 32-Bit Memory Alignment & Padding Waste. Reordering struct members from largest to smallest eliminates padding waste and saves 33% RAM per struct instance on 32-bit MCUs.
2. **`02_pragma_pack_telemetry.c`** — Packed Structs for Network & Fieldbus Serialization. #pragma pack(1) forces exact byte alignment, eliminating padding for over-the-air or RS-485 serial frames.

---


### Day 06 — CPU Interrupt Lifecycle & ISR Rules
1. **`01_interrupt_vector_lookup.c`** — Function Pointer Vector Table Dispatch Simulation. Cortex-M IVT holds 32-bit addresses of ISR functions. Hardware fetches the address directly from Flash upon interrupt assertion.

---


### Day 07 — Week 1 Speed Drills & Consolidation
1. **`01_week1_speed_drill.c`** — 15-Minute Blank Screen Muscle Memory Consolidation. Mastering the top 4 recurring bitwise and memory operations tested in live embedded screening tests.

---


### Day 08 — UART Peripheral & Circular FIFO Ring Buffer
1. **`01_uart_ring_buffer.c`** — Lock-Free SPSC Circular FIFO Ring Buffer. By using power-of-two buffer sizes, modulo '%' (20-40 cycles) is replaced with bitwise '& (SIZE - 1)' (1 cycle)!

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
