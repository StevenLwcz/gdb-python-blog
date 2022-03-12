/* Demo for Blog 3 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

struct Sector {
  int angle; // deg
  int radius;
};

float sectorArea(struct Sector s);
float arcLength(struct Sector s);

float sectorArea(struct Sector s)
{
    float area = M_PI * s.radius * s.radius;
    area = area * s.angle / 360;
    return area;
}

float arcLength(struct Sector s)
{
    float length = 2 * M_PI * s.radius;
    length = length * s.angle / 360;
    return length;
}

struct Sector circle1 = {360, 10};
static struct Sector circle2 = {360, 5};

int main()
{
    char buff[] = "Hello Circle Program\0";
    char *p1 = buff;

    typedef struct Sector Sector;

    Sector s1 = {180, 10};
    Sector s2 = {45, 10};

    float area = sectorArea(s1);
    float length = arcLength(s1);

    area = sectorArea(s2);
    length = arcLength(s2);

    for (int a = 0; a <= 360; a += 10)
    {
        s1.angle = a;
        area = sectorArea(s1);
    }

    area = sectorArea(circle1);

    if (area > 0)
    {
        int len = arcLength(circle1);
        len = len + 1;
        length = len + 1;
    }

    area = sectorArea(circle2);

    if (area > 0)
    {
        int len = arcLength(circle2);
        len = len + 1;
        if (len > 10)
        {
            int len1 = arcLength(circle2);
            len1 = len1 + 1;
            length = len1 + 1;
        }
    }

    exit(0);
}
