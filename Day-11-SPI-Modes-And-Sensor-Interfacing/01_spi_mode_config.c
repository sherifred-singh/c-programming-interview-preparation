/*
 * ============================================================================
 * Problem: SPI Bus Mode Configuration & Edge Timing Simulator
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>

typedef enum {
    SPI_MODE_0 = 0, /* CPOL = 0, CPHA = 0: Idle Low,  Sample on Rising  */
    SPI_MODE_1 = 1, /* CPOL = 0, CPHA = 1: Idle Low,  Sample on Falling */
    SPI_MODE_2 = 2, /* CPOL = 1, CPHA = 0: Idle High, Sample on Falling */
    SPI_MODE_3 = 3  /* CPOL = 1, CPHA = 1: Idle High, Sample on Rising  */
} spi_mode_t;

static void print_spi_mode_details(spi_mode_t mode)
{
    uint8_t cpol = (mode >> 1) & 1;
    uint8_t cpha = mode & 1;

    printf("Mode %d: CPOL=%d (%s), CPHA=%d (%s)\n",
           mode, cpol, cpol ? "Idle HIGH" : "Idle LOW",
           cpha, cpha ? "Sample 2nd Edge" : "Sample 1st Edge");
}

int main(void)
{
    printf("=== Day 11: SPI Bus Modes (0-3) Timing Matrix ===\n\n");
    for (int m = 0; m <= 3; m++) {
        print_spi_mode_details((spi_mode_t)m);
    }
    return 0;
}
