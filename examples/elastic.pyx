import cython


cdef extern from "<aba_for_c.h>":
    pass


cdef public void umat(
    stress: cython.p_double, statev: cython.p_double, ddsdde: cython.p_double, sse: cython.p_double,
    spd: cython.p_double, scd: cython.p_double, rpl: cython.p_double, ddsddt: cython.p_double, drplde: cython.p_double,
    drpldt: cython.p_double, stran: cython.p_double, dstran: cython.p_double, time: cython.p_double,
    dtime: cython.p_double, temp: cython.p_double, dtemp: cython.p_double, predef: cython.p_double,
    dpred: cython.p_double, cmname: cython.p_char, ndi: cython.p_int, nshr: cython.p_int, ntens: cython.p_int,
    nstatv: cython.p_int, props: cython.p_double, nprops: cython.p_int, coords: cython.p_double, drot: cython.p_double,
    pnewdt: cython.p_double, celent: cython.p_double, dfgrd0: cython.p_double, dfgrd1: cython.p_double,
    noel: cython.p_int, npt: cython.p_int, layer: cython.p_int, kspt: cython.p_int, jstep: cython.p_int,
    kinc: cython.p_int,
):
    cdef double E, nu, lam, G
    E, nu = props[0], props[1]
    lam = E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))
    G = E / (2.0 * (1.0 + nu))

    cdef int i, j
    for i in range(3):
        for j in range(3):
            ddsdde[6 * i + j] = lam
        ddsdde[6 * i + i] += 2.0 * G
        ddsdde[6 * (i + 3) + (i + 3)] = G
    for i in range(6):
        for j in range(6):
            stress[i] += ddsdde[6 * i + j] * dstran[j]
