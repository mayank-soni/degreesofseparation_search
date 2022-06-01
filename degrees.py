import csv
import sys

from util import Node, QueueFrontier

# Data is organised in 3 CSVs. 
# - people.csv stores the actors' details and corresponding person_ids. 
# - movies.csv stores the movies' details and the corresponding movie_ids. 
# - stars.csv links the 2 files above. It stores movie_ids and the corresponding person_ids that acted in each movie. 

# Initialise 3 dictionaries to store data. 
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
    # NOTE: Additionally implemented error checking
    # Load people. 
    try:
        f = open(f"{directory}/people.csv", encoding="utf-8")
    except FileNotFoundError as error:
        sys.exit(error)
    with f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["id"]] = {
                    "name": row["name"],
                    "birth": row["birth"],
                    "movies": set()
                }
            except KeyError as error:
                sys.exit(f"Error: people.csv does not contain {error}")
            if row["name"].lower() not in names:
                # Note to self: This is generating a set, not a dictionary, since the curly braces only enclose a single element
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    try:
        f = open(f"{directory}/movies.csv", encoding="utf-8")
    except FileNotFoundError as error:
        sys.exit(error)
    with f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                movies[row["id"]] = {
                    "title": row["title"],
                    "year": row["year"],
                    "stars": set()
                }
            except KeyError as error:
                sys.exit(f"Error: movies.csv does not contain {error}")
                
    # Load stars
    try:
        f = open(f"{directory}/stars.csv", encoding="utf-8")
    except FileNotFoundError as error:
        sys.exit(error)
    with f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError as error:
                pass


def main():
    # Checks if user has provided own data as command-line argument, and if so uses it
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "data"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # Get user input for which actors to find shortest path between
    while True:
        source = person_id_for_name(input("First actor's name: "))
        if source is None:
            print("Actor not found. Please try again.")
        else:
            break
    while True:
        target = person_id_for_name(input("Second actor's name: "))
        if target is None:
            print("Actor not found. Please try again.")
        else:
            break
    path = shortest_path(source, target)
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        if degrees == 1:
            print(f"{degrees} degree of separation.")
        else:
            print(f"{degrees} degrees of separation.")
        # Print out the sequence of connections
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
    # Uses breadth-first search (BFS), which is guaranteed to provide the shortest path even though it may take longer. 
    # Uses Node and QueueFrontier classes implemented in util.py.
    # A node contains:
    #   State: Person ID of actor.
    #   Path: Path taken to reach this node
    #       - Paths consist of a list of (movie_id, person_id)s
    #       - E.g. Path could be [(movie1, person1), (movie2, target)] 
    #           This means the source is linked to person1 via movie1. And person1 is linked to the target via movie2
    # BFS uses the concept of a frontier which is a list of nodes. The frontier starts empty. 
    # First, the nodes directly connected to the source are added. 
    # - While adding, each is checked to see if its state is the target person ID. If so, the search ends. 
    # Next, each node in the frontier is checked in turn. 
    # - This means that its own connections are added to the frontier.
    # - While adding, each is checked to see if its state is the target person ID. If so, the search ends.
    # - No duplicates are allowed i.e. no person_id that has been added before can be added again, even if with a different parent/action 
    # Using a queue frontier for breadth-first search i.e. FIFO when selecting nodes to check in the frontier. 
    # - This guarantees that the fastest path will be found, but might be slow. 
    # Can't think of a suitable heuristic function to be able to use faster algorithms e.g. A* search

    #Initialise frontier with source node
    frontier = QueueFrontier()
    frontier.add([Node(source, [])])

    # Loop until match found or frontier runs out
    while True:
        if frontier.empty():
            return None
        # Extract a node to expand
        working_node = frontier.remove()
        new_neighbours = neighbours(working_node)
        for new_neighbour in new_neighbours:
            # If target is reached, return its path
            if new_neighbour.get_state() == target:
                return new_neighbour.get_path()
        # Otherwise, add it to the frontier
        frontier.add(new_neighbours)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    # dict.get() method used here as it allows a default (in this case: set()) to be specified
    # in case name.lower() is not found in the dictionary
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


def neighbours(node):
    """
    Returns (movie_id, person_id) pairs for people who starred with a given person.
    Edit: Does not return original person_id
    Edit2: Generates and returns node directly to make shortest_path() more readable with fewer indices. 
    """
    # Initialise empty set of neighbours to be returned
    list_of_neighbours = set()

    # Get list of movies actor is involved in
    person_id = node.get_state()
    movie_ids = people[person_id]["movies"]

    # For each movie
    for movie_id in movie_ids:
        # For each actor in the movie
        for neighbour_id in movies[movie_id]["stars"]:
            # Other than the original actor
            if neighbour_id != person_id:
                # Add a node for each actor into list_of_neighbours
                neighbour = Node(neighbour_id, node.get_path() + [(movie_id, neighbour_id)])
                list_of_neighbours.add(neighbour)
    return list_of_neighbours


if __name__ == "__main__":
    main()