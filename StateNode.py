class StateNode:

    def __init__(self, people_list, broken_list, scores_tuple, location_tuple, parent=None, action=None):
        self.people_list = people_list.copy()
        self.broken_list = broken_list.copy()
        self.parent = parent
        self.scores_tuple = scores_tuple
        self.location_tuple = location_tuple

    def get_score(self):
        return self.scores_tuple[0]-self.scores_tuple[1]

    def set_parent(self, other):
        self.parent = other

    def get_info(self):
        return self.people_list, self.broken_list, self.location_tuple, self.scores_tuple

    # def __lt__(self, other):
    #     return self.node.id_ < other.node.id_

    def __eq__(self, other):
        people_list = self.people_list == other.people_list
        broken_list = self.broken_list == other.broken_list
        return people_list and broken_list

    def __repr__(self):
        return "people=%s, broken=%s location=%s, scores=%s\n" % (self.people_list, self.broken_list,
                                                                  self.location_tuple, self.scores_tuple)
