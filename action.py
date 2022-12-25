class Action:
    def __init__(self, agent):
        self.target_vertex = agent.state.current_vertex
        self.agent = agent
        self.graph = agent.world

    def __call__(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__class__.__name__

    def move(self, pickup):
        current_location = self.agent.current_vertex
        self.graph.change_agent_location(self.agent, self.target_vertex)
        if pickup:
            self.agent.score += self.target_vertex.people
            self.graph.total_number_of_people_evacuated += self.target_vertex.people
            self.target_vertex = self.target_vertex.take_people()
        if self.target_vertex.is_brittle:
            self.target_vertex.is_broken = True
        self.agent.time += 1
        print(f"Agant {self.agent.id_} has moved from {current_location} to {self.target_vertex} with score "
              f"{self.agent.score}")
        print(self.graph)


class TraverseAction(Action):
    def __init__(self, agent, target_vertex, pickup=True):
        super().__init__(agent)
        self.target_vertex = target_vertex
        self.pickup = pickup

    def __call__(self):
        if self.graph.agent_locations[self.agent.id_] == self.target_vertex:
            raise Exception(F"this is is traverse action, why {self.agent} is moving to him self?")
        #
        # for neighbor in self.graph.get_neighbors(self.agent.state.current_vertex):
        #     if neighbor == self.target_vertex:
        self.move(self.pickup)
        self.agent.current_vertex = self.target_vertex
        # self.agent.state.time += linked_vertexes1[0][1]
        return False


class NoOpAction(Action):
    def __init__(self, agent, pickup):
        super().__init__(agent)
        self.pickup = pickup

    def __call__(self):
        self.agent.time += 1
        self.move(self.pickup)
        return False
