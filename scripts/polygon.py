from scripts.algorithms_of_generation import *

dung_length, dung_width = randint(3, 7), randint(3, 7)
print(dung_width, dung_length)

dung_map = create_connected_dung(dung_width, dung_length)

for i in dung_map:
    print(*[str((j.type, j.comp)).ljust(5) for j in i])

for i in range(1, dung_width + 1):
    for j in range(1, dung_length + 1):
        print(i, j, dung_map[i][j].type, dung_map[i][j].neighbours)