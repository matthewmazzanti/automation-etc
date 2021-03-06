from setuptools import setup

NAME = "room"

setup(
    name=NAME,
    version="0.0.0",
    py_modules=[NAME],
    entry_points={"console_scripts": [f"{{NAME}}={{NAME}}:main"]},
)
