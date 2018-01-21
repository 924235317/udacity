from decimal import *


def shape(M):
    row = len(M)
    if row == 0:
        return 0, 0
    col = len(M[0])
    if col == 0:
        return row, 0
    return row, col


def matxRound(M, decPts=4):

    num_row, num_col = shape(M)
    for row in range(0, num_row):
        for col in range(0, num_col):
            n = M[row][col]
            M[row][col] = round(n, decPts)
# def matxRound(M, decPts=4):
#     # with localcontext() as ctx:
#     #     ctx.prec = decPts  # Perform a high precision calculation
#         num_row, num_col = shape(M)
#         for row in range(0, num_row):
#             for col in range(0, num_col):
#                 n = M[row][col]
#                 #M[row][col] = Decimal(str(n)).quantize(Decimal(str(10 ** -decPts)), rounding=ROUND_DOWN)
#                 M[row][col] = Decimal(n)
#                 #print Decimal(1.212344)._round_(1)
#
#                 print n


def transpose(M):
    num_row, num_col = shape(M)

    mt = [[0 for col in range(num_row)] for row in range(num_col)]
    for row in range(0, num_row):
        for col in range(0, num_col):
            mt[col][row] = M[row][col]

    return mt

def augmentMatrix(A, b):
    res = [line + n for line, n in zip(A, b)]
    return res



def swapRows(M, r1, r2):
    M[r1], M[r2] = M[r2], M[r1]



def scaleRow(M, r, scale):
    if scale == 0:
        raise ValueError

    M[r] = [x * scale for x in M[r]]

def addScaledRow(M, r1, r2, scale):
    new_r2 = [x*scale for x in M[r2]]
    new_r1 = [x1+x2 for x1, x2 in zip(M[r1], new_r2)]
    M[r1] = new_r1


def gj_Solve1(A, b, decPts=4, epsilon=1.0e-16):
    num_equations, num_variables = shape(A)
    row_b, _ = shape(b)
    if num_variables != row_b:
        return None

    M = augmentMatrix(A, b)

    for col in range(num_variables):
        MT = transpose(M)

        #find the max value in column
        column = MT[col]
        print column
        max_in_col = column[col]
        for n in range(col, num_equations):
            max_in_col = max_in_col if abs(max_in_col) > abs(column[n]) else column[n]

        if abs(max_in_col) < epsilon:
            return None

        print max_in_col

        idx = column[col:].index(max_in_col) + col
        #print idx
        #swap the first row with the max_value_row and scale the value to 1
        swapRows(M, idx, col)
        scaleRow(M, col, 1.0/M[col][col])

        #clear coefficients below
        for row in range(num_equations):
            if row != col and abs(M[row][col]) > epsilon:


                coefficient = -M[row][col]
                addScaledRow(M, row, col, coefficient)

    matxRound(M)
    res = transpose(M)[-1]
    return res


def gj_Solve(A, b, decPts=4, epsilon=1.0e-16):
    if len(A) != len(b):
        raise ValueError

    Ab = augmentMatrix(A, b)

    for c in range(len(A[0])):
        AbT = transpose(Ab)
        col = AbT[c]
        maxValue = max(col[c:], key=abs)
        if abs(maxValue) < epsilon:
            return None

        maxIndex = col[c:].index(maxValue) + c
        print maxValue
        swapRows(Ab, c, maxIndex)
        scaleRow(Ab, c, 1.0 / Ab[c][c])

        for i in range(len(A)):
            if Ab[i][c] != 0 and i != c:
                addScaledRow(Ab, i, c, -Ab[i][c])

    matxRound(Ab)

    return [[value] for value in transpose(Ab)[-1]]



if __name__ == '__main__':
    m = [[1.12132123, 123],
         [123123.121245151, 312]]

    matxRound(m, decPts=4)
    with localcontext() as ctx:
        ctx.prec = 2  # Perform a high precision calculation
        n = 1.231231
        # print Decimal(n)/Decimal(3)
        # print Decimal(1.2222222) * Decimal(1)

    A = [[7, 5, 3],
         [-5, -4, 6],
         [2, -2, -9]]
    b = [[1],
         [1],
         [1]]
    print gj_Solve1(A,b)

    print zip(*A)