/*
 * Problem: Check if an integer is a palindrome without converting it to a string.
 *
 * Instead of reversing the entire number (which could overflow), we reverse
 * only the second half.
 */

#include <stdio.h>
#include <stdbool.h>

static bool is_palindrome(int n)
{
    /* Negative numbers and non-zero numbers ending in 0 cannot be palindromes */
    if (n < 0 || (n % 10 == 0 && n != 0)) {
        return false;
    }

    int rev_half = 0;
    while (n > rev_half) {
        rev_half = rev_half * 10 + (n % 10);
        n /= 10;
    }

    /* Even length: n == rev_half. Odd length: n == rev_half / 10 */
    return (n == rev_half || n == rev_half / 10);
}

int main(void)
{
    int tests[] = {121, -121, 10, 12321, 0, 1221, 12345};
    int count = sizeof(tests) / sizeof(tests[0]);

    for (int i = 0; i < count; i++) {
        printf("%7d -> %s\n", tests[i], is_palindrome(tests[i]) ? "Palindrome" : "Not Palindrome");
    }

    return 0;
}
