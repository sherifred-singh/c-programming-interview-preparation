/*
 * Problem: Swap two numbers without a temporary variable (XOR and arithmetic).
 *
 * Warning: XOR swap fails if both pointers point to the same memory location
 * (&a == &b), as *a ^= *a zeroes the value. Always guard against aliasing.
 */

#include <stdio.h>

static void swap_xor(int *a, int *b)
{
    if (a && b && a != b) {
        *a ^= *b;
        *b ^= *a;
        *a ^= *b;
    }
}

static void swap_arithmetic(int *a, int *b)
{
    if (a && b && a != b) {
        *a = *a + *b;
        *b = *a - *b;
        *a = *a - *b;
    }
}

int main(void)
{
    int x = 25, y = 70;
    printf("Before XOR swap: x = %d, y = %d\n", x, y);
    swap_xor(&x, &y);
    printf("After  XOR swap: x = %d, y = %d\n\n", x, y);

    int m = 100, n = -45;
    printf("Before arithmetic swap: m = %d, n = %d\n", m, n);
    swap_arithmetic(&m, &n);
    printf("After  arithmetic swap: m = %d, n = %d\n\n", m, n);

    /* Aliasing safety test */
    int val = 50;
    swap_xor(&val, &val);
    printf("Aliasing test (swap_xor with same address): val = %d\n", val);

    return 0;
}
