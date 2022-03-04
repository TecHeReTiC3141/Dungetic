import scripts.constants_and_sources as c_a_s
from scripts.constants_and_sources import *

print(c_a_s.curr_room)
print(curr_room)

def tp(room):
    global c_a_s
    c_a_s.curr_room = room

tp(1)

print(c_a_s.curr_room)
print(curr_room)