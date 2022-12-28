class WorldState:
    def __init__(self, percept):
        self.broken_list = [vertex.is_broken for vertex in percept.G.nodes()]
        self.people_list = [vertex.people for vertex in percept.G.nodes()]
        self.agents_location = [percept.agent_locations[0], percept.agent_locations[1]]

    def __hash__(self):
        return hash((tuple(self.people_list), tuple(self.broken_list), tuple(self.agents_location)))

    def __eq__(self, other):
        return self.broken_list == other.broken_list and self.people_list == other.people_list and self.agents_location == other.agents_location
