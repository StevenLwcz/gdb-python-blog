NL = "\n"

GREEN = "\x1b[38;5;47m"
BLUE  = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;15m"
YELLOW = "\x1b[38;5;226m"
RESET = "\x1b[0m"
VIEWLINELEN = 16


import re
pattern = re.compile(r'[\x00-\x1f\x7f-\x9f]')

class MemViewCmd(gdb.Command):
    """memview expression
Memory view at the address of the expression"""

    def __init__(self):
        super(MemViewCmd, self).__init__("memview", gdb.COMMAND_USER)
        self.win = None

    def set_win(self, win):
        self.win = win

    def invoke(self, arguments, from_tty):
        if gdb.selected_inferior().pid == 0:
            print("memview: no program running")
            return

        if len(arguments) == 0:
            print("memview: expression")
            return

        try:
            expr = gdb.parse_and_eval(arguments)
        except gdb.error:
            print("memview: can't evaluate {arguments}")
            return

        addr = expr.address if expr.address != None else expr

        if self.win == None: 
            gdb.execute("layout memview")

        if not self.win.tui.is_valid():
            gdb.execute("layout memview")

        n = self.win.tui.height * VIEWLINELEN 
        try:
            mv = gdb.selected_inferior().read_memory(addr, n)
        except gdb.MemoryError:
            print(f"memview: can't read memory at {hex(addr)}")
            return

        self.win.set_title(arguments)
        self.win.set_display(addr)

        if not self.win.auto:
            gdb.events.before_prompt.connect(self.win.auto_view)
            self.win.auto = True

# gdb.events.exited.connect(self.win.close_inferior)
# gdb.events.exited.disconnect(self.close_inferior)

memViewCmd = MemViewCmd()

class MemViewWindow(object):

    def __init__(self, tui):
        self.tui = tui
        self.tui.title = "Memory View"
        self.buff = "Use (gdb) memview expression"
        self.addr = 0
        self.auto = False

    def set_title(self, args):
        self.tui.title = args

    def render(self):
        if not self.tui.is_valid():
            return

        self.tui.write(self.buff, True)

    def auto_view(self):
        self.set_display(self.addr)

    def set_display(self, addr):
        n = self.tui.height * VIEWLINELEN 
        try:
            mv = gdb.selected_inferior().read_memory(addr, n)
        except gdb.MemoryError:
            return

        self.addr = addr
        self.buff = ""
        for i in range(0, n, VIEWLINELEN):
            m = mv[i:i + VIEWLINELEN]
            text = pattern.sub('.', m.tobytes().decode('latin-1'))
            self.buff+=f"{GREEN}{hex(addr + i)}: {BLUE}{m.hex(' ')}{RESET} {text}\n"

        self.render()

    def close(self):
        try:
            gdb.events.before_prompt.disconnect(self.auto_view)
            self.auto = False
        except SystemError as e:
            pass

    def vscroll(self, num):
        addr = self.addr + num * VIEWLINELEN 
        self.set_display(addr)

    def hscroll(self, num):
        pass

    def click(self, x, y, button):
        pass

# Factory Method
def MemViewFactory(tui):
    win = MemViewWindow(tui)
    memViewCmd.set_win(win)
    return win

gdb.register_window_type("memview", MemViewFactory)




