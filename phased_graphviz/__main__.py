import argparse
import os

import pydot

from .main import PhasedGraphviz


parser = argparse.ArgumentParser(
    description='Generates a series of GraphViz diagrams according to phase attributes in the source GraphViz graph',
)

parser.add_argument('filename',
                    help='The source file, with nodes and edges annotated with phases')
parser.add_argument('-b', '--base-filename', dest='base_filename', default=None,
                    help='The filename base for all generated files. Defaults to the base filename for the source file')
parser.add_argument('-g', '--gif', dest='generate_gif', action='store_true',
                    help='Whether to generate an animated GIF')
parser.add_argument('-d', '--gif-delay', dest='gif_delay', default=200, type=int,
                    help='If generating an animated GIF, the delay between frames in hundredths of a second. '
                         'Default is 200')

if __name__ == '__main__':
    args = parser.parse_args()

    graph = pydot.graph_from_dot_file(args.filename)
    base_filename = args.base_filename or os.path.splitext(args.filename)[0]

    assert isinstance(graph, pydot.Dot)

    phased_graphviz = PhasedGraphviz(graph)
    phased_graphviz.generate(base_filename, generate_gif=args.generate_gif, gif_delay=args.gif_delay)

