nm = input().split()
arr = [int(i) for i in input().split()]
a = [int(j) for j in input().split()]
b = [int(k) for k in input().split()]
mood = 0
for number in arr:
    if number in a:
        mood += 1
    elif number in b:
        mood -= 1
print(mood)
