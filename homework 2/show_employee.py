def show_employee(*inp):
    salary = 100000
    name = inp[0]
    if len(inp) == 2 and isinstance(inp[1], int):
        salary = inp[1]
    else:
        name = ''
        for i in inp:
            name += i
    return (f"{name}: {salary} ₽")
