# colourise address?
# colourise change of values on step?

GREEN = "\x1b[38;5;47m"
BLUE  = "\x1b[38;5;4m"
WHITE = "\x1b[38;5;15m"
YELLOW = "\x1b[38;5;154m"
RESET = "\x1b[0m"
NL = "\n\n"

def substr_end_with_ansi(start_off, st):
    """return the end of the string starting from start_off
       will always return the end of line characters"""

    seq = ""
    esc = False
    count = 0
    for i, c in enumerate(st):
        if esc:
            seq += c
            count += 1
            if c == 'm':
               esc = False
        else:
            if i - count >= start_off:
                break

            if c == '\x1b':
                esc = True
                seq = '\x1b'
                count += 1
            elif c == '\n':
                break

    return(seq + st[i:])

class MemDumpCmd(gdb.Command):
   """memdump expression
memdump /FMT expression - as per x GDB command
display the memory expression in a TUI Window"""

   def __init__(self):
       super().__init__("memdump", gdb.COMMAND_DATA)
       self.window = None

   def set_window(self, window):
       self.window = window

   def invoke(self, arguments, from_tty):
        if self.window == None:
            print("memdump: Tui mode not enabled")
            return

        argv = gdb.string_to_argv(arguments)
        argc = len(argv)
        if argc == 0 or argc > 2:
            print("memdump [/FMT] expression")
            return

        try:
            self.window.set_title(arguments, argc)
            self.window.create_display()
        except gdb.error:
            print(f"memdump: syntax error for {arguments}")
            self.window.set_title(arguments, 0)

memdumpCmd = MemDumpCmd()

def MemDumpFactory(tui):
    win = MemoryWindow(tui)
    memdumpCmd.set_window(win)
    # register create_memdump() to be called each time the gdb prompt will be displayed
    gdb.events.before_prompt.connect(win.update_memdump)
    return win

import re

class MemoryWindow(object):

    pattern = re.compile('[^\w\x20-\x7e]')

    def __init__(self, tui):
        self.tui = tui
        self.start = 0
        self.horiz = 0
        self.title = ""
        self.list = []
        self.cmd = ""
        self.mode = None
        self.create_display = self.set_default

    def set_title(self, text, num):
        self.start = 0
        self.horiz = 0
        self.cmd = text
        self.title = text
        if num == 2:
            self.mode = self.vscroll_1
            self.create_display = self.create_display_1
        elif num == 1:
            self.mode = self.vscroll_2
            self.create_display = self.create_display_2
        else:
            self.mode = None
            self.create_display = self.set_default

    def set_default(self):
        self.tui.title = 'Memory Dump'

    def close(self):
        # stop create_memdump() being called when the window has been closed
        gdb.events.before_prompt.disconnect(self.update_memdump)

    def hscroll(self, num):
        if num > 0 or num < 0 and num + self.horiz >= 0:
            self.horiz += num
            self.render()

    def vscroll(self, num):
        self.mode(num)

    def render(self):
        if not self.tui.is_valid():
            return

        self.tui.title = self.title
        self.tui.erase()

        if self.horiz == 0:
            for l in self.list[self.start:]:
                self.tui.write(l)
        else:
            for l in self.list[self.start:]:
                self.tui.write(substr_end_with_ansi(self.horiz, l))

    def update_memdump(self):
        self.create_display()

# Handle x command with 2 arguments
    def vscroll_1(self, num):
        self.title = self.cmd
        if num > 0 and num + self.start < len(self.list) or \
           num < 0 and num + self.start >= 0:
            self.start += num

            self.render()

    def set_display_1(self, text):
        self.list.clear()
        x = text.replace('\t', ' ')
        for line in x.splitlines():
            i = line.index(':')
            self.list.append(BLUE + line[:i] + RESET + line[i:] + NL) 

        self.render()

    def create_display_1(self):
        try:
            output = gdb.execute(f'x {self.cmd}', False, True)
            self.set_display_1(output)
        except gdb.MemoryError:
            print(f"memdump: Can't read memory at the location for {self.cmd}")


# Memory dump at address
    def vscroll_2(self, num):
        if num + self.start >= 0:
            self.start += num
            if self.start + self.tui.height >= len(self.list):
                self.addr += 8 * num
                try:
                    output = gdb.execute(f"x /{8 * num}xb {self.addr}", False, True)
                    self.set_display_2(output, True)
                except gdb.MemoryError:
                    self.addr -= 8 * num
                    self.start -= num
                    self.title = "Can't read any more memory."

            self.render()

    def set_display_2(self, text, append=False):
        if not append:
            self.list.clear()
            self.cmd = text[0:text.index(':')] # used for update_memdump()

        x = text.replace('\t', ' ')
        x = x.replace('0x', '')

        for line in x.splitlines():
            i = line.index(':')
            # c = bytes.fromhex(line[i + 1:]).decode('ascii', 'replace')
            c = bytes.fromhex(line[i + 1:]).decode('cp437', 'replace')
            c = MemoryWindow.pattern.sub('.', c)
            self.list.append(BLUE + line[:i] + RESET + line[i:] + ' ' + YELLOW + c + RESET + NL) 

        self.addr = int(line[0:i], 16)    # used for vscroll_2()
        self.render()

    def create_display_2(self):
        l = len(self.list)
        n = 8 * self.tui.height if l == 0 else l * 8
        try:
            output = gdb.execute(f'x /{n}xb {self.cmd}', False, True)
            self.set_display_2(output)
        except gdb.MemoryError:
            print(f"memdump: Can't read memory at the location for {self.cmd}")

gdb.register_window_type("memdump", MemDumpFactory)
