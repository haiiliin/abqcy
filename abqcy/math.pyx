cdef extern double norm(double *x, int n):
    cdef int i
    cdef double summation = 0.0
    for i in range(n):
        summation += x[i] * x[i]
    return summation ** 0.5
