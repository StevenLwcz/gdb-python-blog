.cpu cortex-a53
.fpu neon-fp-armv8

.global _start
.text

_start:
    # Integer Imm

    vmov.u8 q0, 1
    vmov.u16 q1, 0x100
    vmov.u32 q2, 0x10000
    vmov.u32 q2, 0x1ff
    vmov.u32 q2, 0x1ffff
    vmov.u64 q3, 0x00ff00ff

    # Float Imm

    vmov.f32 q4, -2.5

    # Vector to Vector

    vmov q5, q2
    vmov d12, d8

    # Vector from General

    mov r0, #255
    vdup.8 q0, r0
    vdup.16 q1, r0
    vdup.32 q2, r0

    # Vector from SIMD scaler

    vdup.8 q7, d0[7]
    vdup.16 q8, d1[3]
    vdup.32 q9, d2[1]

    vmov.u64 q7, 0
    vmov q8, q7
    vmov q9, q7

    vdup.8 d14, d0[6]
    vdup.16 d16, d1[2]
    vdup.32 d18, d2[0]

    # SIMD Scaler from SIMD Scaler

    vmov.u64 q7, #0
    vmov q8, q7
    vmov q9, q7

    vmov.u8 r0, d0[5]
    vmov.8 d14[4], r0
    vmov.u16 r0, d1[2]
    vmov.16 d16[3], r0
    vmov r0, d3[1]
    vmov d18[0], r0

    # Register from vector element

    vmov.s8 r0, d0[7]
    vmov.u8 r1, d0[7]

end:
    mov r0, #0
    mov r7, #1 @ exit
    swi #0

