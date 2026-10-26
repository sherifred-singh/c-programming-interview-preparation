# Day 03: Bit Manipulation & Silicon Register Mapping

Comprehensive collection of low-level bit manipulation techniques, register masking macros, telemetry field packing, endianness conversion, and circular bit rotations essential for Embedded Firmware and Systems Engineer interviews.

---

## 📋 Program Index & Summary

| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **01** | **`01_bitwise_macros.c`** | Silicon Register Macros | $O(1)$ | $O(1)$ | Mandatory `1U` to avoid signed overflow; Read-Modify-Write ISR race conditions. |
| **02** | **`02_bit_packing_extract.c`** | Telemetry Field Packing | $O(1)$ | $O(1)$ | Deterministic portable serialization vs compiler-dependent C struct bitfields. |
| **03** | **`03_endianness_check_swap.c`** | Endianness Check & Swap | $O(1)$ | $O(1)$ | Little-Endian MCU (ARM) vs Big-Endian Network/Fieldbus (Modbus, CAN). |
| **04** | **`04_swap_nibbles.c`** | 8-Bit Nibble Swap | $O(1)$ | $O(1)$ | Split-byte communication for 4-bit parallel display buses (e.g. HD44780 LCD). |
| **05** | **`05_circular_bit_rotation.c`** | Circular ROL & ROR | $O(1)$ | $O(1)$ | GCC rotation idiom compiles to single-cycle native ARM `ROR` assembly instruction. |

---

## 💡 Embedded Notes & Key Hardware Takeaways

### 1. The `1U` Rule and Signed Integer Shift Undefined Behavior
In standard C99 (ISO/IEC 9899 §6.5.7):
- An unscoped integer literal `1` defaults to `signed int`.
- If a 32-bit MCU attempts `1 << 31`, the shift moves into the sign bit. Shifting a `1` into or past the sign bit of a signed integer produces **undefined behavior**.
- On 16-bit microcontrollers (e.g., PIC24 or dsPIC), `1 << 12` can overflow if `int` is 16-bit.
- **Rule:** Always affix `U` or `UL`: `#define SET_BIT(reg, bit) ((reg) |= (1U << (bit)))`.

### 2. The Read-Modify-Write (RMW) Hazard in Shared Peripheral Registers
When you write `PORTA |= (1U << 5);`, the CPU executes three distinct assembly instructions:
1. `LDR R0, [PORTA]` (Read)
2. `ORR R0, R0, #0x20` (Modify)
3. `STR R0, [PORTA]` (Write)

> [!WARNING]
> If a high-priority interrupt (ISR) triggers between step 1 and step 3, modifying another pin on `PORTA`, the subsequent `STR` in `main()` will overwrite and destroy the ISR's change!
> **Solution:** Use atomic bit-set / bit-clear registers provided by hardware (e.g. STM32 `GPIOx->BSRR`) or disable interrupts during non-atomic RMW sequences.

### 3. Bitfields vs Manual Bit Shifts for Packets
While `struct { uint16_t id:3; uint16_t mode:2; }` looks clean in C syntax, **MISRA-C and senior firmware architects forbid struct bitfields for communication protocols**:
- The C standard explicitly leaves bitfield ordering within a storage unit (LSB-first vs MSB-first) **implementation-defined**.
- Endianness differences between sender and receiver silently scramble data.
- **Rule:** Always use explicit bit shifts and bit masks (`(val & MASK) << SHIFT`) for serial telemetry and register maps.

### 4. Endianness in Industrial Fieldbuses
- **ARM Cortex-M:** Little-Endian by default (Least Significant Byte at lowest address).
- **Modbus RTU / RS-485 & CAN / Ethernet:** Big-Endian (Network Byte Order, MSB transmitted first).
- Incoming 16-bit and 32-bit words must be byte-swapped:
  ```c
  uint16_t rev16 = ((raw & 0x00FFU) << 8) | ((raw & 0xFF00U) >> 8);
  ```

---

## 🛠 How to Compile & Run

All programs compile cleanly with strict standard C99 flags:

```bash
# Compile any program with GCC
gcc -Wall -Wextra -std=c99 -pedantic 01_bitwise_macros.c -o test_macros
./test_macros

# Compile and run Telemetry Bit Packing
gcc -Wall -Wextra -std=c99 -pedantic 02_bit_packing_extract.c -o test_pack
./test_pack

# Compile and run Endianness Detection
gcc -Wall -Wextra -std=c99 -pedantic 03_endianness_check_swap.c -o test_endian
./test_endian
```
