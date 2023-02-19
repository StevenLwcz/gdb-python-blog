.text
.global _start

.equ CH_0, 48
.equ CH_MINUS, 45
.equ stdout, 1
.equ syswrite, 64
.equ sysexit, 93 
.include "macro.m"
 
.option push
.option norelax
_initreg
.option pop

_start_:
   la a1, helloworld
   li a2, 13
   call print

   li a0, 123456
   call itoa
   call print
   call printnl

   li a0, -123456
   call itoa
   call print
   call printnl

end:
    li a0, 0 # return code
    li a7, sysexit
    ecall

/* integer to ascii
 * input  a0 integer
 * output a1 address of string
 *        a2 length of string
 */
itoa:
    la a1, itoa_end
    li t0, 10
    slti t2, a0, 0    # 1 = neg
    bgez a0, loop
    neg a0, a0
loop:
    rem t1, a0, t0
    add t1, t1, CH_0
    sb t1, (a1)
    addi a1, a1, -1
    div a0, a0, t0
    bgtz a0, loop

    beqz t2, itoa_1
    li t1, CH_MINUS
    sb t1, (a1)
    addi a1, a1, -1

itoa_1:
    la a2, itoa_end
    sub a2, a2, a1
    ret

/* print to stdout
 * input a1 = address of string to pint
 *       a2 = length 
 */
print:
    li a0, stdout    # stdout
    li a7, syswrite  # print
    ecall
    ret

/* print new line character to stdout */
printnl:
    li a0, stdout
    la a1, newline
    li a2, 1
    li a7, syswrite
    ecall
    ret

.data
    .balign 4
helloworld: .ascii "Hello World!\n"
    .balign 4
newline: .ascii "\n"
    .balign 4
    .skip 20
itoa_end:
    .skip 1
