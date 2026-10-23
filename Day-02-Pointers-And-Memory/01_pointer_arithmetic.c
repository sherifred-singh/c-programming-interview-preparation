/*
 * Problem: Pointer arithmetic and memory traversal.
 *
 * In C, adding 1 to a pointer increments the memory address by sizeof(*ptr) bytes.
 * This demonstrates how different data types scale in memory.
 */

#define __USE_MINGW_ANSI_STDIO 1
#include <stdio.h>
#include <stdint.h>

int main(void)
{
    uint8_t  u8_arr[]  = {0x10, 0x20, 0x30, 0x40};
    uint16_t u16_arr[] = {0x1000, 0x2000, 0x3000, 0x4000};
    uint32_t u32_arr[] = {0x10000000, 0x20000000, 0x30000000, 0x40000000};

    uint8_t  *p8  = u8_arr;
    uint16_t *p16 = u16_arr;
    uint32_t *p32 = u32_arr;

    printf("--- Pointer Arithmetic Scaling ---\n");
    printf("uint8_t pointer step  : %p -> %p (diff: %td byte)\n",
           (void *)p8,  (void *)(p8 + 1),  (char *)(p8 + 1) - (char *)p8);
    printf("uint16_t pointer step : %p -> %p (diff: %td bytes)\n",
           (void *)p16, (void *)(p16 + 1), (char *)(p16 + 1) - (char *)p16);
    printf("uint32_t pointer step : %p -> %p (diff: %td bytes)\n\n",
           (void *)p32, (void *)(p32 + 1), (char *)(p32 + 1) - (char *)p32);

    /* Array traversal using pointer arithmetic */
    printf("Traversing uint16_t array via pointer:\n");
    for (int i = 0; i < 4; i++) {
        printf("  *(p16 + %d) = 0x%04X (at %p)\n", i, *(p16 + i), (void *)(p16 + i));
    }

    return 0;
}
