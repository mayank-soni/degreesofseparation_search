class Node():
    def __init__(self, state, parent, action):
        self._state = state
        self._parent = parent
        self._action = action

    def get_state(self):
        return self._state

    def is_state(self, state):
        # Added this instead of using StackFrontier.contains_state()
        # Easier to get the relevant values of parent/action if you're 
        # checking at the node level
        return self._state == state

    def get_path(self, source, frontier):
        path = [(self._action, self._state)]
        if self._parent != source:
            parent = frontier.get_parent(self._parent)
            # TODO: Error checking if parent is None. 
            path = path + parent.get_path(source, frontier)
        return path


class StackFrontier():
    def __init__(self):
        self._frontier = []
        # Added a list of checked nodes to keep track of them 
        # and not repeatedly search the same people.
        self._checked = []

    def add(self, node):
        # Checks that the node's state isn't already in the frontier or checked lists. 
        if (all(node._state != checked_node._state for checked_node in self._checked)
            and all(node._state != frontier_node._state for frontier_node in self._frontier)):
            self._frontier.append(node)

    def get_parent(self, state):
        for node in self._checked:
            if node._state == state:
                return node
        return None
    
    def empty(self):
        return len(self._frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self._frontier[-1]
            self._frontier = self._frontier[:-1]
            self._checked.append(node)
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self._frontier[0]
            self._frontier = self._frontier[1:]
            self._checked.append(node)
            return node
