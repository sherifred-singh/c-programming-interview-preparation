/*
 * Problem: Reverse the digits of a 32-bit signed integer.
 *
 * Check for potential overflow before multiplying by 10.
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define INT32_MAX_LIMIT  (2147483647)
#define INT32_MIN_LIMIT (-2147483648)

static bool reverse_integer(int32_t num, int32_t *result)
{
    int32_t rev = 0;

    if (!result) {
        return false;
    }

    while (num != 0) {
        int32_t rem = num % 10;

        /* Check for overflow before multiplying */
        if (rev > INT32_MAX_LIMIT / 10 || (rev == INT32_MAX_LIMIT / 10 && rem > 7)) {
            *result = 0;
            return false;
        }
        if (rev < INT32_MIN_LIMIT / 10 || (rev == INT32_MIN_LIMIT / 10 && rem < -8)) {
            *result = 0;
            return false;
        }

        rev = rev * 10 + rem;
        num /= 10;
    }

    *result = rev;
    return true;
}

int main(void)
{
    int32_t tests[] = {12345, -9876, 1200, 0, 1000000009};
    int count = sizeof(tests) / sizeof(tests[0]);

    for (int i = 0; i < count; i++) {
        int32_t rev = 0;
        if (reverse_integer(tests[i], &rev)) {
            printf("%11d -> %11d\n", tests[i], rev);
        } else {
            printf("%11d -> Overflow\n", tests[i]);
        }
    }

    return 0;
}
