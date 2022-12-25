from Agent import Agent, HumanAgent
from Vertex import Vertex
from Graph import Graph


def parse_config(config_):
    num_vertex = 0
    all_vertices = []
    all_edges = []
    for line in config_.split('\n'):

        if len(line) > 0:
            first_letter = line[1]
            if first_letter == 'N':
                num_vertex = int(line[3:])
            elif first_letter == 'V':
                info_on_vertex = line[1:].split()
                if len(info_on_vertex) == 1:
                    vertex_name = int(info_on_vertex[0][1:]) - 1
                    amount_of_people = 0  # maybe 0 or False
                    vertex_is_brittle = False
                    all_vertices.append((vertex_name, amount_of_people, vertex_is_brittle))
                elif len(info_on_vertex) == 2:
                    vertex_name = int(info_on_vertex[0][1:]) - 1
                    if 'P' in info_on_vertex[1]:
                        amount_of_people = info_on_vertex[1][1:]
                        vertex_is_brittle = False
                    else:
                        amount_of_people = 0  # maybe 0 or False
                        vertex_is_brittle = True
                    all_vertices.append((vertex_name, amount_of_people, vertex_is_brittle))
                else:
                    vertex_name = int(info_on_vertex[0][1:]) - 1
                    amount_of_people = info_on_vertex[1][1:]
                    vertex_is_brittle = True
                    all_vertices.append((vertex_name, amount_of_people, vertex_is_brittle))
            else:
                info_on_vertex = line[1:].split()
                all_edges.append(tuple(info_on_vertex))
    return num_vertex, all_vertices, all_edges


def build_dict_graph(vertices_list, edges_list):
    dict_graph = dict()
    for vertex in vertices_list:
        vertex_id = vertex[0]
        current_vertex_to_add = Vertex(vertex_id, vertex[1], vertex[2])
        edges_of_current_vertex = []
        for edge in edges_list:
            if edge[1] == vertex_id or edge[2] == vertex_id:
                edges_of_current_vertex.append((edge[0], "V" + edge[2], edge[3]))
            else:
                if edge[2] == vertex_id:
                    edges_of_current_vertex((edge[0], "V" + edge[1], edge[3]))

                dict_graph[current_vertex_to_add] = edges_of_current_vertex
    return dict_graph


class Problem:

    def __init__(self, graph, broken_vertices, peoples):
        self.graph = graph
        self.broken_vertices = broken_vertices
        self.peoples = peoples


if __name__ == "__main__":
    config_ = '''
#N 4      
#V1                  
#V2 P12 B             
#V3 B                
#V4 P2               

#E1 1 2 W1                 
#E2 3 4 W1                 
#E3 2 3 W1                 
#E4 1 3 W4                 
#E5 2 4 W5                 
'''

    graph = Graph(config_)
    print(graph)
    agent = HumanAgent(1, 2, graph)
    agent.run()
