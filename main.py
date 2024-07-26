from datetime import datetime
import logging
import json

from config import logging_config
from pymysql import connect, Error as PymysqlError
from typing import Dict, Any

from config.db_config import set_db_config, ui_db_config
from config.scraper_config import ui_scraper_config
from database.sql_functions import create_connection, insert, insert_or_ignore, insert_with_update
from processing.leagues_data import process_league_season_data
from processing.matches_data import process_matches_data, process_team_match_stats_data
from processing.stadiums_data import process_stadiums_data
from processing.standings_data import process_standings_data
from processing.teams_data import process_teams_data
from processing.players_data import process_player_match_stats_data, process_players_data
from scraping.events_page import filter_valid_event_pages, scrape_event_pages_by_date_range, scrape_event_pages_for_gameday
from scraping.players_page import scrape_roster_pages
from scraping.standings_page import scrape_standing_pages
from config.api_counter import get_counter

##########################################	GLOBAL SCOPE	#######################################
# logs

logger = logging.getLogger(__name__)
    
##########################################	 FUNCTION   ###########################################

def get_event_pages(league_data : Dict[str, Any], is_full_season_scrape : bool) -> list[Dict[str, Any]]:
    if is_full_season_scrape : # Retrieve data for the entire specified season
        start_date = league_data["startDate"]
        end_date = league_data["endDate"]
        event_pages = scrape_event_pages_by_date_range(league_data["espnId"], start_date, end_date)
    else : # Retrieve data for the lastes gameday of the current season
            event_pages = scrape_event_pages_for_gameday(league_data["espnId"], "")
            
    filtered_event_pages = filter_valid_event_pages(event_pages)
    return filtered_event_pages

##########################################	   MAIN     ###########################################

def main():
    
    db_config = set_db_config(ui_db_config())
    conn =  None
    try :
        with create_connection(db_config) as conn :
            # --- UI selection
            espn_league_id, season_year, is_full_season_scrape = ui_scraper_config()
            
            # --- LEAGUE TABLE
            league_data = process_league_season_data(espn_league_id, season_year)
            insert(conn, "leagues", [league_data])

            # --- Get Events Page
            event_pages = get_event_pages(league_data, is_full_season_scrape)

            # --- STADIUMS TABLE
            stadiums_data = process_stadiums_data(event_pages)
            insert(conn, "stadiums", stadiums_data)
    
            # --- TEAMS & STANDING TABLE
            standings_pages = scrape_standing_pages(espn_league_id, season_year)
            teams_data = process_teams_data(standings_pages)
            insert_with_update(conn, "teams", teams_data)
            standings_data = process_standings_data(standings_pages, league_data["uid"])
            insert_with_update(conn, "standings", standings_data)
    
            # --- MATCHES TABLE
            matches_data = process_matches_data(event_pages, league_data["uid"])
            insert(conn, "matches", matches_data)
            teams_matches_stat = process_team_match_stats_data(event_pages)
            insert(conn, "team_match_stats", teams_matches_stat)
    
            # --- PLAYERS TABLE
            roster_pages = scrape_roster_pages(event_pages)
            if roster_pages :
                players_data = process_players_data(roster_pages)
                insert_with_update(conn, "players", players_data)
                players_teams_data, players_matches_stat = process_player_match_stats_data(roster_pages, season_year)
                insert(conn, "player_team", players_teams_data)
                insert(conn, "player_match_stats", players_matches_stat)
            else :
                logger.warning(f"Players datas and statistics by macth are missing in the ESPN database. No insertion of this data will be made in our database.")
        
        logger.info(f"The program ended successfully.")
    except Exception :
        logger.error(f"The program ended with errors.")
    finally :
        logger.info(f"Total API Request made : {get_counter().get_count()}")
         
if __name__ == "__main__":
    main()