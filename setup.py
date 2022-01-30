# install- pip install -e .
# it can never hurt to re-install. Just run << pip install -e . >> again.
import setuptools
# from pathlib import Path

# requierements_path = Path(__file__).parent / 'requirements.txt'

# looks for requirements
# requirements_list = []
# if requierements_path.is_file():
#    with open(requierements_path, 'r') as fd:
#        requirements_list = fd.read().split('\n')


setuptools.setup(
    name="consulManager",
    version="0.0.1",
    author="OpenAnalytics",
    description="Python package used to dental consultories",
    long_description="Python package used to dental consultories",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    #install_requires=requirements_list,
    python_requires='>=3.8',
)
