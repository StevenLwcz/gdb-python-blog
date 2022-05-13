# two versions 
# one to dump x to Tui Window (xwin)
#   only scroll contents if too big for window
# one to do mem dumpn hex with characters to the side (memdump)
#   can scroll address back and forth
# colourise address?
# colourise change of values on step????

GREEN = "\x1b[38;5;47m"
BLUE  = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;15m"
YELLOW = "\x1b[38;5;226m"
RESET = "\x1b[0m"
NL = "\n\n"

fmt_list = ['o', 'x', 'd', 'u', 't', 'f', 'a', 'i', 'c', 's', 'z']

class MemDumpCmd(gdb.Command):
   """memdump expression
display the memory expression in a TUI Window"""

   def __init__(self):
       super().__init__("memdump", gdb.COMMAND_DATA)
       self.window = None

   def set_window(self, window):
       self.window = window

   def invoke(self, arguments, from_tty):
        argv = gdb.string_to_argv(arguments)
        argc = len(argv)
        if argc == 0:
            print("memdump expression")
            return

        n = self.window.tui.height * 8
        try:
            output = gdb.execute(f'x /{n}xb {argv[0]}', False, True)
            self.window.set_title(argv[0])
            self.window.set_display(output)
        except gdb.MemoryError:
            print(f"memdump: Can't read memory at the location {argv[0]}")

 
memdump = MemDumpCmd()

def MemDumpFactory(tui):
    win = MemoryWindow(tui)
    memdump.set_window(win)
    # register create_auto() to be called each time the gdb prompt will be displayed
    # gdb.events.before_prompt.connect(win.create_auto)
    return win

import re

class MemoryWindow(object):

    def __init__(self, tui):
        self.tui = tui
        self.start = 0
        self.horiz = 0
        self.title = ""
        self.list = []
        self.cmd = ""

    def set_display(self, text):
        x = text.replace('\t', ' ')
        x = x.replace('0x', '')
        self.addr = ""
        for line in x.splitlines():
            i = line.index(':')
            # c = bytes.fromhex(line[i + 1:]).decode('ascii', 'replace')
            c = bytes.fromhex(line[i + 1:]).decode('cp437', 'replace')
            c = re.sub('\W', '.', c)
            self.list.append(line + ' ' + c) 

        self.addr = int(line[0:i], 16)
        self.render()

    def set_title(self, text):
        print(text)
        self.cmd = text
        self.title = text

    # def close(self):
        # stop create_auto() being called when the window has been closed
        # gdb.events.before_prompt.disconnect(self.create_auto)

    def vscroll(self, num):
        self.title = self.cmd
        if num + self.start >= 0:
            self.start += num
            if self.start + self.tui.height >= len(self.list):
                self.addr += 8 * num
                try:
                    output = gdb.execute(f"x /{8 * num}xb {self.addr}", False, True)
                    self.set_display(output)
                except gdb.MemoryError:
                    self.addr -= 8 * num
                    self.start -= num
                    self.title = "Can't read any more memory."

            self.render()

    def hscroll(self, num):
        if num > 0 or num < 0 and num + self.horiz >= 0:
            self.horiz += num
            self.render()

    def render(self):
        if not self.tui.is_valid():
            return

        self.tui.title = self.title
        self.tui.erase()

        if self.horiz == 0:
            for l in self.list[self.start:]:
                self.tui.write(l + NL)
        else:
            for l in self.list[self.start:]:
                self.tui.write(l[self.horiz:] )
                self.tui.write(NL)

    # def create_auto(self):
        # self.render()

gdb.register_window_type("memwin", MemDumpFactory)
