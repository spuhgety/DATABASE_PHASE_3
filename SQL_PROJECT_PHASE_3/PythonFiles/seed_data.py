from db import get_connection

def seed():
    cnx = get_connection()
    cursor = cnx.cursor()

    # Clear tables in correct FK order
    cursor.execute("DELETE FROM NOTE;")
    cursor.execute("DELETE FROM VOD;")
    cursor.execute("DELETE FROM PERFORMANCE;")
    cursor.execute("DELETE FROM MATCH_T;")
    cursor.execute("DELETE FROM AGENT_PLAYED;")
    cursor.execute("DELETE FROM PLAYER;")
    cursor.execute("DELETE FROM TEAM;")

    # Insert Teams
    cursor.execute("""
        INSERT INTO TEAM (name, school, region)
        VALUES
        ('Mizzou Valorant Black', 'University of Missouri', 'Midwest'),
        ('Mizzou Valorant Gold', 'University of Missouri', 'Midwest'),
        ('KU Valorant Blue', 'University of Kansas', 'Midwest');
    """)

    # Insert Players
    cursor.execute("""
        INSERT INTO PLAYER (team_id, first_name, last_name, role_, rank_)
        VALUES
        (1, 'Luke', 'Johnson', 'Duelist', 'Ascendant'),
        (1, 'Ethan', 'Smith', 'Controller', 'Diamond'),
        (1, 'Dylan', 'Reed', 'Initiator', 'Immortal'),
        (1, 'Aidan', 'Cole', 'Sentinel', 'Diamond'),
        (1, 'Noah', 'Wallace', 'Flex', 'Ascendant'),

        (2, 'Chase', 'Greene', 'Duelist', 'Diamond'),
        (2, 'Eli', 'Turner', 'Controller', 'Platinum'),

        (3, 'Jared', 'Hill', 'Initiator', 'Immortal'),
        (3, 'Ryan', 'Price', 'Sentinel', 'Diamond');
    """)

    # Insert simple agent played list
    cursor.execute("""
        INSERT INTO AGENT_PLAYED (player_id, agent_name)
        VALUES
        (1, 'Jett'),
        (1, 'Reyna'),
        (2, 'Omen'),
        (3, 'Sova'),
        (3, 'Fade'),
        (4, 'Killjoy'),
        (5, 'Breach');
    """)

    # Insert a match
    cursor.execute("""
        INSERT INTO MATCH_T (team_id, date_played, map_name, opponent, result, duration_min)
        VALUES (1, '2025-11-01', 'Ascent', 'KU Valorant Blue', 'Win', 42, FALSE);
    """)

    # Insert performance rows (5 players minimum)
    cursor.execute("""
        INSERT INTO PERFORMANCE (player_id, match_id, kills, deaths, assists, headshot_pct, agent_played, acs)
        VALUES
        (1, 1, 22, 15, 5, 18.5, 'Jett', 245),
        (2, 1, 10, 19, 11, 12.4, 'Omen', 175),
        (3, 1, 17, 14, 12, 30.1, 'Sova', 210),
        (4, 1, 15, 13, 3, 25.0, 'Killjoy', 190),
        (5, 1, 8, 16, 8, 9.0, 'Breach', 150);
    """)

    # Insert VOD
    cursor.execute("""
        INSERT INTO VOD (match_id, file_url, upload_date)
        VALUES (1, 'https://youtube.com/example', NOW());
    """)

    # Insert Notes
    cursor.execute("""
        INSERT INTO NOTE (vod_id, vod_timestamp, author, content)
        VALUES
        (1, '00:12:05', 'Coach Mike', 'Great early round coordination.'),
        (1, '00:24:10', 'Luke', 'Need better post-plant positioning.');
    """)

    cnx.commit()
    cursor.close()
    cnx.close()

    print("Seeding complete.")

if __name__ == "__main__":
    seed()
