DROP SCHEMA IF EXISTS A2 CASCADE;
CREATE SCHEMA A2;
SET search_path TO A2;

DROP TABLE IF EXISTS city CASCADE;
DROP TABLE IF EXISTS team CASCADE;
DROP TABLE IF EXISTS player CASCADE;
DROP TABLE IF EXISTS record CASCADE;
DROP TABLE IF EXISTS rink CASCADE;
DROP TABLE IF EXISTS tournament CASCADE;
DROP TABLE IF EXISTS event CASCADE;
DROP TABLE IF EXISTS champion CASCADE;
DROP TABLE IF EXISTS Query1 CASCADE;
DROP TABLE IF EXISTS Query2 CASCADE;
DROP TABLE IF EXISTS Query3 CASCADE;
DROP TABLE IF EXISTS Query4 CASCADE;
DROP TABLE IF EXISTS Query5 CASCADE;
DROP TABLE IF EXISTS Query6 CASCADE;
DROP TABLE IF EXISTS Query7 CASCADE;
DROP TABLE IF EXISTS Query8 CASCADE;
DROP TABLE IF EXISTS Query9 CASCADE;
DROP TABLE IF EXISTS Query10 CASCADE;


-- The city table contains some cities.
-- 'cid' is the id of the city.
-- 'cname' is the name of the city.
CREATE TABLE city(
    cid         INTEGER     PRIMARY KEY,
    cname       VARCHAR     NOT NULL
    );

-- The team table contains information about some hockey teams.
-- 'gid' is the id of the team.
-- 'gnema' is the name of the team.
-- 'cid' is the id of the city that the team belongs to.
CREATE TABLE team(
    gid         INTEGER     PRIMARY KEY,
    gname       VARCHAR     NOT NULL,
    cid         INTEGER     REFERENCES city(cid) ON DELETE RESTRICT
    );
    
-- The player table contains information about some hockey players.
-- 'pid' is the id of the player.
-- 'pname' is the name of the player.
-- 'globalrank' is the global rank of the player.
-- 'position' is the position that the player plays at.
-- 'tid' is the id of the team that the player belongs to.
CREATE TABLE player(
    pid         INTEGER     PRIMARY KEY,
    pname       VARCHAR     NOT NULL,
    globalrank  INTEGER     NOT NULL,
    position       VARCHAR     NOT NULL,
    tid         INTEGER     REFERENCES team(gid) ON DELETE RESTRICT
    );

-- The record table contains information about teams performance in each year.
-- 'rid' is the id of the team.
-- 'year' is the year.
-- 'wins' is the number of wins of the team in that year.
-- 'losses' is the the number of losses of the team in that year.
CREATE TABLE record(
    rid         INTEGER     REFERENCES team(gid) ON DELETE RESTRICT,
    year        INTEGER     NOT NULL,
    wins        INTEGER     NOT NULL,
    losses      INTEGER     NOT NULL,
    PRIMARY KEY(rid, year));

-- The tournament table contains information about a tournament.
-- 'tid' is the id of the tournament.
-- 'tname' is the name of the tournament.
-- 'cid' is the city where the tournament hold.
CREATE TABLE tournament(
    tid         INTEGER     PRIMARY KEY,
    tname       VARCHAR     NOT NULL,
    cid         INTEGER     REFERENCES city(cid) ON DELETE RESTRICT 
    );

-- The rink itable contains the information about hockey rink.
-- 'rinkid' is the id of the rink.
-- 'rinkname' is the name of the rink.
-- 'capacity' is the maximum number of audience the rink can hold.
-- 'tid' is the tournament that this rink is used for
--  Notice: only one tournament can happen on a given rink.
CREATE TABLE rink(
    rinkid     	INTEGER     PRIMARY KEY,
    rinkname   	VARCHAR     NOT NULL,
    capacity    INTEGER     NOT NULL,
    tid         INTEGER     REFERENCES tournament(tid) ON DELETE RESTRICT
    );

-- The champion table provides information about the champion of each tournament.
-- 'mid' refers to the id of the champion(team).
-- 'year' is the year when the tournament hold.
-- 'tid' is the tournament id.
CREATE TABLE champion(
    mid     INTEGER     REFERENCES team(gid) ON DELETE RESTRICT,
    year    INTEGER     NOT NULL, 
    tid     INTEGER     REFERENCES tournament(tid) ON DELETE RESTRICT,
    PRIMARY KEY(mid, year));

-- The event table provides information about certain hockey games.
-- 'vid' refers to the id of the event.
-- 'year' is the year when the event hold.
-- 'rinkid' is the id of the court where the event hold.
-- 'winid' is the id of the team who win the game.
-- 'lossid' is the id of the team who loss the game.
-- 'duration' is duration of the event, in minutes.
CREATE TABLE event(
    vid        INTEGER     PRIMARY KEY,
    year       INTEGER     NOT NULL,
    rinkid    INTEGER     REFERENCES rink(rinkid) ON DELETE RESTRICT,
    winid      INTEGER     REFERENCES team(gid) ON DELETE RESTRICT,
    lossid     INTEGER     REFERENCES team(gid) ON DELETE RESTRICT,
    duration   INTEGER     NOT NULL
    );


-- The following tables will be used to store the results of your queries. 
-- Each of them should be populated by your last SQL statement that looks like:
-- "INSERT INTO QueryX (SELECT ...<complete your SQL query here> ... )"

CREATE TABLE query1(
    pname    VARCHAR,
    cname    VARCHAR,
    tname    VARCHAR    
);

CREATE TABLE query2(
    tname   VARCHAR
);

CREATE TABLE query3(
    pid    INTEGER,
    pname  VARCHAR   
);

CREATE TABLE query4(
    tid     INTEGER,
    tname   VARCHAR,
    city    VARCHAR   
);

CREATE TABLE query5(
    tid      INTEGER,
    tname    VARCHAR,
    avgwins  REAL
);

CREATE TABLE query6(
    tid     INTEGER,
    tname   VARCHAR,
    city    VARCHAR    
);

CREATE TABLE query7(
    pname    VARCHAR,
    year     INTEGER,
    tname    VARCHAR
);

CREATE TABLE query8(
    p1name  VARCHAR,
    p2name  VARCHAR,
    num     INTEGER    
);

CREATE TABLE query9(
    cname       VARCHAR,
    tournaments INTEGER
);

CREATE TABLE query10(
    tname       VARCHAR
);
