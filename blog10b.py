GREEN = "\x1b[38;5;47m"
BLUE  = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;255m"
RESET = "\x1b[0m"

class Register(object):

    frame = None

    def __init__(self, name):
        self.name = name
        self.fmt = 'd'
        self.val = None
        self.colour = None

    def update_value(self):
        val = Register.frame.read_register(self.name)
        self.colour = BLUE if self.val != val else WHITE
        self.val = val

    def __format__(self, format_spec):
        return self.colour + format(str(self), format_spec)

    # use GDB format_string{} to convert to Python string
    def __str__(self):
        return self.val.format_string(format=self.fmt)

r1 = Register('a0')
print(r1.name)

Register.frame = gdb.selected_frame()
r1.update_value()
# need to implement _format_
print(f"{GREEN}{r1.name:<5}{r1:<24}{RESET}X")
r1.update_value()
print(f"{GREEN}{r1.name:<5}{r1:<24}{RESET}X")

r1.fmt = 'x'
print(f"{GREEN}{r1.name:<5}{r1:<24}{RESET}X")

r2 = Register('pc')
r2.update_value()
r2.fmt = 'a'
print(f"{GREEN}{r2.name:<5}{r2:<24}{RESET}X")
