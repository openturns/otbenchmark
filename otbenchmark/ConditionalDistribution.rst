Marginal and conditional distributions
======================================

Conditional distribution
------------------------

For a given pair of continuous random variables :math:`X` and :math:`Y`
with probability densities :math:`f_X` and :math:`f_Y`, the conditional
density of :math:`Y|X` is:

.. math::


   f_{Y|X}(y|X = x) = \frac{f_{X,Y}(x,y)}{f_X(x)},

where :math:`f_X(x)` is the marginal distribution of :math:`X`:

.. math::


   f_X(x) = \int_{\mathbb{R}^{|Y|}} f_{X,Y}(x,y) dy.

In the previous equation, the integer :math:`|Y|` is the dimension of
the vector :math:`Y`.

For a multivariate random variable :math:`X=(X_1, X_2, ..., X_d)` and we
consider conditional distribution which arise when we condition with
respect with several marginals of :math:`X`. More precisely, we assume
that a given set of conditioning indices

.. math::


   C=(i_1, i_2, ..., i_c)

are given, where :math:`0\leq c\leq d` is an integeger,
:math:`i_1, i_2, ..., i_c \in \{1, 2, ..., d\}` and are so that
:math:`i_1 < i_2 < ... <i_c`. In other words, the integers
:math:`i_1, ..., i_c` are unique indices of :math:`X`. We also assume
that we are given the corresponding set of conditioning values

.. math::


   x_C = (x_{i_1}, x_{i_2}, ..., x_{i_c}) \in\mathbb{R}^c.

We denote by :math:`\overline{C}` the complementary set of :math:`C`:

.. math::


   \overline{C} = \{i \in \{1, ..., d\} | i \not\in C\}.

Therefore, the sets :math:`C` and :math:`\overline{C}` partition the
indices of :math:`X`, so that:

.. math::


   X = \left(X_C, X_\overline{C}\right).

The conditional distribution of :math:`X` given the conditioning indices
:math:`C` and the conditioning values :math:`x_C` is the distribution of
the random variable :math:`X` given the conditioning marginals have been
set to :math:`x_C`. Its probability density function is:

.. math::


   f_{X|X_C=x_C}(x_\overline{C})= \frac{f_X(x_C, x_\overline{C})}{f_{X_C}(x_C)}

where :math:`f_{X_C}(x_C)` is the marginal probability density function
of :math:`X_C`:

.. math::


   f_{X_C}(x_C) = \int_{\mathbb{R}^{d - c}} f_\left(X_C, X_\overline{C}\right)\left(x_C, x_\overline{C}\right) dx_\overline{C}.

Example of conditional distributions in three dimensions
--------------------------------------------------------

For example, consider the random variable :math:`X = (X_1, X_2, X_3)`
with probability density function :math:`f_X`. The conditional
distribution of :math:`(X_1, X_2, X_3 | X_2 = x_2, X_3 = x_3)` is:

.. math::


   f_{(X_1, X_2, X_3 | X_2 = x_2, X_3 = x_3)}(x_1) 
   = \frac{f_X(x)}{f_{(X_2, X_3)}(x_2, x_3)}

where :math:`f_{(X_2, X_3)}` is the marginal distribution of
:math:`(X_2,X_3)`:

.. math::


   f_{(X_2, X_3)}(x_2, x_3) = \int_{\mathbb{R}} f_X(x_1, x_2, x_3) dx_1.

The conditional distribution of :math:`(X_1, X_2, X_3 | X_3 = x_3)` is:

.. math::


   f_{(X_1, X_2, X_3 | X_3 = x_3)}(x_1, x_2) 
   = \frac{f_X(x)}{f_{X_3}(x_3)}

where :math:`f_{X_3}` is the marginal density of :math:`X_3`:

.. math::


   f_{X_3}(x_3) = \int_{\mathbb{R}^2} f_X(x_1, x_2, x_3) dx_1 dx_2.

