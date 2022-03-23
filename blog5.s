.text
.globl _start

_start:
    movi v0.16b, 252
    movi v1.8h,  253
    movi v2.4s,  254
    movi v3.2d,  255

    // fmov v4.8h, 1.0 // not supported on CorTex-a53 (Pi 3) or CorTex-a72 (Pi 4)
    fmov v5.4s, 2.0
    fmov v6.2d, 3.0

end:
    mov     x0, #0      /* status */
    mov     x8, #93     /* exit() */
    svc     #0          
