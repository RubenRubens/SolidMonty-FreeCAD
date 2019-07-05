# Identifiers' counter

p_counter = 0
def part_counter():
    global p_counter
    p_counter += 1
    return p_counter

b_counter = 0
def boolean_counter():
    global b_counter
    b_counter += 1
    return b_counter

s_counter = 0
def sketch_counter():
    global s_counter
    s_counter += 1
    return s_counter

c_counter = 0
def copy_counter():
    global c_counter
    c_counter += 1
    return c_counter