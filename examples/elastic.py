import cython


@cython.infer_types(True)
def umat(
    stress, statev, ddsdde, sse, spd, scd, rpl, ddsddt, drplde, drpldt, stran, dstran,
    time, dtime, temp, dtemp, predef, dpred, cmname, ndi, nshr, ntens, nstatv, props,
    nprops, coords, drot, pnewdt, celent, dfgrd0, dfgrd1, noel, npt, layer, kspt,
    jstep, kinc,
):  # fmt: skip
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
