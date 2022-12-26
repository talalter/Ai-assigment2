class State:
    def __init__(self, percept):
        self.broken_list = [vertex.people for vertex in percept.G.nodes()]
        self.people_saved = [vertex.is_broken for vertex in percept.G.nodes()]
        self.agents_location = [percept.agent_locations[0], percept.agent_locations[1]]

    def __hash__(self):
        return hash((tuple(self.people_list), tuple(self.broken_list), tuple(self.agents_location)))
