#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to create an OpenTURNS distribution out of a Black Box Reliability Challenge
 problem"""

import openturns as ot
import numpy as np


class BBRCDistribution:
    """Class to create an OpenTURNS distribution out of a Black Box Reliability
    Challenge problem"""

    def __init__(self, set_id, problem_id):
        """
        Creates an ot.ComposedDistribution from the BBRC 2019 distribution table.
        References
        ----------
        https://rprepo.readthedocs.io/en/latest/
        Parameters
        ----------
        set_id: int
            First item defining the reliability problem selected.
        problem_id: int
            Second item defining the reliability problem selected.
        """
        self.set_id = set_id
        self.problem_id = problem_id
        return None

    def build_composed_dist(self):
        """
        Builds an ot.ComposedDistribution from the BBRC 2019 distribution table for the
        corresponding set_id and problem_id defined in the constructor.
        """

        def switch_build_dist(dist_name, a, b, mean, std):
            if dist_name == "uniform":
                a_dist = ot.Uniform(a, b)
            elif dist_name == "exponential":
                a_dist = ot.Exponential(a)
            elif dist_name == "normal":
                a_dist = ot.Normal(a, b)
            elif dist_name == "gumbel_max":
                a_dist = ot.ParametrizedDistribution(ot.GumbelMuSigma(mean, std))
            elif dist_name == "lognormal":
                a_dist = ot.ParametrizedDistribution(ot.LogNormalMuSigma(mean, std))
            else:
                raise ValueError(
                    "Distribution not defined correctly in \
                                    probabilistic_models.csv file"
                )
            return a_dist

        types = ["i4", "i4", "i4", "i4", "U15", "f8", "f8", "f8", "f8", "f8", "f8"]
        bbrc_dist_table = np.genfromtxt(
            "./distributions/probabilistic_models.csv",
            dtype=types,
            delimiter=",",
            names=True,
        )
        my_dist_table = bbrc_dist_table[
            (bbrc_dist_table["problem_id"] == self.problem_id)
            & (bbrc_dist_table["set_id"] == self.set_id)
        ]

        ot_dist_list = []
        for raw in my_dist_table:
            ot_dist_list.append(
                switch_build_dist(
                    raw["distribution_type"],
                    raw["theta_1"],
                    raw["theta_2"],
                    raw["mean"],
                    raw["std"],
                )
            )
        composed_dist = ot.ComposedDistribution(ot_dist_list)
        return composed_dist
