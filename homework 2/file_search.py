import os
import sys


def find_file(filename):
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files:
            return os.path.join(root, filename)
    return None

if __name__ == "__main__":
    filename = sys.argv[1]
    found_path = find_file(filename)
    if found_path:
        file = open(found_path, 'r', encoding='utf-8')
        i = 0
        for line in file:
            print(line, end="")
            i += 1
            if i > 4:
                break
    else:
        print(f"Файл {filename} не найден")
