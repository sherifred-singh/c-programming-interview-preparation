/*
 * Problem: Check whether an integer is even or odd.
 *
 * In embedded C, (n & 1) is preferred over (n % 2) because it executes in
 * a single clock cycle and avoids expensive division on MCUs without a hardware divider.
 */

#include <stdio.h>
#include <stdbool.h>

static bool is_even_bitwise(int n)
{
    /* LSB is 0 for even numbers, 1 for odd numbers */
    return (n & 1) == 0;
}

static bool is_even_modulo(int n)
{
    /* Using != 0 handles negative odd numbers properly in C99 */
    return (n % 2 == 0);
}

int main(void)
{
    int samples[] = {42, 17, 0, -13, -24};
    int count = sizeof(samples) / sizeof(samples[0]);

    printf("Even / Odd Check:\n");
    for (int i = 0; i < count; i++) {
        int val = samples[i];
        printf("%4d -> Bitwise: %s | Modulo: %s\n",
               val,
               is_even_bitwise(val) ? "Even" : "Odd",
               is_even_modulo(val) ? "Even" : "Odd");
    }

    return 0;
}
