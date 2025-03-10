# Inside Assignment 3/setup.py

from setuptools import setup, find_packages

setup(
    name="assignment_3",           # Name of your package
    version="0.1.0",               # Package version
    packages=find_packages(),      # Automatically find all packages in this directory
    include_package_data=True,     # Include files from MANIFEST.in
    description="CIDM6330 - Assignment 3 with Repositories",
    author="Your Name Here",
    install_requires=[
        # List all your dependencies here, e.g.:
        # "fastapi",
        # "sqlalchemy",
        # "sqlmodel",
        # "pydantic",
        # "pytest",
        # etc.
    ],
)
