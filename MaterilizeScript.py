import sqlite3
import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""

r = redis.Redis(host=redis_host, port=redis_port)

# START_CONNECTION - takes the name of a database to connect to
def start_connection(name=""):
    if not name:
        return
    # Ensures that we connect to the database.
    try:
        conn = sqlite3.connect(
            f"./db/{name}.db", detect_types=sqlite3.PARSE_DECLTYPES
        )  # create connection to db on error default to except clause.
        print(f"Successfully connected to {name} database.")
        return conn

    except sqlite3.Error as error:
        print(f"Error occurred while connecting to {name} database.", error)

# FILTER VALUES - returns guid and number of wins or streaks for top acheivers!
def filter_values(list_of_vals):
    # sort the array based on second property of each element tuple (wins)
    list_of_vals.sort(reverse=True, key=lambda x: x[1])
    return list_of_vals[0:30]

users_db = start_connection("users")
shard_connections = [
    (start_connection("stats_1"), "games_1"),
    (start_connection("stats_2"), "games_2"),
    (start_connection("stats_3"), "games_3"),
]

shard_scan_results = []
stats_win = {}
try:
    users_cur = users_db.cursor()
    # for every shard get their top ten then use filter func to sort and filter
    for (connection, _) in shard_connections:
        cur = connection.cursor()
        cur.execute("""SELECT * FROM wins ORDER BY "COUNT(won)" DESC LIMIT 10""")
        for result in cur.fetchall():
            shard_scan_results.append(result)
    filtered_list = filter_values(shard_scan_results)  # utilizing helper function
    # query each guid for the username that it is linked to
    for (guid, wins) in filtered_list:
        users_cur.execute(
            f"SELECT username FROM users WHERE guid=:id", {"id": guid}
        )
        name = users_cur.fetchone()[0]
        stats_win[name] = wins
except Exception as e:
    print(f"An error has occured! => {e}")

print(stats_win)
r.zadd("topwins", stats_win)

shard_scan_results = []
stats = {}
try:
    users_cur = users_db.cursor()
    # for every shard get their top ten then use filter func to sort and filter
    for (connection, _) in shard_connections:
        cur = connection.cursor()
        cur.execute("""SELECT * FROM losses ORDER BY "COUNT(won)" DESC LIMIT 10""") 
        for result in cur.fetchall():
            shard_scan_results.append(result)
    filtered_list = filter_values(shard_scan_results)  # utilizing helper function
    # query each guid for the username that it is linked to
    for (guid, wins) in filtered_list:
        users_cur.execute(
            f"SELECT username FROM users WHERE guid=:id", {"id": guid}
        )
        name = users_cur.fetchone()[0]
        stats[name] = wins
except Exception as e:
    print(f"An error has occured! => {e}")

print(stats)
r.zadd("toploses", stats)

shard_scan_results = []
stats_streaks = {}
try:
    users_cur = users_db.cursor()
    # for every shard get their top ten then use filter func to sort and filter
    for (connection, _) in shard_connections:
        cur = connection.cursor()
        cur.execute(
            """SELECT guid, streak FROM streaks ORDER BY streak DESC LIMIT 10"""
        )
        for result in cur.fetchall():
            shard_scan_results.append(result)
    filtered_list = filter_values(shard_scan_results)  # utilizing helper function
    # query each guid for the username that it is linked to
    for (guid, streak) in filtered_list:
        users_cur.execute(
            f"SELECT username FROM users WHERE guid=:id", {"id": guid}
        )
        name = users_cur.fetchone()[0]
        stats_streaks[name] = streak
except Exception as e:
    print(f"An error has occured! => {e}")

print(stats_streaks)
r.zadd("topstreaks", stats_streaks)