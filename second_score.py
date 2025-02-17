n = int(input())
maxi = -1
maxi2 = 'Error! Second score not found.'
inp = input().split()
for i in inp:
    if int(i) > maxi:
        maxi2 = maxi
        maxi = int(i)
    elif int(i) > maxi2 and int(i) != maxi:
        maxi2 = int(i)
if maxi2 == -1:
    print('Error! Second score not found.')
else:
    print(maxi2)
