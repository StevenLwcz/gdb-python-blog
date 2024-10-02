infe = gdb.selected_inferior()
print(gdb.inferiors())
print(infe.pid)
print(infe.num)

expr = gdb.parse_and_eval('$x0')
addr = expr.address if expr.address != None else expr

print(hex(int(addr)))

try:
    mv = infe.read_memory(addr, 32)
    print(mv.hex(' '))

    import re
    pattern = re.compile(r'[\x00-\x1f\x7f-\x9f]')

    text = mv.tobytes().decode('latin-1')
    text =  pattern.sub('.', text)

    print(text)

    for i in range(0, 32, 8):
        m = mv[i:i + 8]
        text = pattern.sub('.', m.tobytes().decode('latin-1'))
        print(f"{hex(addr + i)}: {m.hex(' ')} {text}")

except gdb.MemoryError:
    print(f'Cant read memory at {addr}')
