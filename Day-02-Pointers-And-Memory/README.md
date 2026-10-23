# Day 02: Pointers & Memory Architecture

Focuses on pointer arithmetic, scaling rules, and `const` qualification patterns commonly tested in embedded systems interviews.

## Programs

1. **`01_pointer_arithmetic.c`** - Pointer increment scaling based on type size (`sizeof(*ptr)`).
2. **`02_const_pointers.c`** - Differentiating `const int *ptr`, `int * const ptr`, and `const int * const ptr`.

## Key Embedded Concepts

- **Scaling Rule:** In C, `ptr + 1` increases the actual memory address by `sizeof(*ptr)` bytes (e.g. +1 for `uint8_t`, +2 for `uint16_t`, +4 for `uint32_t`).
- **Read-from-right rule for `const`:**
  - `const int *p`: Pointer to constant int (data protected from accidental writes).
  - `int * const p`: Constant pointer to int (fixed address, useful for hardware register pointers).
  - `const int * const p`: Fixed address pointing to read-only data (e.g. Flash lookup table pointer).

## How to Compile & Run

```bash
gcc -Wall -Wextra -std=c99 01_pointer_arithmetic.c -o test1
./test1

gcc -Wall -Wextra -std=c99 02_const_pointers.c -o test2
./test2
```
