# degreesofseparation_search
Implements a breadth-first search algorithm to find the degrees of separation between two actors in IMDB's database. 

Actors are linked to other actors if they were in the same movie. The degrees of separation refer to the minimum number of links required to reach one actor from another. 

To use: python degrees.py data_subfolder
- Upon prompt, key in the names of the two actors to search. 

Done as part of Harvard's CS50AI course (https://cs50.harvard.edu/ai/2020/projects/0/degrees/). Some functions were given e.g. to read in data (load_data()) & find each actor's links (list_of_neighbours()), as well as part of the implementation of the Node and Frontier classes. 

Data needs to be stored in 3 CSV files (as per how IMDB represents its data)
- movies.csv should contain at least 2 fields: "id" & "title" representing a unique movie ID and the movie's title respectively
- people.csv should contain at least 2 fields: "id" & "name" representing a unique person ID and the actor's name respectively. It should also contain the actor's birth year "birth" to de-conflict actors with the same name. 
- stars.csv should contain at least 2 fields: "person_id" and "movie_id" which represent which movies a person has acted in (many-many matching)

