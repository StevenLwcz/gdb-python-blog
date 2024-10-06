
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int i1 = 0x445599;
char *s1 = "Red Orange Yellow Green Blue Indigo Violet\n";
char c[] = {'1', '2', '3', '4', '5', '6'};
const int i2 = 0x224488;

void main()
{
    char a[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g'};
    int b = 100;
    char *s2 = malloc(1024);
    memset(s2, 'x', 1024);
    strcpy(s2, s1);
    a[2] = 'z';
    b = 101;
    a[3] = 'y';
    b = 102;
    a[4] = 'x';
    exit(0);
}
