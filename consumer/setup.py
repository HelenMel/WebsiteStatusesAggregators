import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_requirements(req_file):
    """Read requirements file and return packages and git repos separately"""
    requirements = []
    lines = read(req_file).split("\n")
    for line in lines:
        requirements.append(line)
    return requirements

REQ_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pip-dep")
core_requirements = get_requirements(os.path.join(REQ_DIR, "requirements.txt"))

setup(
    name="consumer",
    version="0.0.1",
    author = "olena babenko",
    author_email = "to.helen.babenko@gmail.com",
    description = ("This is hometast project"),
    python_requires='>=3.7.0',
    url = "https://github.com/HelenMel/WebsiteStatusesAggregators",
    license='MIT',
    packages=find_packages(exclude=["docs", "examples", "dist"]),
    include_package_data=True,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    install_requires=core_requirements,
    test_suite="tests"
)