from ast import Tuple
import logging
from typing import Dict, Any, Tuple

from processing.utils import (
    extract_linescores,
    extract_stats,
    generate_deterministic_uid,
    convert_date_time_to_MySQL,
)
from scraping.utils import scrape_url

##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

##########################################	FUNCTIONS	###########################################


def get_competitors_data(event_page : Dict[str, Any]) -> Tuple[int | None, int | None, int| None, int| None, int, int]:
    """
    Sub function of `process_matches_data` to parse competitors data.

    Args:
        event_page (Dict[str, Any]): A dictionaries containing event data,
                                    in particular competitor data.

    Returns:
        home_team_espn_id (int): home team espn id.
        away_team_espn_id (int): away team espn id.
        winner_espn_id (int): winner team espn id.
        loser_espn_id (int): loser team espn id.
        winner_score (int): winner score.
        loser_score (int): loser score.
    """
    # Init variables for match data
    home_team_espn_id = away_team_espn_id = winner_espn_id = loser_espn_id = None
    winner_score = loser_score = 0

    competitions = event_page["competitions"][0]
    competitors = competitions["competitors"]

    for competitor in competitors:
        espn_id = int(competitor["id"])
        score_page = scrape_url(competitor["score"]["$ref"])
        score = score_page["value"]
        # Check home or away team
        if competitor["homeAway"] == "home":
            home_team_espn_id = espn_id
        else:
            away_team_espn_id = espn_id
        # Check winner or away loser
        if competitor["winner"]:
            winner_espn_id = espn_id
            winner_score = score
        else:
            loser_espn_id = espn_id
            loser_score = score

    # If winner_espn_id is None at the end of the processing loop, this indicates a draw.
    # In this case, the away team is defined as the winner and the home team as the loser.
    if winner_espn_id is None:
        winner_espn_id = away_team_espn_id
        loser_espn_id = home_team_espn_id
        winner_score = loser_score = score

    return home_team_espn_id, away_team_espn_id, winner_espn_id, loser_espn_id, winner_score, loser_score

#--------------------------------------------------------------------------------------------------

def get_venue_espn_id(event_page : Dict[str, Any]) :
    """
    Sub function of `process_matches_data` to parse stadiumEspnId.

    Args:
        event_page (Dict[str, Any]): A dictionaries containing event data,
                                    in particular venue espn id.

    Returns:
        stadium_espn_id (int): venue espn id.
    """
    stadium_espn_id = None
    # Get stadium_espn_id if exist
    competitions_page = event_page["competitions"][0]
    venue = competitions_page.get("venue", None)
    if venue is None:
        logger.warning(
            f"Venue is missing in ESPN database for match '{event_page['name']}' (ID: {event_page['id']})."
        )
    else:
        stadium_espn_id = int(venue["id"])
    return stadium_espn_id

#--------------------------------------------------------------------------------------------------

def get_total_play_time(event_page : Dict[str, Any]) :
    """
    Sub function of `process_matches_data` to parse total play time.

    Args:
        event_page (Dict[str, Any]): A dictionaries containing event data,
                                    in particular total play time.

    Returns:
        total_play_time (int): total play time.
    """
    total_play_time = None
    # Get stadium_espn_id if exist
    competitions_page = event_page["competitions"][0]
    status_url = competitions_page.get("status", {}).get("$ref", None)
    if status_url is None:
        logger.warning(
            f"Total play time is missing in ESPN database for match '{event_page['name']}' (ID: {event_page['id']})."
        )
    else:
        status_page = scrape_url(status_url)
        total_play_time = status_page["clock"]
    return total_play_time

#--------------------------------------------------------------------------------------------------

def process_matches_data(
    event_pages: list[Dict[str, Any]], league_uid: str
) -> list[Dict[str, Any]]:
    """
    Processes match data from a list of event pages for a specific league.

    This function extracts detailed match information from event pages, including team scores,
    winner/loser details, and match statistics.

    Args:
        event_pages (list[Dict[str, Any]]): A list of dictionaries containing event page data.
        league_uid (str): A unique identifier for the league.

    Returns:
        list[Dict[str, Any]]: A list of dictionaries, each containing data for a single match.
        Each dictionary has the following structure:
        {
            "espnId": int,              # ESPN ID of the match
            "date": str,                # Match date in MySQL format
            "name": str,                # Full name of the match
            "abbreviationName": str,    # Short name of the match
            "leagueUid": str,           # Unique identifier of the league
            "homeTeamEspnId": int,      # ESPN ID of the home team
            "awayTeamEspnId": int,      # ESPN ID of the away team
            "winnerEspnId": int,        # ESPN ID of the winning team
            "loserEspnId": int,         # ESPN ID of the losing team
            "stadiumEspnId": int,       # ESPN ID of the stadium
            "winnerScore": int,         # Score of the winning team
            "loserScore": int,          # Score of the losing team
            "totalPlayTime": float      # Total play time of the match in seconds
        }

    Raises:
        KeyError: If required keys are missing from the event page data.
        Exception: For any unexpected errors during the processing of match data.

    Note:
        - This function relies on external functions for scraping additional data and formatting dates.
        - It processes both team information to determine home/away and winner/loser statuses.
    """
    matches_data: list[Dict[str, Any]] = []

    try:

        for page in event_pages:
            # Get Competitors data
            (home_team_espn_id, away_team_espn_id, 
             winner_espn_id, loser_espn_id, 
             winner_score, loser_score) = get_competitors_data(page)
            
            # Get stadium_espn_id
            stadium_espn_id = get_venue_espn_id(page)

            # Get Total Playtime
            total_play_time = get_total_play_time(page)

            # fill the table pattern
            match_data = {
                "espnId": int(page["id"]),
                "date": convert_date_time_to_MySQL(page["date"]),
                "name": page["name"],
                "abbreviationName": page["shortName"],
                "leagueUid": league_uid,
                "homeTeamEspnId": home_team_espn_id,
                "awayTeamEspnId": away_team_espn_id,
                "winnerEspnId": winner_espn_id,
                "loserEspnId": loser_espn_id,
                "stadiumEspnId": stadium_espn_id,
                "winnerScore": winner_score,
                "loserScore": loser_score,
                "totalPlayTime": total_play_time,
            }
            matches_data.append(match_data)

    except KeyError as key_err:
        logger.error(f"Dict parse KeyError: {key_err}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise

    return matches_data


# --------------------------------------------------------------------------------------------------


def process_team_match_stats_data(
    event_pages: list[Dict[str, Any]]
) -> list[Dict[str, Any]]:
    """
    Processes team match statistics data from a list of event pages.

    This function extracts detailed statistics for each team participating in a match,
    including line scores and other performance metrics.

    Args:
        event_pages (list[Dict[str, Any]]): A list of dictionaries containing event page data.

    Returns:
        list[Dict[str, Any]]: A list of dictionaries, each containing match statistics for a team.
        Each dictionary has the following structure:
        {
            "uid": str,                 # Unique identifier for the team-match combination
            "matchEspnId": int,         # ESPN ID of the match
            "teamEspnId": int,          # ESPN ID of the team
            "opponentEspnId": int,      # ESPN ID of the opponent team
            "linescore1stHalf": int,    # Score for the first half
            "linescore2ndHalf": int,    # Score for the second half
            "linescore20min": int,      # Score at 20 minutes
            "linescore60min": int,      # Score at 60 minutes
            ... # Additional statistics extracted from the match data
        }

    Raises:
        KeyError: If required keys are missing from the event page data.
        ValueError: If home or away team data is missing.
        Exception: For any unexpected errors during the processing of team match statistics.

    Note:
        - This function uses external functions for extracting line scores and additional statistics.
        - It generates a unique identifier for each team-match combination.
        - The function processes both home and away team data for each match.
    """
    teams_matches_stat: list[Dict[str, Any]] = []

    try:

        for page in event_pages:
            # Get Match Espn Id
            match_espn_id = int(page["id"])

            # Get Competitors
            competitions = page["competitions"][0]
            competitors = competitions["competitors"]

            for competitor in competitors:
                if competitor["homeAway"] == "home":
                    home_competitor = competitor
                elif competitor["homeAway"] == "away":
                    away_competitor = competitor
                else:
                    raise ValueError("Home or away team data is missing")
            for competitor in [home_competitor, away_competitor]:
                # get opponent id
                opponent_espn_id = int(
                    away_competitor["id"]
                    if competitor == home_competitor
                    else home_competitor["id"]
                )
                # Get team espn id
                team_espn_id = int(competitor["id"])

                # Generate deterministic uid
                uid = generate_deterministic_uid([match_espn_id, team_espn_id])

                # fill the table pattern
                team_match_data = {
                    "uid": uid,
                    "matchEspnId": match_espn_id,
                    "teamEspnId": team_espn_id,
                    "opponentEspnId": opponent_espn_id,
                }

                # Check if linescores exist
                linescore_url = competitor.get("linescores", {}).get("$ref", None)
                if linescore_url is None:
                    logger.warning(
                        f"Match linescores missing in ESPN database for match '{page['name']}' (ID: {page['id']}."
                    )
                else:
                    # If exist, add them to team_match_data
                    team_match_data = team_match_data | extract_linescores(
                        linescore_url
                    )

                # Check if Statistic exist
                stat_url = competitor.get("statistics", {}).get("$ref", None)
                if stat_url is None:
                    team_match_stat = team_match_data
                    logger.warning(
                        f"Match statistics missing in ESPN database for match '{page['name']}' (ID: {page['id']}."
                    )
                else:
                    # If exist, add them to team_match_data
                    team_match_stat = team_match_data | extract_stats(stat_url)

                # Concat
                teams_matches_stat.append(team_match_stat)

    except KeyError as key_err:
        logger.error(f"Dict parse KeyError: {key_err}")
        raise
    except ValueError as val_err:
        logger.error(f"ValueError : {val_err}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise

    return teams_matches_stat
