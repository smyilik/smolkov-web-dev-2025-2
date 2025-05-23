n = int(input())
a = []
b = []
for i in range(0, n):
    a1, b1 = input().split()
    a.append(int(a1))
    b.append(int(b1))
t = int(input())
a.sort()
b.sort()
passengers = 0
for i in range (0, n):
    if a[i] <= t:
        passengers += 1
    if b[i] <= t:
        passengers -= 1
    if a[i] > t and b[i] > t:
        break
print(passengers)
