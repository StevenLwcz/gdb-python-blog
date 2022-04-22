set style enabled off
set tui border-kind ascii
b _start
r

so ../gdb-python/vector.py
tui new-layout debug1 vector 1 src 1 status 0 cmd 1
layout debug1

vec q0.u8
vec q1.u16
vec /x q2.u32
vec /x q3.u64
vec q4.f32
vec /x q5.u32
vec q6.f32

vec q7.u8
vec /x q8.u16
vec /x q9.u32
