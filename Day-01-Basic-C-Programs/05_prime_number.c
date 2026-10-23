/*
 * Problem: Check if a number is prime in O(sqrt(n)) time.
 *
 * Uses integer math (i * i <= n) instead of sqrt() to avoid pulling in
 * floating-point library emulation on MCUs without an FPU.
 */

#include <stdio.h>
#include <stdbool.h>

static bool is_prime(int n)
{
    if (n <= 1) {
        return false;
    }
    if (n <= 3) {
        return true;
    }
    if (n % 2 == 0 || n % 3 == 0) {
        return false;
    }

    /* Check divisors of form 6k +/- 1 */
    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) {
            return false;
        }
    }

    return true;
}

int main(void)
{
    int tests[] = {1, 2, 3, 4, 17, 25, 49, 97, 100, 101};
    int count = sizeof(tests) / sizeof(tests[0]);

    for (int i = 0; i < count; i++) {
        printf("%3d -> %s\n", tests[i], is_prime(tests[i]) ? "Prime" : "Not Prime");
    }

    return 0;
}
