from setuptools import setup, find_packages

setup(
    name="pandas_interactive_html",
    version="0.1.0",
    description="add to_interactive_html method to pandas",
    license="BSD-3-Clause",
    author="Hirotomo Moriwaki",
    author_email="philopon.dependence@gmail.com",
    url="https://github.com/philopon/pandas_interactive_html",
    platforms=["any"],

    packages=find_packages(),

    package_data={
        "pandas_interactive_html": ["bundle.js"],
    },

    install_requires=[
        "pandas>=0.20"
    ],
)
