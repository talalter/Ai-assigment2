from Agent import AdversarialAgent, SemiCooperativeAgent, FullyCooperativeAgent
from Graph import Graph
from WorldState import WorldState

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
def ask_for_gameType():
    gameType = int(input("game type? 1 for adv 2 for semi 3 for full\n"))
    cutoff = int(input("depth of cuttof for agents root is 0\n"))
    assert gameType == 1 or 2 or 3
    agents_list = []
    for i in range(2):
        start_vertex = int(input("choose start vertex\n"))
        assert gameType == 1 or 2 or 3
        if gameType == 1:
            agent = AdversarialAgent(i, cutoff)
        elif gameType == 2:
            agent = SemiCooperativeAgent(i, cutoff)
        elif gameType == 3:
            agent = FullyCooperativeAgent(i, cutoff)
        agents_list.append(agent)
        graph.agent_locations[agent] = graph.vertices[start_vertex]
    return agents_list



def run_agents(graph, all_agents):
    i = 0
    world_state_dict = dict()
    while all_agents:
        runnable_agents = []
        for agent in all_agents:
            world_state = WorldState(graph)
            if world_state_dict.get(world_state) == world_state:
                print("game has ended\n")
                agent = all_agents[0]
                print(type(
                    agent).__name__ + " %d has been removed with a score of %f saved %d with the time of %d\n" % (
                          agent.id_, ((agent.state.people_saved * 1000) - agent.state.time), agent.state.people_saved,
                          agent.time))
                agent = all_agents[1]
                print(type(
                    agent).__name__ + " %d has been removed with a score of %f saved %d with the time of %d\n" % (
                          agent.id_, ((agent.state.people_saved * 1000) - agent.state.time), agent.state.people_saved,
                          agent.time))
                exit(0)# game over
            action = agent(graph)
            graph.calculate_score()
            if not action():
                runnable_agents.append(agent)
                print(type(
                    agent).__name__ + " %d has been removed with a score of %f saved %d with the time of %d\n" % (
                          agent.id_, ((agent.state.people_saved * 1000) - agent.state.time), agent.state.people_saved,
                          agent.time))
            else:
                raise Exception("why did you terminate this is not possible in this essignment")
        all_agents = runnable_agents

    i += 1
    print("simulation over\n")


if __name__ == "__main__":
    with open('input_graph.txt') as f:
        input_txt = f.read()
    graph = Graph(input_txt)
    agents = ask_for_gameType()
    run_agents(graph, agents)
