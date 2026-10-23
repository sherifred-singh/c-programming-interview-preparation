# Day 01: Basic C Programs

Essential C programming interview questions covering bitwise operations, loops, arrays, and basic string operations.

## Programs

1. **`01_even_or_odd.c`** - Check even or odd using bitwise `& 1` vs modulo `% 2`.
2. **`02_reverse_integer.c`** - Reverse a 32-bit integer with overflow checks.
3. **`03_palindrome_number.c`** - Check palindrome by reversing only the second half.
4. **`04_factorial.c`** - Iterative factorial up to 20! (avoids recursion stack usage).
5. **`05_prime_number.c`** - Prime check up to `i * i <= n` using pure integer arithmetic.
6. **`06_min_max_array.c`** - Single-pass scan to find minimum and maximum in an array.
7. **`07_reverse_string.c`** - In-place two-pointer string reversal.
8. **`08_count_vowels_consonants.c`** - Character counting with safe `(unsigned char)` casting.
9. **`09_fibonacci_series.c`** - Iterative Fibonacci generation using 3 registers (O(1) memory).
10. **`10_swap_without_temp.c`** - XOR and arithmetic swap with pointer aliasing guard.
11. **`11_count_set_bits.c`** - Count set bits (Brian Kernighan's algorithm) & power-of-two check.

## Embedded Notes & Key Takeaways

- **Bitwise vs Modulo:** `num & 1` executes in 1 cycle on all MCUs; `% 2` can take 20–40 cycles if the core lacks a hardware divider (e.g. Cortex-M0). Also, `(-5 % 2)` is `-1` in C99, so `n % 2 == 1` fails on negative odd numbers.
- **Brian Kernighan's Bit Trick:** `n &= (n - 1)` clears the lowest set bit in a single operation. It loops only as many times as there are 1s ($O(K)$), making it much faster than shifting 32 times. `(n > 0) && ((n & (n - 1)) == 0)` tests if a number is a power of 2 in $O(1)$.
- **Recursion in Firmware:** Avoid recursion (MISRA-C Rule 17.2) due to small MCU stack sizes (1–4 KB). Iteration is always safer.
- **Integer Math over libm:** In `05_prime_number.c`, using `i * i <= n` avoids linking software floating-point emulation for `sqrt()` on targets without a hardware FPU.
- **String Literals vs Arrays:** `char *s = "hi"` puts the string into read-only Flash (`.rodata`). In-place reversal needs a mutable array in RAM: `char s[] = "hi"`.
- **XOR Swap Aliasing:** If `swap(&x, &x)` is called without checking `ptr_a != ptr_b`, the variable is wiped out (`*a ^= *a` evaluates to 0).

## How to Compile & Run

```bash
# Compile any file with GCC
gcc -Wall -Wextra -std=c99 01_even_or_odd.c -o test
./test
```
