def process_list(arr):
    result = []
    for i in arr:
        if i % 2 == 0:
            result.append(i**2)
        else:
            result.append(i**3)
    return result

def process_list_gen(arr):
    return [i**2 if i % 2 == 0 else i**3 for i in arr]
  
# process_list_gen работает на 0.005 секунды дольше process_list (0.015с и 0.01с соответственно)
# process_list быстрее process_list_gen примерно в 1.5 раза
