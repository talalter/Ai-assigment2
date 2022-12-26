from State import State
from StateNode import StateNode
from action import NoOpAction, TraverseAction, TerminateAction


def generate_state(state):
    people_list = [vertex.people for vertex in state.percept.G.nodes()]
    broken_list = [vertex.is_broken for vertex in state.percept.G.nodes()]
    scores_tuple = [0, 0]
    location_tuple = [state.percept.agent_locations[0], state.percept.agent_locations[1]]
    return StateNode(people_list, broken_list, scores_tuple, location_tuple)


def return_path(node_state):
    path = []
    current_state = node_state
    while current_state is not None:
        path.append(current_state.action)
        current_state = current_state.parent
    return path[::-1][1:]


def minimax_decision(agent1, agent2, state, world, turn_of_max, depth=6, alpha=float('-inf'), beta=float('inf')):
    if is_terminal_state(state) or depth == 0:
        return state.get_score(), state
    people_list, broken_list, location_tuple, scores_tuple = state.get_info()
    if turn_of_max:
        max_eval = float('-inf'), None
        for son in world.get_neighbors(location_tuple[agent1.id_]):
            son_people_list = people_list.copy()
            son_broken_list = broken_list.copy()
            son_location_tuple = location_tuple.copy()
            son_scores_tuple = scores_tuple.copy()
            if not broken_list[son.id_]:
                action = TraverseAction(agent1, son)
                if son.is_brittle:
                    broken_list[son.id_] = True
                son_scores_tuple[0] += son_people_list[son.id_]
                son_people_list[son.id_] = 0
                son_location_tuple[0] = son
                new_state = StateNode(son_people_list, son_broken_list, son_scores_tuple,
                                      son_location_tuple, parent=state, action=action)
                eval_score, rec_state = minimax_decision(agent1, agent2, new_state, world, False, depth - 1)
                max_eval = max_eval if max_eval[0] >= eval_score else (eval_score, rec_state)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf'), None
        for son in world.get_neighbors(location_tuple[agent2.id_]):
            son_people_list = people_list.copy()
            son_broken_list = broken_list.copy()
            son_location_tuple = location_tuple.copy()
            son_scores_tuple = scores_tuple.copy()
            if not broken_list[son.id_]:
                action = TraverseAction(agent2, son)
                if son.is_brittle:
                    broken_list[son.id_] = True
                son_scores_tuple[1] += son_people_list[son.id_]
                son_people_list[son.id_] = 0
                son_location_tuple[1] = son
                new_state = StateNode(son_people_list, son_broken_list, son_scores_tuple,
                                      son_location_tuple, parent=state, action=action)
                eval_score, rec_state = minimax_decision(agent1, agent2, new_state, world, True, depth - 1)
                min_eval = min_eval if min_eval[0] <= eval_score else (eval_score, rec_state)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return min_eval


class Agent:
    def __init__(self, id_):
        self.seq = []
        self.state = State()
        self.id_ = id_

    def update_state(self, state, percept):
        self.state.percept = percept
        self.state.current_vertex = percept.agent_locations[self.id_]
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
    def __init__(self, id_, t=0, l=1):
        super().__init__(id_)
        self.t = t
        self.l = l

    def search(self):
        node_state = generate_state(self.state)
        other_agent = None
        for agent in self.state.percept.agents:
            if agent != self:
                other_agent = agent
        score, path_nodes = minimax_decision(self, other_agent, node_state, self.state.percept, True, 2)
        actions_to_leaf = return_path(path_nodes)
        # seq = list(map(lambda x: TraverseAction(self, x.node, True), temp))
        # self.state.time += n * self.t
        # print(actions_to_leaf)
        return actions_to_leaf


class SemiCooperativeAgent(Agent):
    def __init__(self, id_, t=0, l=1):
        super().__init__(id_)
        self.t = t
        self.l = l

    def search(self):
        pass


class FullyCooperativeAgent(Agent):
    def __init__(self, id_, t=0, l=1):
        super().__init__(id_)
        self.t = t
        self.l = l

    def search(self):
        pass
