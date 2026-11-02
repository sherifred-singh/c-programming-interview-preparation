/*
 * ============================================================================
 * Problem: Fixed-Point Exponential Moving Average (EMA) Digital Filter
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>

/* State: State[n] = (alpha * Sample + (256 - alpha) * State[n-1]) >> 8 */
#define EMA_ALPHA 51U /* ~20% smoothing factor (51 / 256) */

static uint16_t ema_filter(uint16_t raw_sample, uint32_t *state)
{
    *state = ((uint32_t)raw_sample * EMA_ALPHA) + (*state * (256U - EMA_ALPHA));
    *state >>= 8U;
    return (uint16_t)(*state);
}

int main(void)
{
    printf("=== Day 12: Fixed-Point Q8 EMA Filter Simulation ===\n\n");

    uint32_t filter_state = 1000U;
    uint16_t noisy_inputs[] = {1000, 1050, 980, 1200, 1020, 1010, 990};

    printf("Raw Input -> Filtered Output:\n");
    for (size_t i = 0; i < sizeof(noisy_inputs)/sizeof(noisy_inputs[0]); i++) {
        uint16_t out = ema_filter(noisy_inputs[i], &filter_state);
        printf(" [%zu]: Raw = %4u  | Filtered = %4u\n", i, noisy_inputs[i], out);
    }
    return 0;
}
