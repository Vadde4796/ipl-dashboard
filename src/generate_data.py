"""Generates realistic IPL matches and deliveries datasets (2008-2024)."""

import pandas as pd
import numpy as np
import os
import random

random.seed(42)
np.random.seed(42)

TEAMS = {
    2008: ["Mumbai Indians", "Chennai Super Kings", "Kolkata Knight Riders",
           "Royal Challengers Bangalore", "Deccan Chargers", "Kings XI Punjab",
           "Rajasthan Royals", "Delhi Daredevils"],
    2013: ["Mumbai Indians", "Chennai Super Kings", "Kolkata Knight Riders",
           "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Kings XI Punjab",
           "Rajasthan Royals", "Delhi Daredevils", "Pune Warriors India"],
    2020: ["Mumbai Indians", "Chennai Super Kings", "Kolkata Knight Riders",
           "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Punjab Kings",
           "Rajasthan Royals", "Delhi Capitals"],
    2022: ["Mumbai Indians", "Chennai Super Kings", "Kolkata Knight Riders",
           "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Punjab Kings",
           "Rajasthan Royals", "Delhi Capitals", "Gujarat Titans", "Lucknow Super Giants"],
}

SEASON_WINNERS = {
    2008: "Rajasthan Royals", 2009: "Deccan Chargers", 2010: "Chennai Super Kings",
    2011: "Chennai Super Kings", 2012: "Kolkata Knight Riders", 2013: "Mumbai Indians",
    2014: "Kolkata Knight Riders", 2015: "Mumbai Indians", 2016: "Sunrisers Hyderabad",
    2017: "Mumbai Indians", 2018: "Chennai Super Kings", 2019: "Mumbai Indians",
    2020: "Mumbai Indians", 2021: "Chennai Super Kings", 2022: "Gujarat Titans",
    2023: "Chennai Super Kings", 2024: "Kolkata Knight Riders",
}

VENUES = [
    "Wankhede Stadium, Mumbai", "M. A. Chidambaram Stadium, Chennai",
    "Eden Gardens, Kolkata", "M. Chinnaswamy Stadium, Bangalore",
    "Feroz Shah Kotla, Delhi", "Punjab Cricket Association Stadium, Mohali",
    "Rajiv Gandhi International Stadium, Hyderabad", "Sawai Mansingh Stadium, Jaipur",
    "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam",
    "Narendra Modi Stadium, Ahmedabad",
]

BATSMEN = [
    "V Kohli", "RG Sharma", "DA Warner", "CH Gayle", "SK Raina", "MS Dhoni",
    "AB de Villiers", "KL Rahul", "S Dhawan", "AM Rahane", "SR Watson",
    "G Gambhir", "BB McCullum", "F du Plessis", "JP Duminy", "SV Samson",
    "RA Tripathi", "SS Iyer", "HH Pandya", "AT Rayudu", "PA Patel",
    "Q de Kock", "KS Williamson", "DR Smith", "M Vijay", "RV Uthappa",
]

BOWLERS = [
    "SL Malinga", "JJ Bumrah", "DW Steyn", "A Kumble", "PP Chawla",
    "Harbhajan Singh", "R Ashwin", "DL Chahar", "YS Chahal", "Rashid Khan",
    "B Kumar", "MM Sharma", "I Sharma", "MJ McClenaghan", "LH Ferguson",
    "SP Narine", "DJ Bravo", "A Mishra", "P Kumar", "RP Singh",
]

PLAYER_META = {
    "V Kohli":        ("Batsman",        "Indian",      "Royal Challengers Bangalore"),
    "RG Sharma":      ("Batsman",        "Indian",      "Mumbai Indians"),
    "DA Warner":      ("Batsman",        "Australian",  "Sunrisers Hyderabad"),
    "CH Gayle":       ("Batsman",        "West Indian", "Royal Challengers Bangalore"),
    "SK Raina":       ("Batsman",        "Indian",      "Chennai Super Kings"),
    "MS Dhoni":       ("Wicket-Keeper",  "Indian",      "Chennai Super Kings"),
    "AB de Villiers": ("Batsman",        "South African","Royal Challengers Bangalore"),
    "KL Rahul":       ("Batsman",        "Indian",      "Punjab Kings"),
    "S Dhawan":       ("Batsman",        "Indian",      "Sunrisers Hyderabad"),
    "AM Rahane":      ("Batsman",        "Indian",      "Rajasthan Royals"),
    "SR Watson":      ("All-Rounder",    "Australian",  "Chennai Super Kings"),
    "G Gambhir":      ("Batsman",        "Indian",      "Kolkata Knight Riders"),
    "BB McCullum":    ("Wicket-Keeper",  "New Zealander","Kolkata Knight Riders"),
    "F du Plessis":   ("Batsman",        "South African","Chennai Super Kings"),
    "JP Duminy":      ("All-Rounder",    "South African","Mumbai Indians"),
    "SV Samson":      ("Wicket-Keeper",  "Indian",      "Rajasthan Royals"),
    "RA Tripathi":    ("Batsman",        "Indian",      "Sunrisers Hyderabad"),
    "SS Iyer":        ("Batsman",        "Indian",      "Delhi Capitals"),
    "HH Pandya":      ("All-Rounder",    "Indian",      "Mumbai Indians"),
    "AT Rayudu":      ("Batsman",        "Indian",      "Chennai Super Kings"),
    "PA Patel":       ("Wicket-Keeper",  "Indian",      "Rajasthan Royals"),
    "Q de Kock":      ("Wicket-Keeper",  "South African","Mumbai Indians"),
    "KS Williamson":  ("Batsman",        "New Zealander","Sunrisers Hyderabad"),
    "DR Smith":       ("Batsman",        "West Indian", "Rajasthan Royals"),
    "M Vijay":        ("Batsman",        "Indian",      "Chennai Super Kings"),
    "RV Uthappa":     ("Batsman",        "Indian",      "Kolkata Knight Riders"),
    "SL Malinga":     ("Bowler",         "Sri Lankan",  "Mumbai Indians"),
    "JJ Bumrah":      ("Bowler",         "Indian",      "Mumbai Indians"),
    "DW Steyn":       ("Bowler",         "South African","Sunrisers Hyderabad"),
    "A Kumble":       ("Bowler",         "Indian",      "Royal Challengers Bangalore"),
    "PP Chawla":      ("Bowler",         "Indian",      "Chennai Super Kings"),
    "Harbhajan Singh":("Bowler",         "Indian",      "Mumbai Indians"),
    "R Ashwin":       ("Bowler",         "Indian",      "Chennai Super Kings"),
    "DL Chahar":      ("Bowler",         "Indian",      "Chennai Super Kings"),
    "YS Chahal":      ("Bowler",         "Indian",      "Royal Challengers Bangalore"),
    "Rashid Khan":    ("Bowler",         "Afghan",      "Sunrisers Hyderabad"),
    "B Kumar":        ("Bowler",         "Indian",      "Sunrisers Hyderabad"),
    "MM Sharma":      ("Bowler",         "Indian",      "Sunrisers Hyderabad"),
    "I Sharma":       ("Bowler",         "Indian",      "Sunrisers Hyderabad"),
    "MJ McClenaghan": ("Bowler",         "New Zealander","Mumbai Indians"),
    "LH Ferguson":    ("Bowler",         "New Zealander","Kolkata Knight Riders"),
    "SP Narine":      ("All-Rounder",    "West Indian", "Kolkata Knight Riders"),
    "DJ Bravo":       ("All-Rounder",    "West Indian", "Chennai Super Kings"),
    "A Mishra":       ("Bowler",         "Indian",      "Delhi Capitals"),
    "P Kumar":        ("Bowler",         "Indian",      "Sunrisers Hyderabad"),
    "RP Singh":       ("Bowler",         "Indian",      "Deccan Chargers"),
}

SEASON_RUNNERS_UP = {
    2008: "Chennai Super Kings",    2009: "Royal Challengers Bangalore",
    2010: "Mumbai Indians",         2011: "Royal Challengers Bangalore",
    2012: "Chennai Super Kings",    2013: "Chennai Super Kings",
    2014: "Kings XI Punjab",        2015: "Chennai Super Kings",
    2016: "Royal Challengers Bangalore", 2017: "Rising Pune Supergiant",
    2018: "Sunrisers Hyderabad",    2019: "Chennai Super Kings",
    2020: "Delhi Capitals",         2021: "Kolkata Knight Riders",
    2022: "Rajasthan Royals",       2023: "Gujarat Titans",
    2024: "Sunrisers Hyderabad",
}

ORANGE_CAP = {
    2008: ("SE Marsh", 616),   2009: ("ML Hayden", 572),  2010: ("SR Tendulkar", 618),
    2011: ("CH Gayle", 608),   2012: ("CH Gayle", 733),   2013: ("MEK Hussey", 733),
    2014: ("RG Sharma", 679),  2015: ("DA Warner", 562),  2016: ("V Kohli", 973),
    2017: ("DA Warner", 641),  2018: ("KS Williamson", 735), 2019: ("DA Warner", 692),
    2020: ("KL Rahul", 670),   2021: ("RD Gaikwad", 635), 2022: ("JC Buttler", 863),
    2023: ("S Gill", 890),     2024: ("V Kohli", 741),
}

PURPLE_CAP = {
    2008: ("S Sreesanth", 23),  2009: ("RP Singh", 23),    2010: ("PP Chawla", 21),
    2011: ("SL Malinga", 28),   2012: ("M Morkel", 25),    2013: ("DJ Bravo", 32),
    2014: ("MM Sharma", 23),    2015: ("DJ Bravo", 26),    2016: ("B Kumar", 23),
    2017: ("B Kumar", 26),      2018: ("A Nehra", 26),     2019: ("I Sharma", 26),
    2020: ("K Rabada", 30),     2021: ("HV Patel", 32),    2022: ("YS Chahal", 27),
    2023: ("MJ Shami", 28),     2024: ("HV Patel", 24),
}

CITIES = [
    "Mumbai", "Chennai", "Kolkata", "Bangalore", "Delhi", "Mohali",
    "Hyderabad", "Jaipur", "Visakhapatnam", "Ahmedabad", "Indore", "Pune",
]


def get_teams_for_season(year):
    cutoff = max(k for k in TEAMS if k <= year)
    return TEAMS[cutoff]


def generate_matches():
    matches = []
    match_id = 1
    for season in range(2008, 2025):
        teams = get_teams_for_season(season)
        num_matches = 60 if len(teams) == 10 else 56
        for _ in range(num_matches):
            t1, t2 = random.sample(teams, 2)
            toss_winner = random.choice([t1, t2])
            toss_decision = random.choice(["bat", "field"])
            winner = random.choice([t1, t2])
            if winner == t1:
                loser = t2
            else:
                loser = t1
            result_type = random.choices(["runs", "wickets"], weights=[0.45, 0.55])[0]
            win_by_runs = random.randint(1, 80) if result_type == "runs" else 0
            win_by_wickets = random.randint(1, 9) if result_type == "wickets" else 0
            venue = random.choice(VENUES)
            city = random.choice(CITIES)
            player_of_match = random.choice(BATSMEN + BOWLERS)
            matches.append({
                "id": match_id,
                "season": season,
                "city": city,
                "date": f"{season}-0{random.randint(4,5)}-{random.randint(10,30):02d}",
                "team1": t1,
                "team2": t2,
                "toss_winner": toss_winner,
                "toss_decision": toss_decision,
                "result": result_type,
                "dl_applied": random.choices([0, 1], weights=[0.95, 0.05])[0],
                "winner": winner,
                "win_by_runs": win_by_runs,
                "win_by_wickets": win_by_wickets,
                "player_of_match": player_of_match,
                "venue": venue,
                "umpire1": "Umpire A",
                "umpire2": "Umpire B",
            })
            match_id += 1
    return pd.DataFrame(matches)


def generate_deliveries(matches_df):
    records = []
    for _, match in matches_df.iterrows():
        mid = match["id"]
        teams = [match["team1"], match["team2"]]
        for inning in range(1, 3):
            batting = teams[inning - 1]
            bowling = teams[2 - inning]
            batsmen_in = random.sample(BATSMEN, 6)
            bowlers_in = random.sample(BOWLERS, 5)
            current_batsman = batsmen_in[0]
            non_striker = batsmen_in[1]
            batsman_idx = 2
            for over in range(1, 21):
                bowler = bowlers_in[(over - 1) % len(bowlers_in)]
                for ball in range(1, 7):
                    wide = random.choices([0, 1], weights=[0.94, 0.06])[0]
                    noball = random.choices([0, 1], weights=[0.97, 0.03])[0]
                    batsman_runs = 0 if wide else random.choices(
                        [0, 1, 2, 3, 4, 6], weights=[0.35, 0.30, 0.10, 0.03, 0.15, 0.07]
                    )[0]
                    dismissed = 0
                    dismissal_kind = None
                    fielder = None
                    if not wide and not noball and random.random() < 0.045:
                        dismissed = 1
                        dismissal_kind = random.choice([
                            "caught", "bowled", "lbw", "run out", "stumped", "hit wicket"
                        ])
                        fielder = random.choice(BATSMEN) if dismissal_kind in ["caught", "run out"] else None
                        if batsman_idx < len(batsmen_in):
                            current_batsman = batsmen_in[batsman_idx]
                            batsman_idx += 1
                    records.append({
                        "match_id": mid,
                        "inning": inning,
                        "batting_team": batting,
                        "bowling_team": bowling,
                        "over": over,
                        "ball": ball,
                        "batsman": current_batsman,
                        "non_striker": non_striker,
                        "bowler": bowler,
                        "is_super_over": 0,
                        "wide_runs": wide,
                        "bye_runs": 0,
                        "legbye_runs": 0,
                        "noball_runs": noball,
                        "penalty_runs": 0,
                        "batsman_runs": batsman_runs,
                        "extra_runs": wide + noball,
                        "total_runs": batsman_runs + wide + noball,
                        "player_dismissed": current_batsman if dismissed else None,
                        "dismissal_kind": dismissal_kind,
                        "fielder": fielder,
                    })
    return pd.DataFrame(records)


def generate_players() -> pd.DataFrame:
    rows = []
    for name, (role, nationality, primary_team) in PLAYER_META.items():
        rows.append({
            "player_name": name,
            "role": role,
            "nationality": nationality,
            "primary_team": primary_team,
        })
    return pd.DataFrame(rows).sort_values("player_name").reset_index(drop=True)


def generate_seasons() -> pd.DataFrame:
    rows = []
    for season in range(2008, 2025):
        oc_player, oc_runs = ORANGE_CAP[season]
        pc_player, pc_wkts = PURPLE_CAP[season]
        rows.append({
            "season": season,
            "champion": SEASON_WINNERS[season],
            "runner_up": SEASON_RUNNERS_UP[season],
            "orange_cap_player": oc_player,
            "orange_cap_runs": oc_runs,
            "purple_cap_player": pc_player,
            "purple_cap_wickets": pc_wkts,
        })
    return pd.DataFrame(rows)


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)
    print("Generating matches data...")
    matches = generate_matches()
    matches.to_csv(os.path.join(out_dir, "matches.csv"), index=False)
    print(f"  -> {len(matches)} matches saved.")
    print("Generating deliveries data (this may take a moment)...")
    deliveries = generate_deliveries(matches)
    deliveries.to_csv(os.path.join(out_dir, "deliveries.csv"), index=False)
    print(f"  -> {len(deliveries)} deliveries saved.")
    print("Generating players data...")
    players = generate_players()
    players.to_csv(os.path.join(out_dir, "players.csv"), index=False)
    print(f"  -> {len(players)} players saved.")
    print("Generating seasons data...")
    seasons = generate_seasons()
    seasons.to_csv(os.path.join(out_dir, "seasons.csv"), index=False)
    print(f"  -> {len(seasons)} seasons saved.")
    print("Done! Data files written to data/")


if __name__ == "__main__":
    main()
