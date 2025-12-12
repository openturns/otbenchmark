"""
The non-monotonic function of Morris f: R^20 -> R.
"""

from ._SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot
import warnings


class MorrisFunction(ot.OpenTURNSPythonFunction):
    """
    The non-monotonic function of Morris f: [0,1]^20 -> R

    References
    ---------
    M. D. Morris, 1991, Factorial sampling plans for preliminary
    computational experiments,Technometrics, 33, 161--174.

    This code was taken from otmorris/python/src/Morris.i.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(123)
    >>> b0 = ot.DistFunc.rNormal()
    >>> b1 = ot.DistFunc.rNormal(10)
    >>> b2 =  ot.DistFunc.rNormal(175)
    >>> f = ot.Function(MorrisFunction(b0, b1, b2))
    >>> inputSample = ot.JointDistribution([ot.Uniform(0,1)] * 20).getSample(20)
    >>> outputSample = f(inputSample)
    """

    def __init__(
        self,
        b0Random=0.0,
        b1Random=None,
        b2Random=None,
    ):
        """
        Create the Morris function

        Parameters
        ----------
        b0Random : float, optional
            The constant part. The default is 0.0.
        b1Random : ot.Point(10), optional
            The linear part. The default is ot.Point(10).
        b2Random : ot.Point(175), optional
            The quadratic part. The default is ot.Point(175).

        Returns
        -------
        None.

        """
        if b1Random is None:
            b1Random = ot.Point(10)
        if b2Random is None:
            b2Random = ot.Point(175)

        ot.OpenTURNSPythonFunction.__init__(self, 20, 1)

        if not isinstance(b0Random, float):
            raise ValueError(f"b0Random must be float, got {type(b0Random)}")

        if len(b1Random) != 10:
            raise ValueError(f"b1Random must have length 10, got {len(b1Random)}")

        if len(b2Random) != 175:
            raise ValueError(f"b2Random must have length 175, got {len(b2Random)}")

        self.b0Random = b0Random
        self.b1Random = b1Random
        self.b2Random = b2Random

        inputVariables = ot.Description.BuildDefault(20, "x")

        b1 = [20.0] * 10 + list(b1Random)

        DOUBLE_FORMAT = ".17g"
        b0Expr = f"{float(b0Random):{DOUBLE_FORMAT}}"
        b1Expr = ",".join(f"{float(v):{DOUBLE_FORMAT}}" for v in b1)
        b2Expr = ",".join(f"{float(v):{DOUBLE_FORMAT}}" for v in b2Random)

        expr = f"""
    var x[20] := {{
    x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,
    x10,x11,x12,x13,x14,x15,x16,x17,x18,x19
    }};

    var b0Expr := {b0Expr};

    var b1[20] := {{
        {b1Expr}
    }};

    var b2Random[175] := {{
        {b2Expr}
    }};

    var y := b0Expr;

    /* --- build w --- */
    var w[20];

    for (var i := 0; i < 20; i += 1)
    {{
        w[i] := 2 * (x[i] - 0.5);
    }};

    /* nonlinear indices: Python indices 2, 4, 6 */
    w[2] := 2 * (1.1 * x[2] / (x[2] + 0.1) - 0.5);
    w[4] := 2 * (1.1 * x[4] / (x[4] + 0.1) - 0.5);
    w[6] := 2 * (1.1 * x[6] / (x[6] + 0.1) - 0.5);

    /* --- linear term --- */
    for (var i := 0; i < 20; i += 1)
    {{
        y += b1[i] * w[i];
    }};

    /* --- quadratic term --- */
    var randomIndex := 0;

    for (var i := 0; i < 20; i += 1)
    {{
        for (var j := i + 1; j < 20; j += 1)
        {{
            if ((i < 6) and (j < 6))
            {{
                y += -15.0 * w[i] * w[j];
            }}
            else
            {{
                y += b2Random[randomIndex] * w[i] * w[j];
                randomIndex += 1;
            }};
        }};
    }};

    /* --- cubic term: i < j < k, first 5 variables only --- */
    for (var i := 0; i < 5; i += 1)
    {{
        for (var j := i + 1; j < 5; j += 1)
        {{
            for (var k := j + 1; k < 5; k += 1)
            {{
                y += -10.0 * w[i] * w[j] * w[k];
            }};
        }};
    }};

    /* --- quartic term: i < j < k < ell, first 4 variables only --- */
    for (var i := 0; i < 4; i += 1)
    {{
        for (var j := i + 1; j < 4; j += 1)
        {{
            for (var k := j + 1; k < 4; k += 1)
            {{
                for (var ell := k + 1; ell < 4; ell += 1)
                {{
                    y += 5.0 * w[i] * w[j] * w[k] * w[ell];
                }};
            }};
        }};
    }};

    y
    """

        self.g = ot.SymbolicFunction(inputVariables, [expr])

    def _exec(self, x):
        y = self.g(x)
        return y


class MorrisSensitivity(SensitivityBenchmarkProblem):
    """Class to define the Morris sensitivity benchmark problem."""

    def __init__(self, randomParameters=False):
        r"""
        Define the Morris sensitivity benchmark problem.

        The function :math:`g` is defined on :math:`[0,1]^{20}` and takes
        values in :math:`\mathbb{R}`.

        Its inputs are independent random variables with distribution
        :math:`\mathcal{U}(0,1)`.

        It is defined as:

        .. math::

           g(\boldsymbol{x}) & = \beta_0
                  + \sum_{i} \beta_i\, w_i(x) \\
                & \quad + \sum_{i<j} \beta_{i,j}\, w_i(x)\, w_j(x) \\
                & \quad + \sum_{i<j<k} \beta_{i,j,k}\, w_i(x)\, w_j(x)\, w_k(x) \\
                & \quad + \sum_{i<j<k<\ell} \beta_{i,j,k,\ell}\, w_i(x)\, w_j(x)\, w_k(x)\, w_\ell(x)

        for any :math:`\boldsymbol{x} \in [0,1]^{20}` where:

        .. math::

           w_i(x) = 2\,(x_i - 0.5)

        for :math:`i \in \{1, 2, 4, 6, 8, \dots, 20\}`, and:

        .. math::

           w_i(x) = 2\,\left(\frac{1.1\, x_i}{x_i + 1} - 0.5\right)

        for :math:`i \in \{3, 5, 7\}`.
        The parameters :math:`(\beta_i)_{1 \leq i \leq 20}`,
        :math:`(\beta_{i,j})_{1 \leq i, j \leq 20}`,
        :math:`(\beta_{i,j, k})_{1 \leq i, j, k\leq 20}`,
        :math:`(\beta_{i,j, k, \ell})_{1 \leq i, j, k, \ell \leq 20}`
        are presented below, in the **Notes** section.
        In (Morris, 1991)'s paper, these parameters are random.
        In order to get consistent results, the default value of the
        randomParameters parameter is so that the parameters beta
        are constant, deterministic, values.

        Parameters
        ----------
        randomParameters: bool
            Set to True to get random parameters.
            Caution: the reference Sobol' indices are not valid if the
            parameters are random.

        Returns
        -------
        None.

        Notes
        -----

        The dimension of this problem is equal to 20 and cannot be changed.

        The function is the sum of five functions.

        * The first function is constant and equal to :math:`\beta_0`.
        * The second is a linear combination of :math:`\boldsymbol{w}` coefficients.
        * The third is an order 2 combination of :math:`\boldsymbol{w}` coefficients.
        * The fourth is an order 3 combination of :math:`\boldsymbol{w}` coefficients.
        * The fifth is an order 4 combination of :math:`\boldsymbol{w}` coefficients.

        Therefore, Morris's function is a modification of an order 4 polynomial,
        where the small non-linearity comes from the :math:`\boldsymbol{w}`
        coefficients.

        The reference Sobol' indices were computed from
        polynomial chaos expansion.
        A Sobol' low discrepancy design of experiments was generated
        with 65536 training points.
        The full polynomial chaos expansion used an hyperbolic enumeration
        rule (using quasi-norm parameter 0.7) and a polynomial degree 6.
        The coefficients were estimated from least squares.
        With 65536 points in the validation set, the Q² was 99.47%.
        There are 3 significant digits in the reference results.

        **Morris Function Parameters**

        Let :math:`\mathcal{N}(0,1)` be a random Gaussian variable with zero
        mean and unit standard deviation.

        The first order coefficients of the Morris function are:

        .. math::

            \beta_i =
            \begin{cases}
            20 & \text{if } i = 1,\ldots,10, \\
            \mathcal{N}(0,1) & \text{otherwise}.
            \end{cases}

        The second order coefficients are:

        .. math::

            \beta_{i,j} =
            \begin{cases}
            -15 & \text{if } i,j \in \{1,\ldots,6\}, \\
            \mathcal{N}(0,1) & \text{otherwise}.
            \end{cases}

        The third order coefficients are:

        .. math::

            \beta_{i,j,\ell} =
            \begin{cases}
            -10 & \text{if } i,j,\ell \in \{1,\ldots,5\},\\
            0 & \text{otherwise}.
            \end{cases}

        The fourth order coefficients are:

        .. math::

            \beta_{i,j,\ell,s} =
            \begin{cases}
            5 & \text{if } i,j,\ell,s \in \{1,\ldots,4\},\\
            0 & \text{otherwise}.
            \end{cases}

        References
        ----------
        * M. D. Morris, 1991, Factorial sampling plans for preliminary
          computational experiments, Technometrics, 33, 161--174.
        """
        dimension = 20
        if randomParameters:
            b0 = ot.DistFunc.rNormal()
            b1 = ot.DistFunc.rNormal(10)
            b2 = ot.DistFunc.rNormal(175)
            warnings.warn(
                "The parameters were changed, but the reference Sobol' "
                "indices are not updated.",
                stacklevel=2,
            )
        else:
            b0, b1, b2 = self._getParameters()

        function = ot.Function(MorrisFunction(b0, b1, b2))

        distributionList = [ot.Uniform(0.0, 1.0) for i in range(dimension)]
        distribution = ot.JointDistribution(distributionList)

        name = "Morris"

        firstOrderIndices = _FIRST_ORDER_INDICES_REFERENCE
        totalOrderIndices = _TOTAL_ORDER_INDICES_REFERENCE
        super(MorrisSensitivity, self).__init__(
            name, distribution, function, firstOrderIndices, totalOrderIndices
        )

        return None

    def _getParameters(self):
        return _B0_REFERENCE, _B1_REFERENCE, _B2_REFERENCE

# =====================================================================
# Reference Data Definitions
# =====================================================================


_FIRST_ORDER_INDICES_REFERENCE = ot.Point(
    [
        0.0061257, 0.0068268, 0.0148127, 0.0097981, 0.0125528, 0.0000141,
        0.0559007, 0.1419089, 0.1174405, 0.1236114, 0.0000047, 0.0000306,
        0.0014462, 0.0044277, 0.0001056, 0.0002988, 0.0018635, 0.0000012,
        0.0000932, 0.0006815,
    ]
)

_TOTAL_ORDER_INDICES_REFERENCE = ot.Point(
    [
        0.2454044, 0.2451133, 0.1058652, 0.2494050, 0.1038293, 0.0912750,
        0.0575356, 0.1444652, 0.1198208, 0.1264613, 0.0016405, 0.0014999,
        0.0028601, 0.0068092, 0.0018924, 0.0029526, 0.0032192, 0.0018433,
        0.0015019, 0.0019601,
    ]
)

_B0_REFERENCE = 0.60820165121876457

_B1_REFERENCE = ot.Point(
    [
        -1.26617310, -0.43826562, 1.20547820, -2.18138523, 0.35004209,
        -0.35500705, 1.43724931, 0.81066798, 0.79315601, -0.47052560,
    ]
)

_B2_REFERENCE = ot.Point(
    [
        0.26, -2.29, -1.28, -1.31, -0.09, 1.00, -0.14, -0.56, 0.45, 0.32,
        0.45, -1.04, -0.86, 0.47, -0.13, 0.35, 1.78, 0.07, -0.78, -0.72,
        -0.24, -1.79, 0.40, 1.37, 1.00, 0.74, -0.04, 0.54, 0.30, 0.41,
        -0.49, -0.38, -0.75, 0.26, 1.97, -0.67, 1.86, 0.05, 0.79, 0.72,
        -0.74, 0.18, -1.53, 0.66, 0.54, 1.74, -0.96, 0.38, -0.18, 1.67,
        -1.04, -0.35, 1.21, -0.78, -1.37, 0.10, -0.89, 0.91, 0.33, -0.48,
        0.68, 1.71, 1.07, -0.51, -1.66, 2.25, 0.76, -0.51, -0.63, -0.96,
        0.54, 0.81, -0.73, -0.11, 0.99, -0.16, -0.94, -1.97, -0.66, 0.34,
        1.02, 0.64, -0.09, -0.86, 1.3, -0.2, 1.3, 2.1, -0.9, -1.5, -1.3,
        0.2, -3.1, 0.0, -1.3, 1.0, -0.8, 0.2, 1.0, 0.3, -0.5, -0.5, 0.3,
        -0.2, 3.0, 0.9, 0.6, 0.6, -1.5, -2.4, 0.7, -0.7, -0.8, 0.4, -0.5,
        1.9, 0.2, 1.7, -0.5, -0.7, -0.5, -2.3, -0.6, -0.3, -1.8, -0.7,
        0.1, 0.9, -1.5, -0.3, 1.3, -0.4, -1.9, -0.5, 0.6, 0.0, 0.7, -0.2,
        0.5, -0.0, -0.0, 0.1, -0.4, -0.1, 0.1, -0.2, 0.5, 0.2, 0.4, 0.1,
        -0.1, 1.5, 1.2, 0.5, -0.7, -0.1, -1.5, 1.2, 0.9, -0.3, 0.6, -0.6,
        -1.4, -0.5, -1.6, 0.5, 0.2, -0.1, 0.6, -0.6, -1.2, -0.9, -0.1, 0.4,
        0.5,
    ]
)
