tty /dev/pts/1
# set style enabled off
set tui border-kind ascii
so ../gdb-python/general-riscv.py
tui new-layout debug1 register 1 src 1 status 0 cmd 1
layout debug1
reg a0 - a4 t0 - t3
reg /x a1
reg pc sp ra gp
b _start_
r
