/*
 * ============================================================================
 * Problem: Static Fixed-Size Block Memory Pool
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define BLOCK_SIZE  32U
#define BLOCK_COUNT 4U

typedef struct Block {
    struct Block *next;
} block_t;

static uint8_t s_memory_pool[BLOCK_COUNT * BLOCK_SIZE];
static block_t *s_free_list_head = NULL;

static void pool_init(void)
{
    s_free_list_head = (block_t *)&s_memory_pool[0];
    block_t *curr = s_free_list_head;
    for (size_t i = 1; i < BLOCK_COUNT; i++) {
        curr->next = (block_t *)&s_memory_pool[i * BLOCK_SIZE];
        curr = curr->next;
    }
    curr->next = NULL;
}

static void *pool_alloc(void)
{
    if (!s_free_list_head) return NULL; /* Out of memory */
    void *ptr = s_free_list_head;
    s_free_list_head = s_free_list_head->next;
    return ptr;
}

static void pool_free(void *ptr)
{
    if (!ptr) return;
    block_t *block = (block_t *)ptr;
    block->next = s_free_list_head;
    s_free_list_head = block;
}

int main(void)
{
    printf("=== Day 16: Fixed-Size Block Memory Pool ===\n\n");
    pool_init();

    void *b1 = pool_alloc();
    void *b2 = pool_alloc();
    printf("Allocated Block 1 at %p\n", b1);
    printf("Allocated Block 2 at %p\n", b2);

    pool_free(b1);
    printf("Freed Block 1.\n");

    void *b3 = pool_alloc();
    printf("Re-allocated Block 3 at %p (Reused freed block in O(1)!)\n", b3);

    return 0;
}
