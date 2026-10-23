/*
 * Problem: Count vowels, consonants, digits, and spaces in a string.
 *
 * Always cast characters to (unsigned char) when calling ctype functions to
 * prevent undefined behavior on architectures where char is signed.
 */

#define __USE_MINGW_ANSI_STDIO 1
#include <stdio.h>
#include <ctype.h>
#include <stddef.h>

typedef struct {
    int vowels;
    int consonants;
    int digits;
    int spaces;
    int others;
} char_counts_t;

static void count_chars(const char *s, char_counts_t *c)
{
    if (!s || !c) {
        return;
    }

    *c = (char_counts_t){0};

    for (size_t i = 0; s[i] != '\0'; i++) {
        unsigned char ch = (unsigned char)s[i];

        if (isalpha(ch)) {
            unsigned char lower = (unsigned char)tolower(ch);
            if (lower == 'a' || lower == 'e' || lower == 'i' || lower == 'o' || lower == 'u') {
                c->vowels++;
            } else {
                c->consonants++;
            }
        } else if (isdigit(ch)) {
            c->digits++;
        } else if (isspace(ch)) {
            c->spaces++;
        } else {
            c->others++;
        }
    }
}

int main(void)
{
    const char text[] = "STM32 ARM Cortex-M4 @ 180MHz";
    char_counts_t counts;

    count_chars(text, &counts);

    printf("Input: \"%s\"\n", text);
    printf("Vowels: %d | Consonants: %d | Digits: %d | Spaces: %d | Others: %d\n",
           counts.vowels, counts.consonants, counts.digits, counts.spaces, counts.others);

    return 0;
}
