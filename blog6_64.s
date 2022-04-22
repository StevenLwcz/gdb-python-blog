.cpu cortex-a76
.text
.globl _start

_start:
    # Integer Immediate

    movi v0.16b, 1
    movi v2.8h,  1, lsl 8      // 0x100
    movi v4.4s,  1, lsl 24     // 0x1000000
    movi v5.4s,  1, msl 8      // 0x1ff       shift ones
    movi v4.4s,  1, msl 16     // 0x1ffff     shift ones
    movi v6.2d,  0x00ff00ff

    # Float Immediate 

    fmov v8.8h, 1.5
    fmov v10.4s, -2.5
    fmov v12.2d, 3.5

    # Vector from Vector

    mov v3.16b, v2.16b
    mov v9.8b,  v8.8b

    # Vector from General

    mov x0, 129
    dup v0.16b, w0
    dup v2.8h, w0
    dup v4.4s, w0
    dup v6.2d, x0

    # Vector from Vector Element

    dup v1.16b, v0.b[9]
    dup v3.8h, v2.h[4]
    dup v5.4s, v4.s[3]
    dup v7.2d, v6.d[1]

    # reset some vectors

    movi v0.16b, 255
    mov v2.16b, v0.16b
    mov v4.16b, v0.16b
    mov v6.16b, v0.16b

    # Vector Element from Vector Element

    ins v0.b[3], v1.b[15]
    ins v2.h[2], v3.h[7]
    ins v4.s[3], v5.s[3]
    ins v6.d[1], v7.d[0]

    # Vector Element from General Register

    movz x0, 0x6666
    ins v0.b[4], w0
    ins v2.h[3], w0
    ins v4.s[2], w0
    ins v6.d[1], x0

    # General Register from Vector Element

    smov w0, v0.b[7]   // b or h 
    smov x1, v0.b[7]   // b, h or s
    umov w2, v0.b[7]   // b, h or s
    umov x3, v6.d[0]   // d

    # Scalar from Vector Element

    dup b1, v0.b[0]
    dup h9, v8.h[3]
    dup s11, v10.s[2]
    dup d13, v12.d[0]

end:
    mov     x0, #0      /* status */
    mov     x8, #93     /* exit */
    svc     #0          
