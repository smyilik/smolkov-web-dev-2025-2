file = open("example.txt", encoding="utf8")
text = file.readlines()
file.close()
maxlen = 0
ans = ''
for line in text:
    for word in line.split():
        word = word.strip('!~`@#$%^&*()-_=+-\\|/,.?<>\'\"№;:')
        if len(word) > maxlen:
            maxlen = len(word)
            ans = word
        elif len(word) == maxlen:
            ans += "\n" + word
print(ans)
