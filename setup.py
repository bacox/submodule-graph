import setuptools

def install_requires():
    return ['click', 'pydot', 'configparser']

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="submodulegraph",
    version="0.1.5",
    author="Bart Cox",
    author_email="bartcox93@gmail.com",
    py_modules=['submodulegraph'],
    description="Visualize Git Submodule Graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bacox/submodule-graph",
    install_requires=install_requires(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        submodulegraph=submodulegraph:main
    """,
)