#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define a sensitivity benchmark problem."""


class SensitivityBenchmarkProblem:
    def __init__(
        self,
        name,
        distribution,
        function,
        firstOrderIndices,
        totalOrderIndices,
    ):
        """
        Creates a reliability problem.

        Parameters
        ----------
        name : str
            The name of the benchmark problem.
            This is a short string, typically less than a dozen of caracters.

        distribution : ot.Distribution
            The input distribution.

        function : ot.Function
            The model.

        firstOrderIndices : ot.Point
            The first order indices.

        totalOrderIndices : ot.Point
            The total order indices.

        Examples
        --------
        >>> import otbenchmark as otb
        >>> problem = otb.SensitivityBenchmarkProblem(name, distribution, function,
        ...     firstOrderIndices, totalOrderIndices)  # doctest: +SKIP
        """
        dimension = distribution.getDimension()
        if function.getInputDimension() != dimension:
            raise ValueError(
                "The input dimension of the function is %d"
                "but the dimension of the distribution is %d"
                % (dimension, function.getInputDimension())
            )
        if function.getOutputDimension() != 1:
            raise ValueError(
                "The output dimension of the function is %d"
                % (function.getOutputDimension())
            )
        self.name = name
        self.distribution = distribution
        self.function = function
        if firstOrderIndices.getDimension() != dimension:
            raise ValueError(
                "The the dimension of the distribution is %d"
                "but the dimension of the first order indices is %d"
                % (dimension, firstOrderIndices.getDimension())
            )
        if totalOrderIndices.getDimension() != dimension:
            raise ValueError(
                "The the dimension of the distribution is %d"
                "but the dimension of the total order indices is %d"
                % (dimension, firstOrderIndices.getDimension())
            )
        for i in range(dimension):
            if firstOrderIndices[i] < 0.0 or firstOrderIndices[i] > 1.0:
                raise ValueError(
                    "The first order indice of marginal %d"
                    "%f, which is not in [0, 1]" % (i, firstOrderIndices[i])
                )
            if totalOrderIndices[i] < 0.0 or totalOrderIndices[i] > 1.0:
                raise ValueError(
                    "The total order indice of marginal %d"
                    "is %f, which is not in [0, 1]" % (i, firstOrderIndices[i])
                )
            if totalOrderIndices[i] < firstOrderIndices[i]:
                raise ValueError(
                    "The total order indice of marginal %d"
                    "is %f, which is greater than the first "
                    "order indce %f" % (i, totalOrderIndices[i], firstOrderIndices[i])
                )

        self.firstOrderIndices = firstOrderIndices
        self.totalOrderIndices = totalOrderIndices
        return None

    def getInputDistribution(self):
        """
        Returns the input distribution.

        Parameters
        ----------
        None.

        Returns
        -------
        distribution: ot.Distribution
            The distribution.
        """
        return self.distribution

    def getFunction(self):
        """
        Returns the function.

        Parameters
        ----------
        None.

        Returns
        -------
        function: ot.Function
            The function.
        """
        return self.function

    def getName(self):
        """
        Returns the name of the problem.

        Parameters
        ----------
        None.

        Returns
        -------
        name: str
            The name.
        """
        return self.name

    def getFirstOrderIndices(self):
        """
        Returns the first order Sobol' sensitivity indices.

        Parameters
        ----------
        None.

        Returns
        -------
        firstOrderIndices: ot.Point
            The first order sensitivity indices.
        """
        return self.firstOrderIndices

    def getTotalOrderIndices(self):
        """
        Returns the total order Sobol' sensitivity indices.

        Parameters
        ----------
        None.

        Returns
        -------
        totalOrderIndices: ot.Point
            The total order sensitivity indices.
        """
        return self.totalOrderIndices

    def __str__(self):
        """
        Convert the object into a string.

        This method is typically called with the "print" statement.

        Parameters
        ----------
        None.

        Returns
        -------
        s: str
            The string corresponding to the object.
        """
        s = (
            "name = %s\n"
            "distribution = %s\n"
            "function = %s\n"
            "firstOrderIndices = %s\n"
            "totalOrderIndices = %s"
        ) % (
            self.name,
            self.distribution,
            self.function,
            self.firstOrderIndices,
            self.totalOrderIndices,
        )
        return s
