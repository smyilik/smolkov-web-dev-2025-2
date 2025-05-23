def matrix_mult(n, *lines):
    A = []
    B = []
    n = int(n)
    for i in range (0, len(lines)):
        line = lines[i].split()
        for element in line:
            if i < n:
                A.append(int(element))
            else:
                B.append(int(element))
    mat = []
    line = ''
    summ = 0
    for i in range (0, n):
        for j in range(0, n):
            for k in range(0, n):
                summ += A[i * n + k] * B[k * n + j]
            line += str(summ) + ' '
            summ = 0
        mat.append(line.strip())
        line = ''
    return mat
