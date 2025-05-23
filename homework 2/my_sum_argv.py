import sys
from my_sum import my_sum

if __name__ == "__main__":
    args = sys.argv[1:]
    result = my_sum(*args)
    print(result)
