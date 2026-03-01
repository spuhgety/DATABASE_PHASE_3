# cli.py
from db import get_connection
import sys
#--------------------------------------------------------------------------
def menu():
    print("\n==== Valorant Tracker CLI ====")
    print("1. List Teams")
    print("2. List Players")
    print("3. View Player Details")
    print("4. List Matches")
    print("5. View Match Details")
    print("6. Add a Note to a VOD")
    print("7. Add a player") 
    print("0. Exit")
    return input("Choose an option: ")
#--------------------------------------------------------------------------
def list_teams(cnx):
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM TEAM;")
    rows = cursor.fetchall()

    print("\n--- Teams ---")
    for r in rows:
        print(f"[{r['team_id']}] {r['name']} - {r['school']} ({r['region']})")
#--------------------------------------------------------------------------
def list_players(cnx):
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("""
        SELECT player_id, first_name, last_name, role_, rank_, name AS team
        FROM PLAYER
        LEFT JOIN TEAM USING(team_id);
    """)
    rows = cursor.fetchall()

    print("\n--- Players ---")
    for r in rows:
        print(f"[{r['player_id']}] {r['first_name']} {r['last_name']} - {r['role_']} ({r['rank_']}), Team: {r['team']}")
#--------------------------------------------------------------------------
def view_player(cnx):
    pid = input("Enter player_id: ")
    cursor = cnx.cursor(dictionary=True)

    cursor.execute("SELECT * FROM PLAYER WHERE player_id = %s;", (pid,))
    player = cursor.fetchone()
    if not player:
        print("Player not found.")
        return

    print(f"\n{player['first_name']} {player['last_name']}")
    print(f"Role: {player['role_']}  Rank: {player['rank_']}")

    cursor.execute("SELECT agent_name FROM AGENT_PLAYED WHERE player_id = %s;", (pid,))
    agents = cursor.fetchall()

    print("Agents:", ", ".join(a['agent_name'] for a in agents))
#--------------------------------------------------------------------------
def list_matches(cnx):
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("""
        SELECT match_id, name AS team, date_played, map_name, opponent, result, is_finalized
        FROM MATCH_T
        JOIN TEAM USING(team_id)
        ORDER BY match_id;
    """)
    rows = cursor.fetchall()

    print("\n--- Matches ---")
    for r in rows:
        status = "Finalized" if r["is_finalized"] else "Not Finalized"
        print(f"[{r['match_id']}] {r['team']} vs {r['opponent']} on {r['map_name']} ({r['result']}) - {status}")
#--------------------------------------------------------------------------
def view_match(cnx):
    mid = input("Enter match_id: ")
    cursor = cnx.cursor(dictionary=True)

    # match info
    cursor.execute("""
        SELECT *
        FROM MATCH_T 
        JOIN TEAM USING(team_id)
        WHERE match_id = %s;
    """, (mid,))
    match = cursor.fetchone()

    if not match:
        print("Match not found.")
        return

    print(f"\nMatch {mid}: {match['name']} vs {match['opponent']}")
    print(f"Map: {match['map_name']}  Date: {match['date_played']}")
    print("Result:", match["result"])
    print("Finalized:" , match["is_finalized"])

    # performance
    print("\n--- Performance Rows ---")
    cursor.execute("""
        SELECT first_name, last_name, kills, deaths, assists, acs, agent_played
        FROM PERFORMANCE
        JOIN PLAYER USING(player_id)
        WHERE match_id = %s;
    """, (mid,))
    perf = cursor.fetchall()

    for p in perf:
        print(f"{p['first_name']} {p['last_name']} - {p['kills']}/{p['deaths']}/{p['assists']} | Agent: {p['agent_played']} | ACS: {p['acs']}")

    # VOD + Notes
    cursor.execute("SELECT * FROM VOD WHERE match_id = %s;", (mid,))
    vod = cursor.fetchone()

    if vod:
        print("\nVOD:", vod["file_url"])
        cursor.execute("SELECT * FROM NOTE WHERE vod_id = %s;", (vod["vod_id"],))
        notes = cursor.fetchall()

        print("\n--- Notes ---")
        for n in notes:
            print(f"[{n['vod_timestamp']}] {n['author']}: {n['content']}")
    else:
        print("\nNo VOD for this match.")
#--------------------------------------------------------------------------
def add_note(cnx):
    vod_id = input("Enter vod_id: ")
    ts = input("Timestamp (HH:MM:SS): ")
    author = input("Author: ")
    content = input("Content: ")

    cursor = cnx.cursor()
    cursor.execute("""
        INSERT INTO NOTE (vod_id, vod_timestamp, author, content)
        VALUES (%s, %s, %s, %s);
    """, (vod_id, ts, author, content))
    cnx.commit()
    print("Note added.")
#--------------------------------------------------------------------------

def add_player(cnx):
    print("\n--- Add New Player ---")

    # Collect user input
    first = input("First name: ")
    last = input("Last name: ")
    role_ = input("Role (Duelist/Controller/Initiator/Sentinel/Flex): ")
    rank_ = input("Rank (e.g., Ascendant, Diamond, etc.): ")
    team_id = input("Team ID(enter nothing if not on a team): ")
    #include logic for if a player is not on a team
    if team_id.strip() == "":
        team_id = None
    # Insert the player into the database
    cursor = cnx.cursor()

    try:
        cursor.execute("""
            INSERT INTO PLAYER (team_id, first_name, last_name, role_, rank_)
            VALUES (%s, %s, %s, %s, %s);
        """, (team_id, first, last, role_, rank_))

        cnx.commit()
        print(f"Player {first} {last} added successfully!")

    except Exception as e:
        print("Error adding player:", e)


#--------------------------------------------------------------------------
def main():
    cnx = get_connection()

    while True:
        choice = menu()
        if choice == "1":
            list_teams(cnx)
        elif choice == "2":
            list_players(cnx)
        elif choice == "3":
            view_player(cnx)
        elif choice == "4":
            list_matches(cnx)
        elif choice == "5":
            view_match(cnx)
        elif choice == "6":
            add_note(cnx)
        elif choice == "7":
            add_player(cnx)
        elif choice == "0":
            break
        else:
            print("Invalid option.")

    cnx.close()
#--------------------------------------------------------------------------
if __name__ == "__main__":
    main()
