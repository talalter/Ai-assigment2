import sys
import networkx as nx
from queue import PriorityQueue
from State import State
from StateNode import StateNode
from action import NoOpAction, TraverseAction, TerminateAction



class Agent:
    def __init__(self, id_):
        self.seq = []
        self.state = State()
        self.id_ = id_

    def update_state(self, state, percept):
        self.state.percept = percept
        self.state.current_vertex = percept.agent_locations[self]
        return state

    def search(self):
        raise NotImplementedError

    def remainder(self, seq, state):
        if len(seq) == 0:
            return []
        if seq[0].target_vertex.is_broken and type(seq[0]) == TraverseAction:
            return []
        else:
            return seq[1:]

    def recommendation(self, seq, state):
        if len(seq) == 0:
            return TerminateAction(self)
        action = seq[0]
        if type(action) == TraverseAction and action.target_vertex.is_broken:
            return NoOpAction(self, False)
        return action

    def __call__(self, percept):
        self.state = self.update_state(self.state, percept)
        if len(self.seq) == 0:
            self.seq = self.search()
        action = self.recommendation(self.seq, self.state)
        self.seq = self.remainder(self.seq, self.state)
        return action





class AdversarialAgent(Agent):
    def __init__(self, id_, d):
        super().__init__(id_)
        self.d = d

    def search(self):

        return seq

class SemiCooperativeAgent(Agent):
    def __init__(self, id_, d):
        super().__init__(id_)
        self.d = d

    def search(self):

        return seq

class FullyCooperativeAgent(Agent):
    def __init__(self, id_, d):
        super().__init__(id_)
        self.d = d

    def search(self):

        return seq
