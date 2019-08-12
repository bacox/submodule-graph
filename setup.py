import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="submodule-graph",
    version="0.1",
    author="Bart Cox",
    author_email="bartcox93@gmail.com",
    description="Visualize Git Submodule Graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bacox/submodule-graph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)