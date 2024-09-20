#!/bin/sh

set -xe
cd ..

# Show OT version
echo "Python interpreter"
echo `which python`
echo "OpenTURNS version"
python -c "import openturns; print(openturns.__version__); exit()"

# Notebooks in all subdirectories
cd examples
python scripts/analytical_functions.py
python scripts/approximation_methods.py
python scripts/ishigami-classeOTPFun.py
python scripts/main19_07.py
python scripts/simulation_methods.py
python scripts/test-computeCDF.py
python scripts/testCrue-classeOTPFun.py
python scripts/compute_reference_Morris_indices.py
python scripts/generate_reference_Morris_parameters.py
cd ..

# Unit tests
cd tests
python demo_axialbeam.py
python demo_ishigami.py
python -m unittest discover .
cd ..


