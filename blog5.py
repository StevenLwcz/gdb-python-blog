frame = gdb.selected_frame()
val = frame.read_register("v0")
print("d.f", val['d']['f'])
print("s.u", val['s']['u'])
print("h.s", val['h']['s'])
print("b.u", val['b']['u'])
print("d.s[0] ", val['d']['s'][0])
print("d.s[1] ", val['d']['s'][1])

# print("d.u", val['d']['u'].format_string(format='x'))