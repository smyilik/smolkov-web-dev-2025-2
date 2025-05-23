import time

start = time.time()

def fact_it(n):
    answer = 1
    while n > 1:
        answer *= n
        n -= 1
    end = time.time()
    print(end - start)
    return answer

def fact_rec(n):
    if n > 1:
        return n * fact_rec(n - 1)
    end = time.time()
    print(end - start)
    return 1

# fact_rec работает на 0.0019 секунды дольше fact_it (0.0049с и 0.0030с соответственно)
# fact_it быстрее fact_rec примерно в 1.63 раза
