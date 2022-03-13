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
            return

watchCmd = WatchCmd()

def WatchWinFactory(tui):
    win = WatchWindow(tui)
    watchCmd.set_window(win)
    # register render() to be called each time the gdb prompt will be displayed
    gdb.events.before_prompt.connect(win.render)
    return win

class WatchWindow(object):

    save_list = []

    def __init__(self, tui):
        self.tui = tui
        self.watch_list = WatchWindow.save_list
        self.prev = {}

    def set_watch_list(self, list):
        self.watch_list = list

    def close(self):
        # stop rendor() being called when the window has been closed
        gdb.events.before_prompt.disconnect(self.render)
        # save the watch list so it will be restored when the window is activated
        WatchWindow.save_list = self.watch_list

    def render(self):
        if not self.tui.is_valid():
            return

        self.tui.erase()

        try:
            frame = gdb.selected_frame()
        except gdb.error:
            self.tui.write("No frame currently selected" + NL)
            return

        self.tui.title = frame.name()

        for name in self.watch_list:
            try:
                val = frame.read_var(name)
                hint = BLUE if name in self.prev and self.prev[name] != val else WHITE
                self.prev[name] = val
                self.tui.write(f'{GREEN}{name:<10}{hint}{val}{RESET}{NL}')
            except ValueError:
                self.tui.write(f'{GREY}{name:<10}{NL}') 

gdb.register_window_type("watch", WatchWinFactory)
