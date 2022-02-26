# Blog Part 1

NL = "\n\n"

GREEN = "\x1b[38;5;47m"
RESET = "\x1b[0m"

# Factory Method
def HelloWinFactory(tui):
    return HelloWindow(tui)

class HelloWindow(object):

    def __init__(self, tui):
        self.tui = tui
        self.tui.title = "Hello Window"

    def render(self):
        if self.tui.is_valid():
            self.tui.write(f'{GREEN}Hello World{RESET}{NL}')

    def close(self):
        pass

    def hscroll(self, num):
        pass

    def vscroll(self, num):
        pass

    def click(self, x, y, button):
        pass
 
gdb.register_window_type("hello", HelloWinFactory)
