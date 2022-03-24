.cpu cortex-a53
.fpu neon-fp-armv8

.global _start
.text

_start:
    vmov.u8 q0, #1
    vmov.u16 q1, #2
    vmov.u32 q2, #3
    vmov.u64 q3, #0x00ffff00

    vmov.f32 q4, #1.5
    vadd.f32 q4, q4, q4

    vmov.f64 d10, #2.5   /* q5 */
    vmov.f64 d11, #3.5   /* q5 */

    vmov.u8 d12, #1
    vmov.u16 d13, #2
    vmov.u32 d14, #3
    vmov.u64 d15, #255

    vmov.f32 d16, #1.125
    vmov.f64 d17, #2.625

    vadd.f32 d18, d16, d16
    vadd.f64 d19, d17, d17
end:
    mov r0, #0
    mov r7, #1 @ exit
    swi #0

.data

.align 4
