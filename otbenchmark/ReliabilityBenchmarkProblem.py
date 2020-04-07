#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define a benchmark problem."""

import openturns as ot


class ReliabilityBenchmarkProblem:
    """Class to define a benchmark problem."""

    def __init__(self, name, thresholdEvent, probability, description=""):
        """
        Create a reliability problem.

        Parameters
        ----------
        name : str
            The name of the benchmark problem.
            This is a short string, typically less than a dozen of caracters.

        thresholdEvent : ot.ThresholdEvent
            The event.

        probability : float
            The exact probability.

        description : str
            The description of the benchmark problem.
            This is a long string, typically longer than a sentence.
            It typically contains the bibliographical references.

        Example
        -------
        problem  = ReliabilityBenchmarkProblem(name, thresholdEvent,
                                               probability)
        """
        self.name = name
        self.thresholdEvent = thresholdEvent
        self.probability = probability
        self.description = description

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

    def getDescription(self):
        """
        Return the description of the problem.

        Parameters
        ----------
        None.

        Returns
        -------
        description: str
            The description of the problem.
        """
        return self.description

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
        s = ("name = %s\n"
             "event = %s\n"
             "probability = %s\n"
             "description = %s") % (
            self.name, self.thresholdEvent, self.probability, self.description)
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
        s = ("name = %s \n"
             "description = %s\n"
             "function = %s\n"
             "operator = %s\n"
             "threshold = %s\n"
             "probability = %s\n"
             "beta = %s\n"
             "distribution = %s") % (
            self.name, self.description,
            g, operator, threshold, self.probability, beta,
            distribution)
        return s
