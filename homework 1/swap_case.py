line = input()
for i in range (0, len(line)):
    if line[i] >= 'A' and line[i] <= 'Z':
        print(line[i].lower(), end='')
    elif line[i] >= 'a' and line[i] <= 'z':
        print(line[i].upper(), end='')
    else:
        print(line[i], end='')
