SELECT name FROM people JOIN stars, movies ON movies.id = stars.movie_id AND people.id = stars.person_id WHERE name != "Kevin Bacon" AND  title IN (SELECT title FROM movies JOIN stars, people ON movies.id = stars.movie_id AND people.id = stars.
person_id WHERE name = "Kevin Bacon" AND birth = 1958);