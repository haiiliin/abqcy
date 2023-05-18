

cdef extern from "<aba_for_c.h>":
    pass


cdef public void umat(
    double *stress, double *statev, double *ddsdde, double *sse, double *spd, double *scd, double *rpl, double *ddsddt,
    double *drplde, double *drpldt, double *stran, double *dstran, double *time, double *dtime, double *temp,
    double *dtemp, double *predef, double *dpred, char *cmname, int *ndi, int *nshr, int *ntens, int *nstatv,
    double *props, int *nprops, double *coords, double *drot, double *pnewdt, double *celent, double *dfgrd0,
    double *dfgrd1, int *noel, int *npt, int *layer, int *kspt, int *jstep, int *kinc,
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
