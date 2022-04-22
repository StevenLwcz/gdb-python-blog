set style enabled off
b _start
r
so ../gdb-python/vector.py
tui new-layout debug1 vector 1 src 1 status 0 cmd 1
layout debug1

vec v0.b.u
vec v1.b.u
vec v2.h.u
vec v3.h.u
vec /x v4.s.u
vec /x v5.s.u
vec /x v6.d.u
vec /x v7.d.u

vec v8.h.f
vec v9.h.f
vec v10.s.f
vec v11.s.f
vec v12.d.f
vec v13.d.f

