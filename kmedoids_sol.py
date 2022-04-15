#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Nicolas Golenvaux <nicolas.golenvaux@uclouvain.be>"""
from search import *
import sys


class KMedoids(Problem):

    def __init__(self, k, n_points, points, initial=None):
        self.k = k
        self.n_points = n_points
        self.points = points
        self.initial = initial
        if initial is None:
            self.initial = self.build_init()

    # an init state building is provided here but you can change it at will
    def build_init(self):
        medoids = random.sample(list(range(self.n_points)),self.k)
        others = [point for point in range(self.n_points) if point not in medoids]
        return State(medoids, others)

    def assign_metroid(self,medoids):
        clusters = dict.fromkeys(medoids)
        for point in range(self.n_points):
            if point not in medoids:
                best = None
                for medoid in medoids

    # if you want you can implement this method and use it the maxvalue and randomized_maxvalue functions
    def successor(self, state):
        for u in state.medoids:
            for v in state.others:
                yield (None,State([x for x in state.medoids if x != u]+[v],[x for x in state.others if x != v]+[u]))


    # if you want you can implement this method and use it the maxvalue and randomized_maxvalue functions
    def value(self, state):
        edges_covered = []
        for v in state.cover:
            for e in self.vertex[v]:
                if e not in edges_covered:
                    edges_covered += [e]
        return len(edges_covered)

    # if you want you can implement this method and use it the maxvalue and randomized_maxvalue functions
    def goal_test(self, state):
        return self.value(state) == self.n_edges


class State:

    def __init__(self, cover, not_cover):
        self.cover = cover
        self.not_cover = not_cover

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
    mvc_problem = MaximumVertexCover(info[0], info[1], info[2], info[3], info[4])
    step_limit = 20
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
