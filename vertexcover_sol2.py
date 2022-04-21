#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Nicolas Golenvaux <nicolas.golenvaux@uclouvain.be>"""
from search import *
import sys


class MaximumVertexCover(Problem):

    # if you want you can implement this method and use it the maxvalue and randomized_maxvalue functions
    def successor(self, state):
        for u in state.cover:
            for v in state.not_cover:
                yield (None,State(state.k,state.vertices,state.edges,[x for x in state.cover if x != u]+[v],[x for x in state.not_cover if x != v]+[u]))


    # if you want you can implement this method and use it the maxvalue and randomized_maxvalue functions
    def value(self, state):
        edges_covered = []
        for v in state.cover:
            for e in state.vertices[v]:
                if e not in edges_covered:
                    edges_covered += [e]
        return len(edges_covered)


class State:

    def __init__(self, k, vertices, edges, cover=None, not_cover=None):
        self.k = k
        self.n_vertices = len(vertices)
        self.n_edges = len(edges)
        self.vertices = vertices
        self.edges = edges
        if cover is None:
            self.cover = self.build_init()
        else:
            self.cover = cover
        if not_cover is None:
            self.not_cover = [v for v in range(self.n_vertices) if v not in self.cover]
        else:
            self.not_cover = not_cover

    # an init state building is provided here but you can change it at will
    def build_init(self):
        return list(range(self.k))

    def __str__(self):
        s = ''
        for v in self.cover:
            s += ' ' + str(v)
        return s


def read_instance(instanceFile):
    file = open(instanceFile)
    line = file.readline()
    k = int(line.split(' ')[0])
    n_vertices = int(line.split(' ')[1])
    n_edges = int(line.split(' ')[2])
    vertices = {}
    for i in range(n_vertices):
        vertices[i] = []
    edges = []
    line = file.readline()
    while line:
        [edge,vertex1,vertex2] = [int(x) for x in line.split(' ')]
        vertices[vertex1] += [edge]
        vertices[vertex2] += [edge]
        if (vertex1,vertex2) in edges:
            print('already in : ',edge)
        else:
            edges.append((vertex1,vertex2))
        line = file.readline()
    return k, vertices, edges

# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    best_val = current.value()
    for step in range(limit):
        best_succ = None
        best_succ_val = 0
        for successor in current.expand():
            val = successor.value()
            if val > best_succ_val:
                best_succ = successor
                best_succ_val = val
        current = best_succ
        if best_succ_val > best_val:
            best = current
            best_val = best_succ_val
    return best

# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    best_val = current.value()
    for step in range(limit):
        best_succ = [None,None,None,None,None]
        best_succ_val = [0,0,0,0,0]
        min_best_val = 0
        min_best_index = 0
        for successor in current.expand():
            val = successor.value()
            if val > min_best_val:
                best_succ[min_best_index] = successor
                best_succ_val[min_best_index] = val
                min_best_val = min(best_succ_val)
                min_best_index = best_succ_val.index(min_best_val)
                if val > best_val:
                    best = successor
                    best_val = val
        current = random.choice(best_succ)
    return best


#####################
#       Launch      #
#####################
if __name__ == '__main__':
    info = read_instance(sys.argv[1])
    init_state = State(info[0], info[1], info[2])
    mvc_problem = MaximumVertexCover(init_state)
    step_limit = 100
    node = maxvalue(mvc_problem, step_limit)
    state = node.state
    print('max val')
    print('step : '+ str(node.step))
    print('val : ' + str(mvc_problem.value(state)))
    node = randomized_maxvalue(mvc_problem, step_limit)
    state = node.state
    print('random max val')
    print('step : ' + str(node.step))
    print('val : ' + str(mvc_problem.value(state)))
