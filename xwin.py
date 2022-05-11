# two versions 
# one to dump x to window (hexdump)
#   only scroll contents if too big for window
# one to do hex dump with characters to the side (xwin)
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

class XWCmd(gdb.Command):
   """xw [/FMT] expression
/FMT as per GDB command x.
display the memory in a TUI Window"""

   def __init__(self):
       super().__init__("xw", gdb.COMMAND_DATA)
       self.window = None

   def set_window(self, window):
       self.window = window

   def invoke(self, arguments, from_tty):
        argv = gdb.string_to_argv(arguments)
        argc = len(argv)
        if argc == 0:
            print("xw expression")
            return

        n = self.window.tui.height * 8
        output = gdb.execute(f"x /{n}xb {argv[0]}", False, True)
        self.window.set_display(output)
 
xwin = XWCmd()

def AutoWinFactory(tui):
    win = MemoryWindow(tui)
    xwin.set_window(win)
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

    # def close(self):
        # stop create_auto() being called when the window has been closed
        # gdb.events.before_prompt.disconnect(self.create_auto)

    def vscroll(self, num):
        if num > 0 and num + self.start < len(self.list) or \
           num < 0 and num + self.start >= 0:
            self.start += num
            if num > 0:
                self.addr += 8
                output = gdb.execute(f"x /8xb {self.addr}", False, True)
                self.set_display(output)

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

gdb.register_window_type("xwin", AutoWinFactory)
