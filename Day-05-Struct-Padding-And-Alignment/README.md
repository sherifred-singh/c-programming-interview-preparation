# Day 05: Structure Padding, Memory Alignment & Packing

Understanding natural boundary memory alignment, compiler struct padding, sizeof calculation, #pragma pack(1), and attribute((packed)) for serial frames.

---

## 📋 Program Index & Summary

| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **01** | **`01_struct_padding_alignment.c`** | Natural 32-Bit Memory Alignment & Padding Waste | O(1) | O(1) | Reordering struct members from largest to smallest eliminates padding waste and saves 33% RAM per struct instance on 32-bit MCUs. |
| **02** | **`02_pragma_pack_telemetry.c`** | Packed Structs for Network & Fieldbus Serialization | O(1) | O(1) | #pragma pack(1) forces exact byte alignment, eliminating padding for over-the-air or RS-485 serial frames. |

---

## 💡 Embedded Notes & Key Hardware Takeaways

### 1. Natural 32-Bit Memory Alignment & Padding Waste
- **Key Silicon Insight:** Reordering struct members from largest to smallest eliminates padding waste and saves 33% RAM per struct instance on 32-bit MCUs.
- **Technical Design Question:** *Why do 32-bit ARM cores enforce 4-byte natural alignment?*
- **Engineering Rationale:** Unaligned memory access (e.g. reading 32-bit integer from address 0x20000001) causes a UsageFault exception on Cortex-M0/M0+, or takes multiple bus cycles on Cortex-M3/M4.

### 2. Packed Structs for Network & Fieldbus Serialization
- **Key Silicon Insight:** #pragma pack(1) forces exact byte alignment, eliminating padding for over-the-air or RS-485 serial frames.
- **Technical Design Question:** *What performance hazard occurs when accessing fields of a packed struct?*
- **Engineering Rationale:** Accessing unaligned fields forces the CPU or compiler to generate multiple single-byte reads and shift operations, increasing code size and cycle count.

---

## 🛠 How to Compile & Run

```bash
# Compile all programs in this module with strict C99 warnings
gcc -Wall -Wextra -std=c99 -pedantic 01_struct_padding_alignment.c -o 01_struct_padding_alignment && ./01_struct_padding_alignment
gcc -Wall -Wextra -std=c99 -pedantic 02_pragma_pack_telemetry.c -o 02_pragma_pack_telemetry && ./02_pragma_pack_telemetry
```
