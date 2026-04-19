"""IPL analysis functions used by the dashboard."""

import pandas as pd
from src.generate_data import SEASON_WINNERS


def team_win_stats(matches: pd.DataFrame) -> pd.DataFrame:
    teams = pd.concat([matches["team1"], matches["team2"]]).unique()
    rows = []
    for team in teams:
        played = matches[(matches["team1"] == team) | (matches["team2"] == team)]
        won = matches[matches["winner"] == team]
        rows.append({"team": team, "played": len(played), "won": len(won),
                     "lost": len(played) - len(won),
                     "win_pct": round(len(won) / len(played) * 100, 1) if len(played) else 0})
    return pd.DataFrame(rows).sort_values("won", ascending=False).reset_index(drop=True)


def top_batsmen(deliveries: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    runs = (deliveries.groupby("batsman")["batsman_runs"]
            .agg(runs="sum", balls="count")
            .reset_index())
    runs["strike_rate"] = (runs["runs"] / runs["balls"] * 100).round(1)
    fifties = (deliveries.groupby(["match_id", "inning", "batsman"])["batsman_runs"]
               .sum().reset_index())
    fifties50 = (fifties[(fifties["batsman_runs"] >= 50) & (fifties["batsman_runs"] < 100)]
                 .groupby("batsman").size().reset_index(name="fifties"))
    hundreds = (fifties[fifties["batsman_runs"] >= 100]
                .groupby("batsman").size().reset_index(name="hundreds"))
    runs = runs.merge(fifties50, on="batsman", how="left").merge(hundreds, on="batsman", how="left")
    runs[["fifties", "hundreds"]] = runs[["fifties", "hundreds"]].fillna(0).astype(int)
    return runs.sort_values("runs", ascending=False).head(top_n).reset_index(drop=True)


def top_bowlers(deliveries: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    wickets = (deliveries[deliveries["player_dismissed"].notna() &
                          ~deliveries["dismissal_kind"].isin(["run out", "retired hurt", "obstructing the field"])]
               .groupby("bowler").size().reset_index(name="wickets"))
    runs_conceded = (deliveries.groupby("bowler")["total_runs"].sum().reset_index(name="runs_conceded"))
    overs_bowled = (deliveries.groupby("bowler").size().reset_index(name="balls"))
    bowl = wickets.merge(runs_conceded, on="bowler").merge(overs_bowled, on="bowler")
    bowl["overs"] = (bowl["balls"] / 6).round(1)
    bowl["economy"] = (bowl["runs_conceded"] / bowl["overs"]).round(2)
    return bowl.sort_values("wickets", ascending=False).head(top_n).reset_index(drop=True)


def season_summary(matches: pd.DataFrame) -> pd.DataFrame:
    grp = matches.groupby("season")
    summary = grp.agg(
        matches=("id", "count"),
        avg_win_by_runs=("win_by_runs", "mean"),
    ).reset_index()
    winners = pd.DataFrame([
        {"season": s, "champion": c} for s, c in SEASON_WINNERS.items()
        if s in summary["season"].values
    ])
    return summary.merge(winners, on="season")


def head_to_head(matches: pd.DataFrame, team_a: str, team_b: str) -> dict:
    h2h = matches[((matches["team1"] == team_a) & (matches["team2"] == team_b)) |
                  ((matches["team1"] == team_b) & (matches["team2"] == team_a))]
    return {
        "total": len(h2h),
        team_a: len(h2h[h2h["winner"] == team_a]),
        team_b: len(h2h[h2h["winner"] == team_b]),
    }


def toss_impact(matches: pd.DataFrame) -> pd.DataFrame:
    matches = matches.copy()
    matches["toss_win_match_win"] = matches["toss_winner"] == matches["winner"]
    return matches.groupby("toss_decision")["toss_win_match_win"].mean().reset_index(
        name="win_rate_after_toss_win")
