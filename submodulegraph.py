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

    def print(self, indentation=0, with_url=False):
        label = self._getLabel(with_url)
        indent = indentation * '---'
        # Add spacing when we actually indent
        indent += ' ' if indent else ''
        print(indent + label)
        for child in self.children:
            child.print(indentation + 1, with_url)

    def buildGraph(self, graph, parent, indentation, graphmode, with_url):
        label = self._getLabel(with_url, '\n')
        # Add explicit quotation marks to avoid parsing confusion in dot
        if graphmode == 'scattered':
            node = pydot.Node('"' + str(indentation) + '-' + label + '"')
        else:
            node = pydot.Node('"' + label + '"')
        indentation += 1
        if parent is not None:
            graph.add_edge(pydot.Edge(parent, node))
        graph.add_node(node)
        for child in self.children:
            [graph, indentation] = child.buildGraph(
                graph, node, indentation, graphmode, with_url)
            indentation += 1
        return [graph, indentation]

    def _getLabel(self, with_url, sep=' - '):
        label = self.data['name']
        if with_url and 'url' in self.data and self.data['url']:
            label += sep + self.data['url']
        return label

def parseGitModuleFile(file):
    config = configparser.ConfigParser()
    config.read(file)
    res = []
    for section in config.sections():
        p = os.path.join(config[section]['path'])
        u = config[section]['url']
        res.append((p, u))
    return res

def parse(path, url=None):
    if os.path.isfile(os.path.join(path, '.gitmodules')) is False:
        return Tree({'name': os.path.basename(os.path.normpath(path)),
                     'path': path, 'url': url})

    tree = Tree({'name': os.path.basename(os.path.normpath(path)),
                 'path': path, 'url': url})
    moduleFile = os.path.join(path, '.gitmodules')

    if os.path.isfile(moduleFile) is True:
        subs = parseGitModuleFile(moduleFile)
        for p, u in subs:
            newPath = os.path.join(path, p)
            newTree = parse(newPath, u)
            tree.createChild(newTree)
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
@click.option('-u', '--with-url',
              default=False, is_flag=True,
              show_default=True,
              help="Add repo URLs")
@click.argument('repo')
def main(mode, repo, graphmode, out, with_url):
    root = repo
    tree = parse(root)

    if mode == 'text':
        tree.print(with_url=with_url)
    else:
        graph = pydot.Dot(graph_type='digraph')
        [graph, indentation] = tree.buildGraph(graph, None, 1, graphmode, with_url)
        filename = out + '.png'
        graph.write_png(filename)


if __name__ == '__main__':
    main()
