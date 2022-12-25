from Agent import MaxAgent, MinAgent
from Graph import Graph
from StateNode import StateNode
from action import TraverseAction


def is_terminal_state(state):
    return is_goal(state)  # or state in state_lists


def is_goal(state):
    people_list = state.people_list
    for i in people_list:
        if i != 0:
            return False
    return True


def return_path(node_state):
    path = []
    current_state = node_state
    while current_state is not None:
        path.append(current_state.action)
        current_state = current_state.parent
    return path[::-1][1:]


class Game:
    def __init__(self, world, agents):
        self.world = world
        self.A = agents[0]
        self.B = agents[1]
        self.current_state = self.generate_state()

    def adversarial(self):
        res_node = self.minimax_decision(self.current_state, True)
        all_actions = return_path(res_node[1])
        for action in all_actions:
            action()

    def semi_cooperative(self):
        a = self.semi_cooperative_decision(self.current_state, True)
        all_actions = return_path(a[1][1])
        for action in all_actions:
            action()
    def fully_cooperative(self):
        a = self.fully_cooperative_decision(self.current_state, True)
        all_actions = return_path(a[1])
        for action in all_actions:
            action()

    def generate_state(self, state=None):
        people_list = [vertex.people for vertex in self.world.G.nodes()]
        broken_list = [vertex.is_broken for vertex in self.world.G.nodes()]
        scores_tuple = [0, 0]
        location_tuple = [self.world.agent_locations[0], self.world.agent_locations[1]]
        return StateNode(people_list, broken_list, scores_tuple, location_tuple, parent=state)

    def semi_cooperative_decision(self, state, turn_of_A, depth=3):
        if is_terminal_state(state) or depth == 0:
            return state.scores_tuple, state
        people_list, broken_list, location_tuple, scores_tuple = state.get_info()
        if turn_of_A:
            max_eval = [float('-inf'), float('-inf')], None
            for son in self.world.get_neighbors(location_tuple[0]):
                son_people_list = people_list.copy()
                son_broken_list = broken_list.copy()
                son_location_tuple = location_tuple.copy()
                son_scores_tuple = scores_tuple.copy()
                if not broken_list[son.id_]:
                    action = TraverseAction(self.A, son)
                    if son.is_brittle:
                        broken_list[son.id_] = True
                    son_scores_tuple[0] += son_people_list[son.id_]
                    son_people_list[son.id_] = 0
                    son_location_tuple[0] = son
                    new_state = StateNode(son_people_list, son_broken_list, son_scores_tuple,
                                          son_location_tuple, parent=state, action=action)
                    eval, state = self.semi_cooperative_decision(new_state, False, depth - 1)
                    max_eval = eval, state if eval[0] >= max_eval[0][0] and eval[1] >= max_eval[0][1] else max_eval
            return max_eval
        else:
            min_eval = [float('inf'), float('inf')], None
            for son in self.world.get_neighbors(location_tuple[1]):
                son_people_list = people_list.copy()
                son_broken_list = broken_list.copy()
                son_location_tuple = location_tuple.copy()
                son_scores_tuple = scores_tuple.copy()
                if not broken_list[son.id_]:
                    action = TraverseAction(self.B, son)
                    if son.is_brittle:
                        broken_list[son.id_] = True
                    son_scores_tuple[1] += son_people_list[son.id_]
                    son_people_list[son.id_] = 0
                    son_location_tuple[1] = son
                    new_state = StateNode(son_people_list, son_broken_list, son_scores_tuple,
                                          son_location_tuple, parent=state, action=action)
                    eval, state = self.semi_cooperative_decision(new_state, True, depth - 1)
                    min_eval = eval, state if eval[0] <= min_eval[0][0] and eval[1] <= min_eval[0][1] else min_eval
            return min_eval

    def fully_cooperative_decision(self, state, turn_of_A, depth=2):
        if is_terminal_state(state) or depth == 0:
            return state.scores_tuple[0] + state.scores_tuple[1]
        people_list, broken_list, location_tuple, scores_tuple = state.get_info()
        if turn_of_A:
            max_eval = float('-inf')
            for son in self.world.get_neighbors(location_tuple[0]):
                son_people_list = people_list.copy()
                son_broken_list = broken_list.copy()
                son_location_tuple = location_tuple.copy()
                son_scores_tuple = scores_tuple.copy()
                if not broken_list[son.id_]:
                    action = TraverseAction(self.A, son)
                    if son.is_brittle:
                        broken_list[son.id_] = True
                    son_scores_tuple[0] += son_people_list[son.id_]
                    son_people_list[son.id_] = 0
                    son_location_tuple[0] = son
                    new_state = StateNode(son_people_list, son_broken_list, son_scores_tuple,
                                          son_location_tuple, parent=state, action=action)
                    eval = self.fully_cooperative_decision(new_state, False, depth - 1)
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('-inf')
            for son in self.world.get_neighbors(location_tuple[1]):
                son_people_list = people_list.copy()
                son_broken_list = broken_list.copy()
                son_location_tuple = location_tuple.copy()
                son_scores_tuple = scores_tuple.copy()
                if not broken_list[son.id_]:
                    action = TraverseAction(self.B, son)
                    if son.is_brittle:
                        broken_list[son.id_] = True
                    son_scores_tuple[1] += son_people_list[son.id_]
                    son_people_list[son.id_] = 0
                    son_location_tuple[1] = son
                    new_state = StateNode(son_people_list, son_broken_list, son_scores_tuple,
                                          son_location_tuple, parent=state, action=action)
                    eval = self.fully_cooperative_decision(new_state, True, depth - 1)
                    min_eval = max(min_eval, eval)
            return min_eval

    def minimax_decision(self, state, turn_of_A, depth=3, alpha=float('-inf'), beta=float('inf')):
        if is_terminal_state(state) or depth == 0:
            return state.get_score(), state
        people_list, broken_list, location_tuple, scores_tuple = state.get_info()
        if turn_of_A:
            max_eval = float('-inf'), None
            for son in self.world.get_neighbors(location_tuple[0]):
                son_people_list = people_list.copy()
                son_broken_list = broken_list.copy()
                son_location_tuple = location_tuple.copy()
                son_scores_tuple = scores_tuple.copy()
                if not broken_list[son.id_]:
                    action = TraverseAction(self.A, son)
                    if son.is_brittle:
                        broken_list[son.id_] = True
                    son_scores_tuple[0] += son_people_list[son.id_]
                    son_people_list[son.id_] = 0
                    son_location_tuple[0] = son
                    new_state = StateNode(son_people_list, son_broken_list, son_scores_tuple,
                                          son_location_tuple, parent=state, action=action)
                    eval_score, rec_state = self.minimax_decision(new_state, False, depth - 1)
                    max_eval = max_eval if max_eval[0] >= eval_score else (eval_score, rec_state)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf'), None
            for son in self.world.get_neighbors(location_tuple[1]):
                son_people_list = people_list.copy()
                son_broken_list = broken_list.copy()
                son_location_tuple = location_tuple.copy()
                son_scores_tuple = scores_tuple.copy()
                if not broken_list[son.id_]:
                    action = TraverseAction(self.B, son)
                    if son.is_brittle:
                        broken_list[son.id_] = True
                    son_scores_tuple[1] += son_people_list[son.id_]
                    son_people_list[son.id_] = 0
                    son_location_tuple[1] = son
                    new_state = StateNode(son_people_list, son_broken_list, son_scores_tuple,
                                          son_location_tuple, parent=state, action=action)
                    eval_score, rec_state = self.minimax_decision(new_state, True, depth - 1)
                    min_eval = min_eval if min_eval[0] <= eval_score else (eval_score, rec_state)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            return min_eval


if __name__ == "__main__":
    with open('input_graph.txt') as f:
        input_txt = f.read()
    graph = Graph(input_txt)
    start_node = graph.get_node(0)
    graph.agent_locations[0] = start_node
    graph.agent_locations[1] = start_node
    A = MaxAgent(start_node, graph)
    B = MinAgent(start_node, graph)
    g = Game(graph, [A, B])
    # g.adversarial()
    g.semi_cooperative()
    # g.fully_cooperative()
