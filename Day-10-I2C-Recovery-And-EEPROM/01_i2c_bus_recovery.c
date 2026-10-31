/*
 * ============================================================================
 * Problem: I2C Bus Stuck-Low Recovery via 9 SCL Clock Pulses
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

/* Simulated GPIO Bit-Banging */
static void SCL_Set(bool high) { printf(" SCL -> %s\n", high ? "HIGH" : "LOW"); }
static void SDA_Set(bool high) { printf(" SDA -> %s\n", high ? "HIGH" : "LOW"); }
static bool SDA_Read(void)     { return true; /* Assume freed */ }

static void i2c_bus_clear_recovery(void)
{
    printf("1. Configuring SCL and SDA as open-drain GPIO outputs...\n");
    SDA_Set(true);

    printf("2. Clocking SCL 9 times to force stuck slave to release SDA...\n");
    for (int i = 0; i < 9; i++) {
        SCL_Set(false);
        SCL_Set(true);
        if (SDA_Read()) {
            printf(" -> Slave released SDA line after %d clock pulses!\n", i + 1);
            break;
        }
    }

    printf("3. Generating STOP condition (SDA low -> SCL high -> SDA high)...\n");
    SDA_Set(false);
    SCL_Set(true);
    SDA_Set(true);
    printf("4. I2C Bus Restored Cleanly!\n");
}

int main(void)
{
    printf("=== Day 10: Senior I2C 9-Clock Bus Recovery Routine ===\n\n");
    i2c_bus_clear_recovery();
    return 0;
}
