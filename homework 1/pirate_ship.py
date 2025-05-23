n, m = input().split()
n = int(n)
m = int(m)
lines = []
for i in range (0, m):
    line = input()
    temp = line.split(',')
    lines.append([round(float(temp[2])/float(temp[1]), 2), line])
lines.sort(reverse=True)
for line in lines:
    print(line[1].replace(',', ' '))
