import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                # Note to self: This is generating a set, since the curly braces only enclose a single element
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Source name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Target name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        if degrees == 1:
            print(f"{degrees} degree of separation.")
        else:
            print(f"{degrees} degrees of separation.")
        for i in range(degrees):
            if i == 0:
                person1 = people[source]["name"]
            else:
                person1 = people[path[i - 1][1]]["name"]
            person2 = people[path[i][1]]["name"]
            movie = movies[path[i][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # Let's use breadth-first search, which is guaranteed to provide the 
    # shortest path even though it may take a while to do it. 
    # Each state is a person ID. Each action is a movie ID.
    # Each action can lead to multiple new states. 
    # The path cost is the number of actions taken from the source state. 
    # Each node contains a state, the previous state, the action that led to it, and the path cost.
    # The frontier contains all nodes to be checked. 
    # Nodes are added to frontier by looking at set of possible actions from the current node. 
    # Using a queue frontier for breadth-first search i.e. FIFO. 
    # No heuristic function available so can't use greedier algorithms.

    neighbours = neighbours_for_person(source)
    frontier = QueueFrontier()
    # Add initial list of neighbours to frontier
    for neighbour in neighbours:
        node = Node(neighbour[1], source, neighbour[0])
        frontier.add(node)
        if node.is_state(target):
            path = node.get_path(source, frontier)
            return path
    # Infinitely loop until match found or frontier runs out
    while True:
        if frontier.empty():
            return None
        # Extract a node to expand
        working_node = frontier.remove()
        working_node_state = working_node.get_state()
        new_neighbours = neighbours_for_person(working_node_state)
        for new_neighbour in new_neighbours:
            new_node = Node(new_neighbour[1], working_node_state, new_neighbour[0])
            if new_node.is_state(target):
                path = new_node.get_path(source, frontier)
                path.reverse()
                return path
            frontier.add(new_node)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    # dict.get() method used here as it allows a default (in this case: set())
    # to be specified in case name.lower() is not found in the dictionary
    person_ids = list(names.get(name.strip().lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        # Not sure what is the circumstance that would raise ValueError in try block above
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbours_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    Edit: Does not return self
    """
    movie_ids = people[person_id]["movies"]
    neighbours = set()
    for movie_id in movie_ids:
        for neighbour_id in movies[movie_id]["stars"]:
            if neighbour_id != person_id:
                neighbours.add((movie_id, neighbour_id))
    return neighbours


if __name__ == "__main__":
    main()
