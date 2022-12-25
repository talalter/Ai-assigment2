import sys
import networkx as nx
from queue import PriorityQueue
from State import State
from StateNode import StateNode
from action import NoOpAction, TraverseAction


def run_dijkstra(source, world_graph, heurstic_graph):
    vertices_to_weight = dict()
    for target in heurstic_graph:
        if nx.has_path(world_graph, source, target):
            weight = nx.shortest_path_length(world_graph, source, target, weight="weight")
            vertices_to_weight[target] = weight
    return source, vertices_to_weight


def prepare_to_dijkstra(graph_for_heuristic, graph, broken_list):
    world_graph_without_b = graph.G.copy()
    for node in graph.G.nodes():
        if broken_list[node.id_]:
            world_graph_without_b.remove_node(node)
    return [run_dijkstra(node, world_graph_without_b, graph_for_heuristic.nodes()) for node in
            graph_for_heuristic.nodes()]


def heuristic(graph, state_node):
    graph_for_heuristic = nx.Graph()
    current_vertex, people_list, broken_list = state_node.get_info()
    for vertex in graph.vertices:
        if (people_list[vertex.id_] and not broken_list[vertex.id_]) or (
                vertex == state_node.node and not broken_list[vertex.id_]):
            graph_for_heuristic.add_node(vertex)
    if graph_for_heuristic.number_of_nodes() == 1:
        return 0
    shortest_path_to_each_vertex = prepare_to_dijkstra(graph_for_heuristic, graph, broken_list)
    for info in shortest_path_to_each_vertex:
        source, targets = info
        for target, weight in targets.items():
            if target is not source:
                graph_for_heuristic.add_edge(target, source, weight=weight)
    mst = nx.minimum_spanning_tree(graph_for_heuristic)

    return mst.size(weight="weight")


def return_path(node_state):
    path = []
    current_state = node_state
    while current_state is not None:
        path.append(current_state.node)
        current_state = current_state.parent

    return path[::-1]


def is_terminal_state(state, state_lists):
    return is_goal(state) or state in state_lists


def is_goal(state):
    people_list = state.people_list
    for i in people_list:
        if i != 0:
            return False
    return True


class Agent:
    def __init__(self, id_):
        self.seq = []
        self.state = State()
        self.id_ = id_
        self.final_path = []
        self.people_saved = 0
        self.time = 0
        self.score = 0

    def __str__(self):
        res = f"Agent from type {type(self)} path was: "
        res += "--->".join(list(map(lambda node: str(node), self.final_path)))
        res += "\nand saved"
        res += f"{self.people_saved} people in time of {self.time}"

    def pick(self, vertex):
        self.people_saved += vertex.people

    def add_to_path(self, vertex):
        self.final_path.append(vertex)

    def update_state(self, state, percept):
        self.state.set_percept(percept)
        self.state.set_current_vertex(percept.get_node(percept.agent_locations[self]))
        return state


class MaxAgent(Agent):
    def __init__(self, start_vertex, world):
        super().__init__(0)
        self.current_vertex = start_vertex
        self.world = world


class MinAgent(Agent):
    def __init__(self, start_vertex, world):
        super().__init__(1)
        self.current_vertex = start_vertex
        self.world = world

