
#include <stdio.h>
#include <stdlib.h>

void main()
{
    char a[] = {'a', 'b', 'c', 'd', 'e', 'f'};
    int b = 100;
    a[2] = 'z';
    b = 101;
    a[3] = 'y';
    b = 102;
    a[4] = 'x';
    exit(0);
}
