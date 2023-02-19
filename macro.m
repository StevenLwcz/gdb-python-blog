.macro _initreg
_start:
   li a0, 0
   li a1, 0
   li a2, 0
   li a3, 0
   li t0, 0
   li t1, 0
   li t2, 0
   li t3, 0
   li s0, 0
   li s1, 0
   li s2, 0
   li s3, 0
   li ra, 0
   la gp, __global_pointer$
.endm
