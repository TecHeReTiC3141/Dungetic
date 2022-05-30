from scripts.algorithms_of_generation import *

dung_length, dung_width = randint(3, 7), randint(3, 7)
print(dung_width, dung_length)
dung_map = create_dung_map(dung_width, dung_length)

for i in dung_map:
    print(*[str(j.type).ljust(3) for j in i])