from Agent import AStarAgent, GreedyAStarAgent, RealTimeAStarAgent, SaboteurAgent, HumanAgent
from Graph import Graph

#N 4
#V1
#V2 P23
#V3 P13 B
#V4 P1 B
#E1 1 2 W4
#E2 2 3 W5
#E3 1 3 W1
#E4 3 4 W6




# N 5
# V1
# V2 P12 B
# V3 B
# V4 P2
# V5 P2

# E1 1 2 W1
# E2 3 4 W1
# E3 2 3 W1
# E4 4 5 W4
# E5 1 3 W5
def ask_for_agents():
    how_many_agents = 1# int(input("how many agents"))
    agents_list = []
    for i in range(how_many_agents):
        agent_type = 5#int(input("choose type"))
        start_vertex = 0#int(input("choose start vertex"))
        assert agent_type == 1 or 2 or 3 or 4 or 5 or 6
        if agent_type == 3:
            agent = SaboteurAgent(i)
        elif agent_type == 4:
            agent = GreedyAStarAgent(i,
                                     0)  # (int(input("insert T for agent\n\n"))), (int(input("insert L for agent\n\n"))))
        elif agent_type == 5:
            agent = AStarAgent(i, 0)
        elif agent_type == 6:
            agent = HumanAgent(i)
        else:
            print("agent Type not recognized")
            continue
        agents_list.append(agent)
        graph.agent_locations[agent] = graph.vertices[start_vertex]
    return agents_list


def run_agents(world, all_agents):
    i = 0
    while all_agents:
        runnable_agents = []
        for agent in all_agents:
            action = agent(world)
            world.calculate_score()
            if not action():
                runnable_agents.append(agent)
                print(type(
                    agent).__name__ + " %d has been removed with a score of %f saved %d with the time of %d\n" % (
                          agent.id_, ((agent.state.people_saved * 1000) - agent.state.time), agent.state.people_saved,
                          agent.time))
        all_agents = runnable_agents

    i += 1
    print("simulation over\n")


if __name__ == "__main__":
    with open('input_graph.txt') as f:
        input_txt = f.read()
    graph = Graph(input_txt)
    agents = ask_for_agents()
    run_agents(graph, agents)

    # graph = Graph(input_txt)
    # agent = AStarAgent(0)
    # graph.agent_locations[agent] = graph.vertices[0]
    # agents = [agent]
    # run_agents(graph, agents)
    #
    # graph = Graph(input_txt)
    # agent = AStarAgent(1, 0.000001)
    # graph.agent_locations[agent] = graph.vertices[0]
    # agents = [agent]
    # run_agents(graph, agents)
    #
    # graph = Graph(input_txt)
    # agent = AStarAgent(2, 0.01)
    # graph.agent_locations[agent] = graph.vertices[0]
    # agents = [agent]
    # run_agents(graph, agents)
    #
    # graph = Graph(input_txt)
    # agent = GreedyAStarAgent(0)
    # graph.agent_locations[agent] = graph.vertices[0]
    # agents = [agent]
    # run_agents(graph, agents)
    #
    # graph = Graph(input_txt)
    # agent = GreedyAStarAgent(1, 0.000001)
    # graph.agent_locations[agent] = graph.vertices[0]
    # agents = [agent]
    # run_agents(graph, agents)
    #
    # graph = Graph(input_txt)
    # agent = GreedyAStarAgent(2, 0.01)
    # graph.agent_locations[agent] = graph.vertices[0]
    # agents = [agent]
    # run_agents(graph, agents)
    #
    # graph = Graph(input_txt)
    # agent = RealTimeAStarAgent(0)
    # graph.agent_locations[agent] = graph.vertices[0]
    # agents = [agent]
    # run_agents(graph, agents)
    #
    # N 4
    # V1 B
    # V2 P23
    # V3 P2
    # V4 P4
    # E1 1 2 W4
    # E2 1 3 W5
    # E3 1 4 W2
    # E4 3 4 W1
