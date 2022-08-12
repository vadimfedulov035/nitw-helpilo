with open("eng.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    lines = [line.split(":") for line in lines]
    lines_1 = [(name, "".join(line)) for (name, *line) in lines]


with open("rus.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    lines = [line.split(":") for line in lines]
    lines_2 = [(name, "".join(line)) for (name, *line) in lines]


for idx, (line_1, line_2) in enumerate(zip(lines_1, lines_2)):
    name_1, str_1 = line_1
    name_2, str_2 = line_2
    if name_1 != name_2:
        print(idx, name_1, name_2)
        print(idx, str_1, str_2)
        exit()
