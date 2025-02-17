n = int(input())
ls = []
maxi = -1
maxi2 = 'Error! Second score not found.'
for i in range(0, n):
    name = input()
    mark = float(input())
    if mark > maxi:
        maxi2 = maxi
        maxi = mark
    elif mark > maxi2 and mark != maxi:
        maxi2 = mark
    ls.append([name, mark])
ls.sort()
if maxi2 == -1:
    print('Error! Second score not found.')
else:
    for i in ls:
        if i[1] == maxi2:
            print(i[0])
