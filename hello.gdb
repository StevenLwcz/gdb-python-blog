# Make printf() from C programs go to another termnal as to not mess up the gdb session.
# tty /dev/pts/1

source hellotui.py
# source hellotuicmd.py

tui new-layout mylayout hello 1 cmd 1
layout mylayout
