import cython


cdef extern from "<aba_for_c.h>":
    pass


@cython.infer_types(True)  # type: ignore
cdef extern void umat(
    double *stress, double *statev, double *ddsdde, double *sse, double *spd,
    double *scd, double *rpl, double *ddsddt, double *drplde, double *drpldt,
    double *stran, double *dstran, double *time, double *dtime, double *temp,
    double *dtemp, double *predef, double *dpred, char *cmname, int *ndi,
    int *nshr, int *ntens, int *nstatv, double *props, int *nprops, double *coords,
    double *drot, double *pnewdt, double *celent, double *dfgrd0, double *dfgrd1,
    int *noel, int *npt, int *layer, int *kspt, int *jstep, int *kinc,
):
    E, nu = props[0], props[1]
    lam = E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))
    G = E / (2.0 * (1.0 + nu))

    ddsdde[:] = [
        lam + 2.0 * G, lam, lam, 0.0, 0.0, 0.0,
        lam, lam + 2.0 * G, lam, 0.0, 0.0, 0.0,
        lam, lam, lam + 2.0 * G, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, G, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, G, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, G,
    ]  # fmt: skip
    for i in range(6):
        for j in range(6):
            stress[i] += ddsdde[6 * i + j] * dstran[j]
