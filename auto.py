# Blog Part 4

GREEN = "\x1b[38;5;47m"
BLUE  = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;15m"
YELLOW = "\x1b[38;5;226m"
RESET = "\x1b[0m"
NL = "\n\n"

fmt_list = ['o', 'x', 'd', 'u', 't', 'f', 'a', 'i', 'c', 's', 'z']

class AutoCmd(gdb.Command):
   """auto /FMT variable-list
/FMT as per GDB command x.
Change the format for any variable displayed in the auto window."""

   def __init__(self):
       super().__init__("auto", gdb.COMMAND_DATA)
       self.window = None

   def set_window(self, window):
       self.window = window

   def invoke(self, arguments, from_tty):
        argv = gdb.string_to_argv(arguments)
        argc = len(argv)
        if self.window:
            if argc < 2:
                print("auto /FMT variable-list")
            elif argv[0][0:1] == '/' and argv[0][1:2] in fmt_list:
                self.window.set_format(argc, argv) 
            else:
                print(f"auto /FMT variable-list. /{fmt_list}")
        else:
            print("auto: Tui window not active yet")
 
autoCmd = AutoCmd()

def AutoWinFactory(tui):
    win = AutoWindow(tui)
    autoCmd.set_window(win)
    # register create_auto() to be called each time the gdb prompt will be displayed
    gdb.events.before_prompt.connect(win.create_auto)
    return win

def split_with_ansi_escape(idx, start, st):
    """return the string st at offset idx not counting ANSI escape sequences
from offset start, which needs to include ANSI escape sequences.
The first characer in the string will be the last ANSI escape sequence enountered"""

    seq = ""
    esc = False
    count = 0
    for i, c in enumerate(st[start:]):
        if esc:
            seq += c
            count += 1
            if c == 'm':
               esc = False
        else:
            if i - count >= idx:
                break

            if c == '\x1b':
                esc = True
                seq = '\x1b'
                count += 1
            elif c == '\n':
                break

    return(st[0:start] + seq + st[i + start:])

AutoVariableOffset = 27   # 11 (Yellow) + 16 (Type)
AutoValueOffset = 24      # 10 (Green) + 10 (Name) - 2 (Idx)

def scroll_auto_line(idx, start, st):
    if idx == 1:                                           # skip type
        i = AutoVariableOffset
        return(st[0:start] + st[start + i:])
    else:
        return split_with_ansi_escape(idx + AutoValueOffset, start, st) 

class AutoWindow(object):

    LineOffset = 7 # Keep Line numbers when horizontal scrolling.

    def __init__(self, tui):
        self.tui = tui
        self.prev = {}
        self.start = 0
        self.horiz = 0
        self.list = []
        self.title = ""
        self.block = None
        self.format = {}

    def set_format(self, argc, argv):
        fmt = argv[0][1:2]
        del argv[0]
        for name in argv:
            symbol = gdb.lookup_symbol(name)[0]
            if symbol and (symbol.is_variable or symbol.is_argument):
                self.format[name] = fmt
            else:
                print(f'auto: {name} is not a variable or argument.')
                return

        self.render()

    def close(self):
        # stop create_auto() being called when the window has been closed
        gdb.events.before_prompt.disconnect(self.create_auto)

    def vscroll(self, num):
        if num > 0 and num + self.start < len(self.list) or \
           num < 0 and num + self.start >= 0:
            self.start += num
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
                self.tui.write(l)
        else:
            for l in self.list[self.start:]:
                self.tui.write(scroll_auto_line(self.horiz, AutoWindow.LineOffset, l))
                # self.tui.write(split_with_ansi_escape(self.horiz, AutoWindow.LineOffset, l))

    def create_auto(self):
        self.list = []

        try:
            frame = gdb.selected_frame()
        except gdb.error:
            self.start = 0
            self.block = None
            self.title = "No Frame"
            self.list.append("No frame currently selected" + NL)
            self.render()
            return

        self.title = frame.name()

        block = frame.block()
        if not block == self.block:
            self.start = 0
            self.block = block

        while block:
            for symbol in block:
                if not symbol.is_variable and not symbol.is_argument:
                    continue

                name = symbol.name
                line = symbol.line
                type = str(symbol.type)
                arg = "*" if symbol.is_argument else " "
                val = frame.read_var(symbol, block)

                hint = BLUE if name in self.prev and self.prev[name] != val else WHITE
                self.prev[name] = val

                if name in self.format:
                    val = val.format_string(format=self.format[name])

                self.list.append(f'{arg}{line:<6}{YELLOW}{type:<16}{GREEN}{name:<10}{hint}{val}{RESET}{NL}')

            block = block.superblock
            if block.is_static:
                break

        self.render()

gdb.register_window_type("auto", AutoWinFactory)
