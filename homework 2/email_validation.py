def fun(s):
    # your code here
    # return True if s is a valid email, else return False
    if not('@' in s) or not('.' in s):
        return False
    temp = s.split('@')
    temp2 = temp[1].split('.')
    first = temp[0]
    second = temp2[0]
    third = temp2[1]
    for letter in first:
        if not(letter >= 'a' and letter <= 'z' or letter >= '0' and letter <= '9' or letter == '_' or letter == '-'):
            return False
    for letter in second:
        if not(letter >= 'a' and letter <= 'z' or letter >= '0' and letter <= '9'):
            return False
    if len(third) > 3:
        return False
    for letter in third:
        if not(letter >= 'a' and letter <= 'z'):
            return False
    return True

def filter_mail(emails):
    return list(filter(fun, emails))

if __name__ == '__main__':
    n = int(input())
    emails = []
    for _ in range(n):
        emails.append(input())

    filtered_emails = filter_mail(emails)
    filtered_emails.sort()
    print(filtered_emails)
