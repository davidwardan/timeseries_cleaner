from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="timeseries_cleaner",
    version="0.3.0",
    description="Time-series preprocessing library: outlier removal, resampling, trend removal, plotting, etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourname/timeseries_cleaner",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        "pandas>=1.4",
        "numpy>=1.22",
        "prophet>=1.1",
        "scikit-learn>=1.3",
        "matplotlib>=3.5",
        "rich>=13.0",
    ],
    python_requires=">=3.8",
)