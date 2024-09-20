"""
Analysis of the LogNormal distribution in the BBRC
==================================================
"""

# %%
# The goal of this document is to clarify the parametrization of the LogNormal distribution in the BBRC.
#
# From the RPREPO
# ---------------
#
# https://rprepo.readthedocs.io/en/latest/distributions.html#sec-lognormal
#
# * Type : univariate, continuous
# * Support : :math:`x\in(0,\infty)`
# * Parameter : :math:`\theta_1=\mu \in (-\infty,\infty)`, shape
# * Parameter : :math:`\theta_2=\sigma \in (0,\infty)`, scale
# * Mean : :math:`e^{\mu+\frac{\sigma^2}{2}}`
# * Variance : :math:`\left(e^{\sigma^2} - 1\right) e^{2\mu + \sigma^2}`
#
# .. math::
#     f(x) = \frac{1}{x} \frac{1}{\sigma \sqrt{2\pi}} \exp\left(-\frac{\left(\ln(x) - \mu\right)^2}{2 \sigma^2}\right)
#
# From this description we see that:
#
# * :math:`\theta_1` is the mean of the underlying gaussian and :math:`\theta_2`
#   is the standard deviation of the underlying gaussian
# * Mean is the Mean of the LogNormal random variable and Std
#   is the standard deviation of the LogNormal random variable.
#
# From OpenTURNS
# --------------
#
# * http://openturns.github.io/openturns/master/user_manual/_generated/openturns.LogNormal.html
# * http://openturns.github.io/openturns/master/user_manual/_generated/openturns.LogNormalMuSigma.html
#
# One of the two following parametrizations must be chosen:
#
# * `LogNormal` with :math:`\mu_\ell=\theta_1, \sigma_\ell=\theta_2` where :math:`\theta_1` is the mean
#    of the underlying gaussian and :math:`\theta_2` is the standard deviation of the underlying gaussian
# * `LogNormalMuSigma` with Mean, Std where Mean is the Mean of the LogNormal random variable
#    and Std is the standard deviation of the LogNormal random variable.
#
# Problem
# -------
#
# The problem is to select the parametrization that best corresponds to the problem and the data.
# The goal of this document is to make this selection clearer.

# %%
import openturns as ot
ot.__version__

# %%
# RP60
# ----
#
# https://rprepo.readthedocs.io/en/latest/reliability_problems.html#rp60

# %%
# RP60 with LogNormalMuSigma
# --------------------------

# %%
Mean = 2200.0
Std = 220.0
parameters = ot.LogNormalMuSigma(Mean, Std)

# %%
X = ot.ParametrizedDistribution(parameters)

# %%
X.getMean()

# %%
X.getStandardDeviation()

# %%
# RP60 with LogNormal
# -------------------

# %%
theta1 = 7.691
theta2 = 0.09975
X = ot.LogNormal(7.691, 0.09975, 0.0)
X

# %%
X.getMean()

# %%
X.getStandardDeviation()

# %%
# RP8
# ---
#
# https://rprepo.readthedocs.io/en/latest/reliability_problems.html#rp8

# %%
# RP8 with LogNormalMuSigma
# -------------------------

# %%
Mean = 120.0
Std = 12.0
parameters = ot.LogNormalMuSigma(Mean, Std)
parameters


# %%
X = ot.ParametrizedDistribution(parameters)
X

# %%
X.getMean()

# %%
X.getStandardDeviation()

# %%
# RP8 with LogNormal
# ------------------

# %%
theta1 = 4.783
theta2 = 0.09975
X = ot.LogNormal(4.783, 0.09975, 0.0)
X

# %%
X.getMean()

# %%
X.getStandardDeviation()

# %%
# Conclusion
# ----------
#
# We see that in the RP60 and RP8 problems, the Mean and Std parameters are exact
# while :math:`\theta_1` and :math:`\theta_2` are given with 4 significant digits.
# This leads to an approximation if the :math:`\theta_1` and :math:`\theta_2` parameters are used.
#
# This is why we choose the Mean and Std parameters as the parametrization for the BBRC.
# This corresponds to the following code and comments:

# %%
Mean = 120.0
Std = 12.0
parameters = ot.LogNormalMuSigma(Mean, Std)
X = ot.ParametrizedDistribution(parameters)

# %%
# * Mean is the Mean of the LogNormal random variable
# * Std is the standard deviation of the LogNormal random variable.
