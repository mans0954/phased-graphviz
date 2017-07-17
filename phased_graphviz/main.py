import copy
import sys

import itertools
import pydot
import subprocess

from .util import parse_phases


class PhasedGraphviz(object):
    def __init__(self, graph):
        self.graph = graph

    def copy_graph(self, graph):
        # Copy the graph objecr so we can play with it. Unfortunately, Dot.__getstate__ returns its data, not a copy of
        # it, so we can't use copy.copy() to make this prettier.
        new_graph = type(graph)()
        new_graph.__setstate__(copy.deepcopy(graph.__getstate__()))
        return new_graph

    def generate(self, base_filename, generate_gif=False, gif_delay=300):
        min_phase, max_phase = 0, 0

        # Find the min and max phases across all objects in the graph
        for obj in itertools.chain(self.graph.get_nodes(), self.graph.get_edges()):
            assert isinstance(obj, (pydot.Node, pydot.Edge))
            phases = parse_phases(obj.get('phase') or '', min_phase, max_phase)
            min_phase, max_phase = min([min_phase, *phases]), max([max_phase, *phases])

        generated_filenames = []

        # Time to start drawing. For each phase, draw the point in time transition state, and then the changes between this and
        # the next state.
        for phase in range(min_phase, max_phase+1):
            for transition in (False, True):
                # The last phase has no next phase to transition into
                if phase == max_phase and transition:
                    continue

                phase_graph = self.copy_graph(self.graph)

                for obj in itertools.chain(phase_graph.get_nodes(), phase_graph.get_edges()):
                    # Don't do anything to the nodes that provide node and edge defaults.
                    if isinstance(obj, pydot.Node) and obj.get_name() in ('node', 'edge'):
                        continue
                    assert isinstance(obj, (pydot.Node, pydot.Edge))
                    if isinstance(obj, pydot.Node):
                        obj_defaults = (phase_graph.get_node_defaults() or [{}])[0]
                    elif isinstance(obj, pydot.Edge):
                        obj_defaults = (phase_graph.get_edge_defaults() or [{}])[0]

                    obj_phases = parse_phases(obj.get('phase') or '', min_phase, max_phase)
                    obj_style = (obj.get('style') or obj_defaults.get('style') or '').split()

                    if transition:
                        in_cur_phase = phase in obj_phases
                        in_next_phase = (phase + 1) in obj_phases
                        if in_cur_phase and not in_next_phase:
                            obj.set('color', 'red')
                            obj_style.append('dotted')
                        elif not in_cur_phase and in_next_phase:
                            obj.set('color', 'green')
                        if not in_cur_phase and not in_next_phase:
                            obj_style.append('invis')
                    else:
                        if phase not in obj_phases:
                            obj_style.append('invis')

                    obj.set('style', ', '.join(obj_style))

                if transition:
                    phase_graph.set("label", "Phase {}\n(transitional changes)\n".format(phase+1))
                else:
                    phase_graph.set("label", "Phase {}\n \n".format(phase))

                filename = base_filename + '-{}{}'.format(phase, '-transition' if transition else '')
                phase_graph.write(filename + '.dot')
                subprocess.call(['dot', filename + '.dot', '-Tpng',  '-o', filename + '.png'])
                generated_filenames.append(filename + '.png')

        if generate_gif:
            # Turn all our PNGs into an animated GIF
            subprocess.check_call(['convert', '-delay', str(gif_delay), '-loop', '0'] +
                                  generated_filenames + [base_filename + '.gif'])