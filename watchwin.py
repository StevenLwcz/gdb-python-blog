# Blog Part 3

GREEN = "\x1b[38;5;47m"
BLUE  = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;15m"
GREY  = "\x1b[38;5;246m"
RESET = "\x1b[0m"
NL = "\n\n"

class WatchCmd(gdb.Command):
    """Add variables to the TUI Window watch
watch variable-list
Variables will be greyed out when it goes out of scope.
Changes to the values while stepping are highlighted in blue."""

    def __init__(self):
       super(WatchCmd, self).__init__("watch", gdb.COMMAND_DATA)
       self.window = None

    def set_window(self, window):
        self.window = window

    def invoke(self, arguments, from_tty):
        argv = gdb.string_to_argv(arguments)
        if self.window:
            self.window.set_watch_list(argv) 
        else:
            print("watch: Tui Window not active yet")

watchCmd = WatchCmd()

def WatchWinFactory(tui):
    win = WatchWindow(tui)
    watchCmd.set_window(win)
    # register render() to be called each time the gdb prompt will be displayed
    gdb.events.before_prompt.connect(win.create_watch)
    return win

class WatchWindow(object):

    save_list = []

    def __init__(self, tui):
        self.tui = tui
        self.watch_list = WatchWindow.save_list
        self.prev = {}
        self.title = ""
        self.start = 0
        self.list = []

    def set_watch_list(self, list):
        self.watch_list = list

    def vscroll(self, num):
        if num > 0 and self.start < len(self.list) - 1 or num < 0 and self.start > 0:
            self.start += num
            self.render()

    def close(self):
        gdb.events.before_prompt.disconnect(self.create_watch)
        # save the watch list so it will be restored when the window is activated
        WatchWindow.save_list = self.watch_list

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

        for name in self.watch_list:
            try:
                val = frame.read_var(name)

                if name in self.prev and self.prev[name] != val:
                    hint = BLUE
                else:
                    hint = WHITE

                self.prev[name] = val
                self.list.append(f'{GREEN}{name:<10}{hint}{val}{RESET}{NL}')
            except ValueError:
                self.list.append(f'{GREY}{name:<10}{NL}') 

        self.render()

    def render(self):
        if not self.tui.is_valid():
            return

        self.tui.title = self.title
        self.tui.erase()

        for l in self.list[self.start:]:
            self.tui.write(l)

gdb.register_window_type("watch", WatchWinFactory)
