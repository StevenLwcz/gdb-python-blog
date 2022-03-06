# tty /dev/pts/1
b main
run
so watchwin-basic.py
tui new-layout debug1 watch 1 src 1 status 0 cmd 1
layout debug1
# watch s1 s2 buff p1 area length
