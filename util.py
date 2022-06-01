class Node():
    def __init__(self, state, path):
        self._state = state
        # self._parent = parent
        # self._action = action
        self._path = path

    def get_state(self):
        return self._state

    def get_path(self):
        return self._path

    # Original implementation, when the nodes contained a parent and action instead of a path. 
    # def get_path(self, source, frontier):
    #     path = [(self._action, self._state)]
    #     if self._parent != source:
    #         parent = frontier.get_parent(self._parent)
    #         # TODO: Error checking if parent is None. 
    #         path = path + parent.get_path(source, frontier)
    #     return path


class QueueFrontier():
    def __init__(self):
        self._frontier = []
        # Added a list of checked nodes to keep track of them 
        # and not repeatedly search the same people.
        self._checked = []

    def add(self, nodes):
        # Generate list of states that have been checked or are already in frontier
        checked_states = [node.get_state() for node in (self._checked + self._frontier)]
        # Filter the list of nodes to identify those that are not already in checked_states, and add them
        non_overlapping_nodes = [node for node in nodes if node.get_state() not in checked_states]
        self._frontier = self._frontier + non_overlapping_nodes

    # def get_parent(self, state):
    #     for node in self._checked:
    #         if node.get_state() == state:
    #             return node
    #     return None
    
    def empty(self):
        return len(self._frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self._frontier[0]
            self._frontier = self._frontier[1:]
            self._checked.append(node)
            return node