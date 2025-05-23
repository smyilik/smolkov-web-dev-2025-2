s = input()
vowels = "AEIOU"
kevin = 0
stuart = 0
length = len(s)
for i in range(0, length):
    if s[i] in vowels:
        kevin += length - i
    else:
        stuart += length - i
if kevin >= stuart:
    print("Кевин", kevin)
else:
    print("Стюарт", stuart)
