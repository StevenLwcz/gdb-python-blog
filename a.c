#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// read only
const int i1 = 0xfecaadbe; // 4
const long int i2 = 0x8877665544332211; // 8

// data
int i3 = 0x11223344;;
char *s1 = "@ Red Orange Yellow Green Blue Indigo Violet @"; // literal in read only
char c[] = {'g', 'l', 'o', 'b', 'a', 'l'};

// bss
char d[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0 ,0 ,0 ,0 ,0};
int i4;

// parameters in stack area (or registers)
int func1(int p1, int p2)
{
    // local items in stack area
    int l1 = p1;
    int l2 = p2;
    char d[] = {'f', 'u', 'n', 'c', '1', ' '}; // literal copied from read only
    return l1 + l2;
}

void main(int argc, char *argv[])
{
    // locals in stack area
    char a[] = {'i', 'n', ' ', 'm', 'a', 'i', 'n'}; // literal copied from read only
    int i5 = 100;
    // memory allocated on heap
    char *s2 = malloc(1024); // heap
    memset(s2, 'x', 1024);
    strcpy(s2, s1);
    s2 = malloc(1024);
    memset(s2, 'y', 1024);
    s2 = malloc(1024);
    memset(s2, 'z', 1024);
    printf("* Cyan Yellow Magenta *\n"); // literal in read only
    d[10] = 10;
    d[8] = 8;
    a[2] = 'z';
    a[3] = 'y';
    i5 = 101;
    i5 = func1(i5, i5);
    exit(0);
}
