#!/usr/bin/env python
# -*- coding: utf-8 -*-


def gfun_22(x):
    """Performance function for reliability problem 22.

    Parameters
    ----------
        x : numpy.array of float(s)
            Values of independent variables: columns are the different
            parameters/random variables (x1, x2,...xn) and rows are different
            parameter/random variables sets for different calls.

    Returns
    -------
        g_val_sys : numpy.array of float(s)
            Performance function value for the system.
        g_val_comp : numpy.array of float(s)
            Performance function value for each component.
        msg : str
            Accompanying diagnostic message, e.g. warning.
    """
    import numpy as np

    # expected number of random variables/columns
    nrv_e = 2

    g = float("nan")
    msg = "Ok"
    x = np.array(x, dtype="f")

    n_dim = len(x.shape)
    if n_dim == 1:
        x = np.array(x)[np.newaxis]
    elif n_dim > 2:
        msg = "Only available for 1D and 2D arrays."
        return float("nan"), float("nan"), msg

    nrv_p = x.shape[1]
    if nrv_p != nrv_e:
        msg = f"The number of random variables (x, columns) is expected "
        "to be {nrv_e} but {nrv_p} is provided!"
    else:
        g = 2.5 - 1 / np.sqrt(2) * (x[:, 0] + x[:, 1]) + 0.1 * (x[:, 0] - x[:, 1]) ** 2

    g_val_comp = g
    return g_val_comp


def gfun_8(x):
    """Performance function for reliability problem 8.

    Parameters
    ----------
        x : numpy.array of float(s)
            Values of independent variables: columns are the different
            parameters/random variables (x1, x2,...xn) and rows are different
            parameter/random variables sets for different calls.

    Returns
    -------
        g_val_sys : numpy.array of float(s)
            Performance function value for the system.
        g_val_comp : numpy.array of float(s)
            Performance function value for each component.
        msg : str
            Accompanying diagnostic message, e.g. warning.
    """
    import numpy as np

    # expected number of random variables/columns
    nrv_e = 6

    g = float("nan")
    msg = "Ok"
    x = np.array(x, dtype="f")

    n_dim = len(x.shape)
    if n_dim == 1:
        x = np.array(x)[np.newaxis]
    elif n_dim > 2:
        msg = "Only available for 1D and 2D arrays."
        return float("nan"), float("nan"), msg

    nrv_p = x.shape[1]
    if nrv_p != nrv_e:
        msg = f"The number of random variables (x, columns) is expected "
        "to be {nrv_e} but {nrv_p} is provided!"
    else:
        g = x[:, 0] + 2 * x[:, 1] + 2 * x[:, 2] + x[:, 3] - 5 * x[:, 4] - 5 * x[:, 5]

    g_val_comp = g
    return g_val_comp
