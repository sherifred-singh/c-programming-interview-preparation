/*
 * Problem: Understanding 'const' qualifiers with pointers.
 *
 * 1. const int *ptr       -> Pointer to constant data (data cannot change, pointer can move).
 * 2. int * const ptr       -> Constant pointer (pointer cannot move, data can change).
 * 3. const int * const ptr -> Constant pointer to constant data (neither can change).
 */

#include <stdio.h>

int main(void)
{
    int val1 = 10;
    int val2 = 20;

    /* 1. Pointer to constant integer */
    const int *ptr_to_const = &val1;
    printf("1. Pointer to const: *ptr_to_const = %d\n", *ptr_to_const);
    ptr_to_const = &val2; /* OK: pointer itself is mutable */
    printf("   After moving pointer: *ptr_to_const = %d\n", *ptr_to_const);
    /* *ptr_to_const = 30; -> Compiler Error: assignment of read-only location */

    /* 2. Constant pointer to integer */
    int * const const_ptr = &val1;
    *const_ptr = 50; /* OK: pointed data is mutable */
    printf("2. Const pointer: *const_ptr = %d (val1 modified)\n", *const_ptr);
    /* const_ptr = &val2; -> Compiler Error: assignment of read-only variable */

    /* 3. Constant pointer to constant integer */
    const int * const fixed_ptr = &val2;
    printf("3. Const pointer to const: *fixed_ptr = %d\n", *fixed_ptr);
    /* *fixed_ptr = 99; -> Error */
    /* fixed_ptr = &val1; -> Error */

    return 0;
}
