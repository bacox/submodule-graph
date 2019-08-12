import os
import configparser
import pydot
import click

class Tree(object):
    def __init__(self, data=None):
        self.left = None
        self.children = []
        self.data = data

    def createChild(self,tree):
        self.children.append(tree)
    def getChildren(self):
        return self.children

    def getChildByURL(self, url):
        if self.data['url'] == url:
            return self
        for child in self.children:
            result = child.getChildByURL(url)
            if result is not False:
                return result
        return False

    def getData(self):
        return self.data

    def print(self, indentation=0):
        print(indentation * '---', self.data['name'])
        for child in self.children:
            child.print(indentation + 1)

    def buildGraph(self, graph, parent, indentation, graphmode):
        if graphmode == 'scattered':
            node = pydot.Node(str(indentation) + '-' + self.data['name'])
        else:
            node = pydot.Node(self.data['name'])
        indentation += 1
        if parent is not None:
            graph.add_edge(pydot.Edge(parent, node))
        graph.add_node(node)
        for child in self.children:
            [graph, indentation] = child.buildGraph(graph, node, indentation, graphmode)
            indentation += 1
        return [graph, indentation]

def parseGitModuleFile(file):
    config = configparser.ConfigParser()
    config.read(file)
    paths = []
    for section in config.sections():
        p = os.path.join(config[section]['path'])
        paths.append(p)
    return paths

def parse(path):
    if os.path.isfile(os.path.join(path, '.gitmodules')) is False:
        return Tree({'path': path, 'name': os.path.basename(os.path.normpath(path))})

    tree = Tree({'path': path, 'name': os.path.basename(os.path.normpath(path))})
    moduleFile = os.path.join(path, '.gitmodules')
    if os.path.isfile(moduleFile) is True:
        subPaths = parseGitModuleFile(moduleFile)
        for p in subPaths:
            newPath = os.path.join(path, p)
            t = parse(newPath)
            tree.createChild(t)
    return tree

@click.command()
@click.option('-m', '--mode',
              default='text',
              show_default=True,
              help="Output Mode: text | png")
@click.option('-g', '--graphmode',
              default='scattered',
              show_default=True,
              help="GraphMode: scattered | clustered")
@click.option('-o', '--out',
              default='graph',
              show_default=True,
              help="Image filename")
@click.argument('repo')
def main(mode, repo, graphmode, out):
    root = repo

    tree = parse(root)
    if mode == 'text':
        tree.print()
    else:
        graph = pydot.Dot(graph_type='digraph')
        [graph, indentation] = tree.buildGraph(graph, None, 1, graphmode)
        filename = out + '.png'
        graph.write_png(filename)


if __name__ == '__main__':
    main()