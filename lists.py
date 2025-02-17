n = int(input())
arr = []

for i in range(0, n):
    inp = input().split()
    match inp[0]:
        case 'insert':
            arr.insert(int(inp[1]), int(inp[2]))
        case 'print':
            print(arr)
        case 'remove':
            arr.remove(int(inp[1]))
        case 'append':
            arr.append(int(inp[1]))
        case 'sort':
            arr.sort()
        case 'pop':
            arr.pop()
        case 'reverse':
            arr.reverse()
