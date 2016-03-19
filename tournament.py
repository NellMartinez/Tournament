#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

# Completed 1
def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    ammount = c.execute("DELETE FROM matches WHERE id_matches <> 0;")
    conn.commit()
    conn.close()
    
# Completed 2
def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    ammount = c.execute("DELETE FROM players WHERE id_players <> 0;")
    conn.commit()
    conn.close()
    return ammount
    
# Completed 3
def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(*) FROM players;")
    rows = c.fetchone()
    count_players = rows[0]
    conn.commit()
    conn.close()
    return count_players

# Completed 3
def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    query = ('INSERT INTO players (name) VALUES (%s);')
    name = (str(name),)
    c.execute(query, name)
    conn.commit()
    conn.close()
    return countPlayers()

# Completed 4
def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM billboard;")
    rows = c.fetchall()
    conn.close()
    return rows

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches (winners, losers) VALUES (%s,%s)",
              (winner, loser,))
    conn.commit()
    conn.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    tuple_pairs = []
    
    for id1, id2 in zip(standings[0::2], standings[1::2]):
        tuple_pairs.append((id1[0], id1[1], id2[0], id2[1]))
    return tuple_pairs

