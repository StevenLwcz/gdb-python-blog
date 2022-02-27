# Blog Part 2

NL = "\n\n"

GREEN = "\x1b[38;5;47m"
RESET = "\x1b[0m"

class AddTextCmd(gdb.Command):
    """Add text to the Tui window hello
addtext [string]
string = text to be displayed"""

    def __init__(self):
       super(AddTextCmd, self).__init__("addtext", gdb.COMMAND_USER)

    def set_win(self, win):
        self.win = win

    def invoke(self, arguments, from_tty):
        self.win.set_text(arguments)
        self.win.render()

# create an instance of our command class to register with gdb and keep a reference for later
addTextCmd = AddTextCmd()

# Factory Method
def HelloWinFactory(tui):
    win =  HelloWindow(tui)
    # register the Window class with the addtext command
    addTextCmd.set_win(win)
    return win

class HelloWindow(object):

    def __init__(self, tui):
        self.tui = tui
        self.tui.title = "Hello Window"
        self.text = "hello World"

    def set_text(self, text):
        self.text = text

    def render(self):
        if not self.tui.is_valid():
            return

        # self.tui.erase()
        self.tui.write(f'{GREEN}{self.text}{RESET}{NL}')

    def close(self):
        pass

    def hscroll(self, num):
        pass

    def vscroll(self, num):
        pass

    def click(self, x, y, button):
        pass
 
gdb.register_window_type("hello", HelloWinFactory)
