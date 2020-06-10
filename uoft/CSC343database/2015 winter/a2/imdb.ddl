-- -*- mode:sql -*-

DROP SCHEMA IF EXISTS imdb;
CREATE SCHEMA imdb;
SET search_path TO imdb;


CREATE TABLE movies (
  movie_id integer PRIMARY KEY,
  title varchar NOT NULL,
  year integer NOT NULL,
  rating float NOT NULL,
  UNIQUE (title,year)
) ;


-- People associated with movies

CREATE TABLE people (
  person_id integer PRIMARY KEY,
  name varchar NOT NULL UNIQUE
) ;

CREATE TABLE cinematographers (
  movie_id integer NOT NULL REFERENCES movies,
  person_id integer NOT NULL REFERENCES people,
  PRIMARY KEY (movie_id,person_id)
) ;

CREATE TABLE composers (
  movie_id integer NOT NULL REFERENCES movies,
  person_id integer NOT NULL REFERENCES people,
  PRIMARY KEY (movie_id,person_id)
) ;

CREATE TABLE directors (
  movie_id integer NOT NULL REFERENCES movies,
  person_id integer NOT NULL REFERENCES people,
  PRIMARY KEY (movie_id,person_id)
) ;

CREATE TABLE roles (
  person_id integer NOT NULL REFERENCES people,
  movie_id integer NOT NULL REFERENCES movies,
  role varchar NOT NULL,
  PRIMARY KEY (person_id,movie_id,role)
) ;

CREATE TABLE writers (
  movie_id integer NOT NULL REFERENCES movies,
  person_id integer NOT NULL REFERENCES people,
  PRIMARY KEY (movie_id,person_id)
) ;


-- Movie categorization

CREATE TABLE genres (
  genre_id integer PRIMARY KEY,
  label varchar NOT NULL UNIQUE
) ;

CREATE TABLE movie_genres (
  movie_id integer NOT NULL REFERENCES movies,
  genre_id integer NOT NULL REFERENCES genres,
  PRIMARY KEY (movie_id,genre_id)
) ;

CREATE TABLE keywords (
  keyword_id integer PRIMARY KEY,
  keyword varchar NOT NULL UNIQUE
) ;

CREATE TABLE movie_keywords (
  movie_id integer NOT NULL REFERENCES movies,
  keyword_id integer NOT NULL REFERENCES keywords,
  PRIMARY KEY (movie_id,keyword_id)
) ;


-- Other movie information.
-- NOT USED FOR ASSIGNMENT 2!!
CREATE TABLE aka_titles (
  movie_id integer NOT NULL REFERENCES movies,
  title varchar NOT NULL,
  note varchar NOT NULL,
  PRIMARY KEY (movie_id,title)
) ;

CREATE TABLE aka_names (
  person_id integer NOT NULL REFERENCES people,
  name varchar NOT NULL,
  PRIMARY KEY (person_id,name)
) ;


CREATE TABLE distributors (
  distributor_id integer PRIMARY KEY,
  name varchar NOT NULL UNIQUE
) ;

CREATE TABLE media_types (
  media_type_id integer PRIMARY KEY,
  label varchar NOT NULL UNIQUE
) ;

CREATE TABLE movie_distributors (
  movie_id integer NOT NULL REFERENCES movies,
  distributor_id integer NOT NULL REFERENCES distributors,
  media_type_id integer NOT NULL REFERENCES media_types,
  PRIMARY KEY (movie_id,distributor_id,media_type_id)
) ;

CREATE TABLE countries (
  country_id integer PRIMARY KEY,
  name varchar NOT NULL UNIQUE
) ;

CREATE TABLE movie_countries (
  movie_id integer NOT NULL REFERENCES movies,
  country_id integer NOT NULL REFERENCES countries,
  PRIMARY KEY (movie_id,country_id)
) ;

CREATE TABLE locations (
  location_id integer PRIMARY KEY,
  name varchar NOT NULL,
  parent_location_id integer REFERENCES locations,
  UNIQUE (name,parent_location_id)
) ;

CREATE TABLE movie_locations (
  movie_id integer NOT NULL,
  location_id integer NOT NULL,
  PRIMARY KEY (movie_id,location_id)
) ;
