/*
 * Problem: Reverse a null-terminated string in-place using two pointers.
 *
 * String literals (char *s = "hi") live in read-only Flash/ROM (.rodata) and
 * cause a HardFault if modified. In-place reversal requires a mutable array (char s[]).
 */

#include <stdio.h>
#include <string.h>

static void reverse_string(char *str)
{
    if (!str) {
        return;
    }

    size_t len = strlen(str);
    if (len <= 1) {
        return;
    }

    size_t left = 0;
    size_t right = len - 1;

    while (left < right) {
        char tmp = str[left];
        str[left] = str[right];
        str[right] = tmp;
        left++;
        right--;
    }
}

int main(void)
{
    char word1[] = "Embedded";
    char word2[] = "Firmware";
    char word3[] = "A";

    printf("[%s] -> ", word1);
    reverse_string(word1);
    printf("[%s]\n", word1);

    printf("[%s] -> ", word2);
    reverse_string(word2);
    printf("[%s]\n", word2);

    printf("[%s] -> ", word3);
    reverse_string(word3);
    printf("[%s]\n", word3);

    return 0;
}
