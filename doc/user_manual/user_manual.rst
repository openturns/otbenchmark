API Reference
=============

.. currentmodule:: otbenchmark

Reliability problems
--------------------

.. autosummary::
    :toctree: _generated/
    :template: class.rst_t
  
    ReliabilityBenchmarkProblem
    AxialStressedBeamReliability
    RminusSReliability
    FourBranchSerialSystemReliability
    ReliabilityProblem53
    ReliabilityProblem22
    ReliabilityProblem24
    ReliabilityProblem25
    ReliabilityProblem28
    ReliabilityProblem31
    ReliabilityProblem35
    ReliabilityProblem55
    ReliabilityProblem57
    ReliabilityProblem75
    ReliabilityProblem89
    ReliabilityProblem110
    ReliabilityProblem111
    ReliabilityProblem33
    ReliabilityProblem8
    ReliabilityProblem14
    ReliabilityProblem38
    ReliabilityProblem54
    ReliabilityProblem107
    ReliabilityProblem91
    ReliabilityProblem63
    ReliabilityProblem60
    ReliabilityProblem77
    
Reliability methods
-------------------

.. autosummary::
    :toctree: _generated/
    :template: class.rst_t

    FORM
    SORM
    SubsetSampling
    ProbabilitySimulationAlgorithmFactory
    LHS
    ReliabilityBenchmarkMetaAlgorithm
    ReliabilityBenchmarkResult
    ConditionalDistribution
    CrossCutFunction
    CrossCutDistribution
    DrawEvent

    :template: function.rst_t

    ReliabilityLibrary.ComputeLogRelativeError
    ReliabilityLibrary.ComputeAbsoluteError
    ReliabilityLibrary.ComputeRelativeError
    ReliabilityLibrary.ReliabilityBenchmarkProblemList

Sensitivity problems
--------------------

.. autosummary::
    :toctree: _generated/
    :template: class.rst_t

    SensitivityBenchmarkProblem
    BoreholeSensitivity
    BorgonovoSensitivity
    OakleyOHaganSensitivity
    DirichletSensitivity
    FloodingSensitivity
    NLOscillatorSensitivity
    GaussianSumSensitivity
    GaussianProductSensitivity
    GSobolSensitivity
    MorrisSensitivity
    IshigamiSensitivity

    :template: function.rst_t

    SensitivityLibrary.SensitivityBenchmarkProblemList
    
Sensitivity methods
-------------------

.. autosummary::
    :toctree: _generated/
    :template: class.rst_t
    
    SparsePolynomialChaosSensitivityAnalysis
    SensitivityBenchmarkMetaAlgorithm
    SensitivityConvergence
    SensitivityDistribution
    JanonSensitivityAlgorithm
