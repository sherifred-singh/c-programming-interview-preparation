/*
 * ============================================================================
 * Problem: 5-Step Hardware Board Bring-Up Sequence
 * ============================================================================
 */

#include <stdio.h>
#include <stdbool.h>

typedef struct {
    bool visual_microscope_pass;
    bool cold_resistance_ok;      /* > 10 kOhm VDD to GND */
    bool current_limit_50ma_safe; /* Consumes < 50mA */
    bool crystal_osc_verified;    /* Clock frequency verified on scope */
    bool swd_debugger_locked;     /* SWD IDCODE read */
} board_bringup_t;

static bool verify_board_health(const board_bringup_t *check)
{
    if (!check->visual_microscope_pass) { printf("FAIL: Solder bridge or polarity reverse detected!\n"); return false; }
    if (!check->cold_resistance_ok)      { printf("FAIL: Short circuit detected on VDD rail!\n"); return false; }
    if (!check->current_limit_50ma_safe) { printf("FAIL: Excessive current draw (>50mA)!\n"); return false; }
    if (!check->crystal_osc_verified)    { printf("FAIL: Oscillator not oscillating!\n"); return false; }
    if (!check->swd_debugger_locked)     { printf("FAIL: SWD cannot read MCU IDCODE!\n"); return false; }
    return true;
}

int main(void)
{
    printf("=== Day 14: 5-Step Silicon Bring-Up Diagnostics ===\n\n");
    board_bringup_t board = {true, true, true, true, true};
    if (verify_board_health(&board)) {
        printf("SUCCESS: Board Bring-Up Complete. Ready for Firmware Flashing!\n");
    }
    return 0;
}
