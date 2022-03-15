# Blog Part 3

GREEN = "\x1b[38;5;47m"
BLUE  = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;15m"
YELLOW = "\x1b[38;5;226m"
GREY  = "\x1b[38;5;246m"
RESET = "\x1b[0m"
NL = "\n\n"

class WatchCmd(gdb.Command):
    """Add variables to the TUI Window watch.
watch variable-list
    Variables will be greyed out when it goes out of scope.
    Changes to the values while stepping are highlighted in blue.
watch hex [on|of] variable
    Toggle display of a variable in hex. Add if not already in the watch window.
watch del variable-list
    Delete the variables from the watch window.
watch clear
    Clears all variables from the watch window.
watch type [on|off]
    Toggle display of the variable type."""


    def __init__(self):
       super(WatchCmd, self).__init__("watch", gdb.COMMAND_DATA)
       self.window = None

    def set_window(self, window):
        self.window = window

    def invoke(self, arguments, from_tty):
        argv = gdb.string_to_argv(arguments)
        argc = len(argv)
        if self.window:
            if argc == 0:
                print("watch variable-list")
            elif argv[0] == "del" and argc > 1:
                self.window.delete_from_watch_list(argv[1:]) 
            elif argv[0] == "clear":
                self.window.clear_watch_list()
            elif argv[0] == "hex" and argc == 3:
                if argv[1] == "on": 
                    self.window.toggle_hex_mode(argv[2], True)
                elif argv[1] == "off":
                    self.window.toggle_hex_mode(argv[2], False)
                else:
                    print("watch hex [on|off] variable")
            elif argv[0] == "type" and argc == 2:
                if argv[1] == "on":
                    self.window.toggle_type_mode(True)
                elif argv[1] == "off":
                    self.window.toggle_type_mode(False)
                else:
                    print("watch type [on|off]")
            else:
                self.window.add_watch_dict(argv) 
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

    save_dict = {}

    def __init__(self, tui):
        self.tui = tui
        self.watch_dict = WatchWindow.save_dict
        self.prev = {}
        self.title = ""
        self.start = 0
        self.list = []
        self.type_mode = False

    def add_watch_dict(self, list):
        self.watch_dict.update(dict.fromkeys(list, False))

    def toggle_hex_mode(self, name, mode):
        self.watch_dict[name] = mode

    def toggle_type_mode(self, mode):
        self.type_mode = mode

    def clear_watch_list(self):
        self.watch_dict.clear()
        self.prev.clear()

    def delete_from_watch_list(self, list):
        for l in list:
            try:
                del self.watch_dict[l]
                del self.prev[l]
            except:
                print(f"watch del: {l} not found")

    def vscroll(self, num):
        if num > 0 and num + self.start < len(self.list) or \
           num < 0 and num + self.start > 0:
            self.start += num
            self.render()

    def close(self):
        gdb.events.before_prompt.disconnect(self.create_watch)
        # save the watch list so it will be restored when the window is activated
        WatchWindow.save_dict = self.watch_dict

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

        for name, hex in self.watch_dict.items():
            try:
                value = frame.read_var(name)
                hint = BLUE if name in self.prev and self.prev[name] != value else WHITE
                self.prev[name] = value
                st = value.format_string(format="x") if hex else value
                if self.type_mode:
                    self.list.append(f'{YELLOW}{str(value.type):<16}{GREEN}{name:<10}{hint}{st}{RESET}{NL}')
                else:
                    self.list.append(f'{GREEN}{name:<10}{hint}{st}{RESET}{NL}')
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
