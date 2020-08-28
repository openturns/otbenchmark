#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define a benchmark problem."""

import openturns as ot


class ReliabilityBenchmarkProblem:
    """Class to define a benchmark problem."""

    def __init__(self, name, thresholdEvent, probability):
        """
        Create a reliability problem.

        The essential information is the exact probability.
        This should be as accurate as possible.
        The best possible accuracy for a Python float is 53 significant
        (binary) bits, which approximately corresponds to 15-17 decimal digits.
        If this accuracy is not available, then a reference value may be used,
        for example from a large Monte-Carlo sample.

        In general, the exact probability should be a constant value,
        e.g. 0.123456789.
        However, we may be forced to compute this probability at the creation
        of the problem, for example if the threshold of the problem
        can be set at the creation of the object.
        In this case, the unit test must check that the default value of the
        parameters correspond to a reference, constant, value.

        Parameters
        ----------
        name : str
            The name of the benchmark problem.
            This is a short string, typically less than a dozen of caracters.

        thresholdEvent : ot.ThresholdEvent
            The event.

        probability : float
            The exact probability.

        Example
        -------
        problem  = ReliabilityBenchmarkProblem(name, thresholdEvent,
                                               probability)
        """
        self.name = name
        self.thresholdEvent = thresholdEvent
        self.probability = probability

        return None

    def getEvent(self):
        """
        Return the event.

        Parameters
        ----------
        None.

        Returns
        -------
        event: ot.ThresholdEvent
            The event.
        """
        return self.thresholdEvent

    def getProbability(self):
        """
        Return the probability.

        Parameters
        ----------
        None.

        Returns
        -------
        probability: float
            The probability of the event.
        """
        return self.probability

    def getName(self):
        """
        Return the name of the problem.

        Parameters
        ----------
        None.

        Returns
        -------
        name: str
            The name of the problem.
        """
        return self.name

    def computeBeta(self):
        """
        Return the beta of the reliability problem.

        This is the quantile of the
        probability of a standard gaussian distribution.

        Parameters
        ----------
        None.

        Returns
        -------
        beta: float
            The beta of the problem.
        """
        beta = ot.Normal().computeQuantile(self.probability, True)[0]
        return beta

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
        s = ("name = %s\n" "event = %s\n" "probability = %s\n") % (
            self.name,
            self.thresholdEvent,
            self.probability,
        )
        return s

    def toFullString(self):
        """
        Convert the object into a string, with full details.

        Parameters
        ----------
        None.

        Returns
        -------
        s: str
            The string of the problem.
        """
        g = self.thresholdEvent.getFunction()
        operator = self.thresholdEvent.getOperator()
        threshold = self.thresholdEvent.getThreshold()
        beta = ot.Normal().computeQuantile(self.probability, True)[0]
        inputVector = self.thresholdEvent.getAntecedent()
        distribution = inputVector.getDistribution()
        s = (
            "name = %s \n"
            "function = %s\n"
            "operator = %s\n"
            "threshold = %s\n"
            "probability = %s\n"
            "beta = %s\n"
            "distribution = %s"
        ) % (self.name, g, operator, threshold, self.probability, beta, distribution,)
        return s
