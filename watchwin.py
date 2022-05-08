GREEN = "\x1b[38;5;47m"
BLUE  = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;15m"
YELLOW = "\x1b[38;5;226m"
GREY  = "\x1b[38;5;246m"
RESET = "\x1b[0m"
NL = "\n\n"

fmt_list = ['o', 'x', 'd', 'u', 't', 'f', 'a', 'i', 'c', 's', 'z']

class WatchCmd(gdb.Command):
    """Add variables to the TUI Window watch.
watchwin variable-list
    Variables will be greyed out when they go out of scope.
    Changes to values while stepping are highlighted in blue.
watchwin /FMT  variable-list
    Set the format specifier as per print /FMT for the variable list
watchwin /C variable-list
    Clear the format specifier for the variable list
watchwin del variable-list
    Delete variables from the watch window.
watchwin clear
    Clears all variables from the watch window.
watchwin type [on|off]
    Toggle display of the variable type and indicator: static(=), global(^) or argument(*)."""

    def __init__(self):
       super(WatchCmd, self).__init__("watchwin", gdb.COMMAND_DATA)
       self.window = None

    def set_window(self, window):
        self.window = window

    def invoke(self, arguments, from_tty):
        argv = gdb.string_to_argv(arguments)
        argc = len(argv)
        if self.window:
            if argc == 0:
                print("watchwin variable-list")
            elif argv[0] == "del" and argc > 1:
                self.window.delete_from_watch_list(argv[1:]) 
            elif argv[0] == "clear":
                self.window.clear_watch_list()
            elif argv[0][0:1] == "/":
                if argv[0][1:2] in fmt_list:
                    if argc > 1:
                        self.window.set_format(argv[1:], argv[0][1:2])
                    else:
                        print("watchwin /FMT variable-list")
                else:
                    if argv[0][1:2] == 'C':
                        if argc > 1:
                            self.window.clear_format(argv[1:])
                        else:
                            print("watchwin /C variable-list")
                    else:
                        print("watchwin /FMT variable-list")
            elif argv[0] == "type" and argc == 2:
                if argv[1] == "on":
                    self.window.toggle_type_mode(True)
                elif argv[1] == "off":
                    self.window.toggle_type_mode(False)
                else:
                    print("watchwin type [on|off]")
            else:
                self.window.add_watch(argv) 
        else:
            print("watchwin: Tui Window not active yet")

watchCmd = WatchCmd()

def WatchWinFactory(tui):
    win = WatchWindow(tui)
    watchCmd.set_window(win)
    # register create_watch() to be called each time the gdb prompt is displayed.
    gdb.events.before_prompt.connect(win.create_watch)
    return win

class WatchWindow(object):

    save_watch = {}

    def __init__(self, tui):
        self.tui = tui
        self.watch = WatchWindow.save_watch
        self.title = ""
        self.start = 0
        self.list = []
        self.type_mode = False

    def add_watch(self, list, fmt=None):
        for name in list:
            symbol = gdb.lookup_global_symbol(name)
            if symbol and symbol.is_variable:
                tag = "^"
            else:
                symbol = gdb.lookup_static_symbol(name)
                if symbol and symbol.is_variable:
                    tag = "="
                else:
                    symbol = gdb.lookup_symbol(name)[0]
                    if symbol:
                        if symbol.is_argument:
                            tag = "*"
                        elif symbol.is_variable:
                            tag = " "
                        else: 
                            print(f'watchwin: {name} is not a variable or argument.')
                            return
                    else:
                        print(f'watchwin: {name} not found in current frame.')
                        return

            self.watch[name] = {'tag': tag, 'type': str(symbol.type), 'fmt': fmt, 'val': None}

    def set_format(self, list, fmt):
        for name in list:
            if name in self.watch:
                self.watch[name]['fmt'] = fmt
            else:
                self.add_watch([name], fmt)

    def clear_format(self, list):
        for name in list:
            if name in self.watch:
                self.watch[name]['fmt'] = None
            else:
                print(f'watchwin /C: {name} not found')

    def toggle_type_mode(self, mode):
        self.type_mode = mode

    def clear_watch_list(self):
        self.watch.clear()

    def delete_from_watch_list(self, list):
        for l in list:
            try:
                del self.watch[l]
            except:
                print(f"watchwin del: {l} not found")

    def vscroll(self, num):
        if num > 0 and num + self.start < len(self.list) or \
           num < 0 and num + self.start >= 0:
            self.start += num
            self.render()

    def close(self):
        gdb.events.before_prompt.disconnect(self.create_watch)
        # save the watch dictionary so it will be restored when the window is activated
        WatchWindow.save_watch = self.watch

    def create_watch(self):
        self.list = []

        try:
            frame = gdb.selected_frame()
        except gdb.error:
            self.title = "No Frame"
            self.list.append("No frame currently selected" + NL)
            self.render()
            return

        self.title = frame.name()

        for name, attr in self.watch.items():
            try:
                value = frame.read_var(name)
                hint = BLUE if attr['val'] != value else WHITE
                self.watch[name]['val'] = value

                if attr['fmt']:
                    value = value.format_string(format=attr['fmt'])
                
                if self.type_mode:
                    self.list.append(f'{attr["tag"]}{YELLOW}{attr["type"]:<16}{GREEN}{name:<10}{hint}{value}{RESET}{NL}')
                else:
                    self.list.append(f'{GREEN}{name:<10}{hint}{value}{RESET}{NL}')
            except ValueError:
                value = attr['val'].format_string(format=attr['fmt']) if attr['fmt'] else attr['val']

                if self.type_mode:
                    self.list.append(f'{GREY}{attr["tag"]}{attr["type"]:<16}{name:<10}{value}{RESET}{NL}')
                else:
                    self.list.append(f'{GREY}{name:<10}{value}{RESET}{NL}')

        self.render()

    def render(self):
        if not self.tui.is_valid():
            return

        self.tui.title = self.title
        self.tui.erase()

        for l in self.list[self.start:]:
            self.tui.write(l)

gdb.register_window_type("watch", WatchWinFactory)
