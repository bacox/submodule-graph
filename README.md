# Submodule Graph
Visualize Git Submodule Graphs

## Install
```
$ pip install submodulegraph
```

## Usage
```
$ submodulegraph --help

Usage: submodulegraph [OPTIONS] REPO

Options:
  -m, --mode TEXT       Output Mode: text | png  [default: text]
  -g, --graphmode TEXT  GraphMode: scattered | clustered  [default: scattered]
  -o, --out TEXT        Image filename  [default: graph]
  --help                Show this message and exit.
```

```
Examples:
# (Default) print the structure of the submodules in text in the console.
$ submodulegraph <path to repo>

# Create a png of the submodule structure where all the submodules are listed separately.
$ submodulegraph -m png <path to repo>

# Create a png of the submodule structure where all the submodules are only listed once.
$ submodulegraph -m png -g clustered <path to repo>
```