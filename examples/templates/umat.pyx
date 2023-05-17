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
    r"""Abaqus UMAT interface for the material model.

    Parameters
    ----------
    stress : double[:], shape (ntens,), defined in all situations
        This array is passed in as the stress tensor at the beginning of the increment and must be updated in this
        routine to be the stress tensor at the end of the increment. If you specified initial stresses Initial
        Conditions, this array will contain the initial stresses at the start of the analysis. The size of this
        array depends on the value of ``NTENS`` as defined below. In finite-strain problems the stress tensor has
        already been rotated to account for rigid body motion in the increment before ``UMAT`` is called, so that
        only the corotational part of the stress integration should be done in ``UMAT``. The measure of stress used
        is ``true`` (Cauchy) stress.

        If the ``UMAT`` utilizes a hybrid formulation that is total (as opposed to the default incremental behavior),
        the stress array is extended beyond NTENS. The first NTENS entries of the array contain the stresses, as
        described above. The additional quantities are as follows::

            STRESS(NTENS+1)

        Read only :math:`\hat{J}`::

            STRESS(NTENS+2)

        Write only :math:`\widehat{K}=J \frac{\partial^2 U}{\partial \widehat{J}^2}`, and::

            STRESS(NTENS+3)

        Write only
        :math:`\frac{\partial \widehat{K}}{\partial \widehat{J}}=J \frac{\partial^3 U}{\partial \widehat{J}^3}`,
        where :math:`U` is the volumetric part of the strain energy density potential.
    statev : double[:], shape (nstatv,), defined in all situations
        An array containing the solution-dependent state variables. These are passed in as the values at the beginning
        of the increment unless they are updated in user subroutines ``USDFLD`` or ``UEXPAN``, in which case the
        updated values are passed in. In all cases ``STATEV`` must be returned as the values at the end of the
        increment. The size of the array is defined as described in Allocating Space for Solution-Dependent State
        Variables.

        In finite-strain problems any vector-valued or tensor-valued state variables must be rotated to account for
        rigid body motion of the material, in addition to any update in the values associated with constitutive
        behavior. The rotation increment matrix, ``DROT``, is provided for this purpose.
    ddsdde : double[:,:], shape (ntens, ntens), defined in all situations
        Jacobian matrix of the constitutive model,
        :math:`\mathbf{C}=(1 / J) \partial \Delta(J \boldsymbol{\sigma}) / \partial \Delta \boldsymbol{\varepsilon}`,
        where :math:`\Delta(J \boldsymbol{\sigma})` are the Kirchhoff stress increments, :math:`J` is the determinant
        of the deformation gradient representing the volume change from the reference configuration, :math:`\sigma` is
        the Cauchy  stress, and :math:`\Delta \varepsilon` are the strain increments. If the volume change is small,
        the Jacobian matrix can be approximated as
        :math:`\partial \Delta \boldsymbol{\sigma} / \partial \Delta \varepsilon`, where :math:`\Delta \sigma` are the
        Cauchy stress increments. ``DDSDDE(I,J)`` defines the change in the Ith stress component at the end of the time
        increment caused by an infinitesimal perturbation of the Jth component of the strain increment array. Unless
        you invoke the unsymmetric equation solution capability for the user-defined material, Abaqus/Standard will use
        only the symmetric part of ``DDSDDE``. The symmetric part of the matrix is calculated by taking one half the sum
        of the matrix and its transpose.

        For viscoelastic behavior in the frequency domain, the Jacobian matrix must be dimensioned as
        ``DDSDDE(NTENS,NTENS,2)``. The stiffness contribution (storage modulus) must be provided in
        ``DDSDDE(NTENS,NTENS,1)``, while the damping contribution (loss modulus) must be provided in
        ``DDSDDE(NTENS,NTENS,2)``.
    sse, spd, scd : double, defined in all situations
        Specific elastic strain energy, plastic dissipation, and ``creep`` dissipation, respectively. These are passed in
        as the values at the start of the increment and should be updated to the corresponding specific energy values
        at the end of the increment. They have no effect on the solution, except that they are used for energy output.
    rpl : double, defined only in a fully coupled thermal-stress or a coupled thermal-electrical-structural analysis
        Volumetric heat generation per unit time at the end of the increment caused by mechanical working of the
        material.
    ddsddt : double[:,:], shape (ntens, ntens), defined only in a fully coupled thermal-stress or a coupled thermal-electrical-structural analysis
        Variation of the stress increments with respect to the temperature.
    drplde : double[:], shape (ntens,), defined only in a fully coupled thermal-stress or a coupled thermal-electrical-structural analysis
        Variation of ``RPL`` with respect to the strain increments.
    drpldt : double, defined only in a fully coupled thermal-stress or a coupled thermal-electrical-structural analysis
        Variation of ``RPL`` with respect to the strain increments.
    stran : double[:], shape (ntens,), passed for information only
        An array containing the total strains at the beginning of the increment. If thermal expansion is included in
        the same material definition, the strains passed into UMAT are the mechanical strains only (that is, the
        thermal strains computed based upon the thermal expansion coefficient have been subtracted from the total
        strains). These strains are available for output as the ``elastic`` strains.

        In finite-strain problems the strain components have been rotated to account for rigid body motion in the
        increment before UMAT is called and are approximations to logarithmic strain.
    dstran : double[:], shape (ntens,), passed for information only
        Array of strain increments. If thermal expansion is included in the same material definition, these are the
        mechanical strain increments (the total strain increments minus the thermal strain increments).
    time : double, passed for information only
        - ``time(1)``: Value of step time at the beginning of the current increment or frequency.
        - ``time(2)``: Value of step time at the beginning of the current increment or frequency.
    dtime : double, passed for information only
        Value of step time at the beginning of the current increment or frequency.
    temp : double, passed for information only
        Temperature at the beginning of the increment.
    dtemp : double, passed for information only
        Increment of temperature.
    predef : double[:], shape (npr-ed,), passed for information only
        Array of interpolated values of predefined field variables at this point at the start of the increment, based
        on the values read in at the nodes.
    dpred : double[:], shape (npred,), passed for information only
        Array of increments of predefined field variables.
    cmname : str, passed for information only
        User-defined material name, left justified. Some internal material models are given names starting with the
        ``ABQ_`` character string. To avoid conflict, you should not use ``ABQ_`` as the leading string for ``CMNAME``.
    ndi : int, passed for information only
        Number of direct stress components at this point.
    nshr : int, passed for information only
        Number of engineering shear stress components at this point.
    ntens : int, passed for information only
        Size of the stress or strain component array (``NDI`` + ``NSHR``).
    nstatv : int, passed for information only
        Number of solution-dependent state variables that are associated with this material type (defined as described
        in Allocating Space for Solution-Dependent State Variables).
    props : double[:], shape (nprops,), passed for information only
        User-specified array of material constants associated with this user material.
    nprops : int, passed for information only
        User-specified array of material constants associated with this user material.
    coords : double[:], shape (3,), passed for information only
        An array containing the coordinates of this point. These are the current coordinates if geometric nonlinearity
        is accounted for during the step (see Defining an Analysis); otherwise, the array contains the original
        coordinates of the point.
    drot : double[:,:], shape (3, 3), passed for information only
        Rotation increment matrix. This matrix represents the increment of rigid body rotation of the basis system in
        which the components of stress (``STRESS``) and strain (``STRAN``) are stored. It is provided so that vector-
        or tensor-valued state variables can be rotated appropriately in this subroutine: stress and strain components
        are already rotated by this amount before ``UMAT`` is called. This matrix is passed in as a unit matrix for
        small-displacement analysis and for large-displacement analysis if the basis system for the material point
        rotates with the material (as in a shell element or when a local orientation is used).
    pnewdt : double, can be updated in any situations
        Ratio of suggested new time increment to the time increment being used (``DTIME``, see discussion later in this
        section). This variable allows you to provide input to the automatic time incrementation algorithms in
        Abaqus/Standard (if automatic time incrementation is chosen). For a quasi-static procedure the automatic time
        stepping that Abaqus/Standard uses, which is based on techniques for integrating standard creep laws (see
        Quasi-Static Analysis), cannot be controlled from within the UMAT subroutine.

        ``PNEWDT`` is set to a large value before each call to ``UMAT``.

        - If ``PNEWDT`` is redefined to be less than 1.0, Abaqus/Standard must abandon the time increment and attempt
          it again with a smaller time increment. The suggested new time increment provided to the automatic time
          integration algorithms is ``PNEWDT`` x ``DTIME``, where the ``PNEWDT`` used is the minimum value for all
          calls to user subroutines that allow redefinition of PNEWDT for this iteration.
        - If ``PNEWDT`` is given a value that is greater than 1.0 for all calls to user subroutines for this iteration
          and the increment converges in this iteration, Abaqus/Standard may increase the time increment. The suggested
          new time increment provided to the automatic time integration algorithms is ``PNEWDT`` x ``DTIME``, where the
          ``PNEWDT`` used is the minimum value for all calls to user subroutines for this iteration.
        - If automatic time incrementation is not selected in the analysis procedure, values of ``PNEWDT`` that are
          greater than 1.0 will be ignored and values of ``PNEWDT`` that are less than 1.0 will cause the job to
          terminate.
    celent : double, passed for information only
        Characteristic element length, which is a typical length of a line across an element for a first-order element;
        it is half of the same typical length for a second-order element. For beams and trusses it is a characteristic
        length along the element axis. For membranes and shells it is a characteristic length in the reference surface.
        For axisymmetric elements it is a characteristic length in the :math:`(r,z)` plane only. For cohesive elements
        it is equal to the constitutive thickness.
    dfgrd0 : double[:,:], shape (3, 3), passed for information only
        Array containing the deformation gradient at the beginning of the increment. If a local orientation is defined
        at the material point, the deformation gradient components are expressed in the local coordinate system defined
        by the orientation at the beginning of the increment. For a discussion regarding the availability of the
        deformation gradient for various element types, see Deformation Gradient.
    dfgrd1 : double[:,:], shape (3, 3), passed for information only
        Array containing the deformation gradient at the end of the increment. If a local orientation is defined at the
        material point, the deformation gradient components are expressed in the local coordinate system defined by the
        orientation. This array is set to the identity matrix if nonlinear geometric effects are not included in the
        step definition associated with this increment. For a discussion regarding the availability of the deformation
        gradient for various element types, see Deformation Gradient.
    noel : int, passed for information only
        Element number.
    npt : int, passed for information only
        Integration point number.
    layer : int, passed for information only
        Layer number (for composite shells and layered solids).
    kspt : int, passed for information only
        Section point number within the current layer.
    jstep : int, passed for information only
        - ``jstep(1)``: Step number.
        - ``jstep(2)``: Procedure type key (see Results File).
        - ``jstep(3)``: 1 if NLGEOM=YES for the current step; 0 otherwise.
        - ``jstep(4)``: 1 if NLGEOM=YES for the current step; 0 otherwise.
    kinc : int, passed for information only
        Increment number.
    """
