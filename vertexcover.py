#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Nicolas Golenvaux <nicolas.golenvaux@uclouvain.be>"""
from search import *
import sys


class VertexCover(Problem):

    # if you want you can implement this method and use it the maxvalue and randomized_maxvalue functions
    def successor(self, state):
        pass

    # if you want you can implement this method and use it the maxvalue and randomized_maxvalue functions
    def value(self, state):
        pass

    # if you want you can implement this method and use it the maxvalue and randomized_maxvalue functions
    def goal_test(self, state):
        pass


class State:

    def __init__(self, k, n_vertex, n_edges, vertex, edges):
        self.k = k
        self.n_vertex = n_vertex
        self.n_edges = n_edges
        self.vertex = vertex
        self.edges = edges
        self.cover = self.build_init()

    # an init state building is provided here but you can change it at will
    def build_init(self):
        return random.sample(range(self.n_vertex),self.k)

    def __str__(self):
        s = ''
        for v in self.cover:
            s += ' ' + str(v)
        return s


def read_instance(instanceFile):
    file = open(instanceFile)
    line = file.readline()
    k = int(line.split(' ')[0])
    n_vertex = int(line.split(' ')[1])
    n_edges = int(line.split(' ')[2])
    vertex = {}
    for i in range(n_vertex):
        vertex[i] = []
    edges = {}
    line = file.readline()
    while line:
        [edge,vertex1,vertex2] = [int(x) for x in line.split(' ')]
        vertex[vertex1] += [edge]
        vertex[vertex2] += [edge]
        edges[edge] = (vertex1,vertex2)
        line = file.readline()
    return k, n_vertex, n_edges, vertex, edges

# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current

    # Put your code here

    return best

# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current

    # Put your code here

    return best


#####################
#       Launch      #
#####################
if __name__ == '__main__':
    info = read_instance(sys.argv[1])
    init_state = State(info[0], info[1], info[2], info[3], info[4])
    vc_problem = VertexCover(init_state)
    step_limit = 100
    node = randomized_maxvalue(vc_problem, step_limit)
    state = node.state
    print(state)
