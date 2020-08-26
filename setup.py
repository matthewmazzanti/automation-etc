from setuptools import setup

NAME = "&&NAME&&"

setup(
    name=NAME,
    version="&&VERSION&&",
    py_modules=[NAME],
    entry_points={"console_scripts": [f"{{NAME}}={{NAME}}:main"]},
)
