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

    ddsdde[:] = [0.0] * 36
    for i in range(3):
        for j in range(3):
            ddsdde[6 * i + j] = lam
        ddsdde[6 * i + i] += 2.0 * G
        ddsdde[6 * (i + 3) + (i + 3)] = G
    for i in range(6):
        for j in range(6):
            stress[i] += ddsdde[6 * i + j] * dstran[j]
