from typing import Tuple
from click import pause

import logging
from config.db_config import clear
from parsing.leagues_data import parse_leagues_id, parse_seasons_year
from scraping.league_pages import scrape_league_pages, scrape_league_season_urls_page

##########################################	GLOBAL SCOPE	#######################################
# logs

logger = logging.getLogger(__name__)

##########################################	FUNCTIONS	###########################################


def select_league():
    league_pages = scrape_league_pages(200)
    leagues_id = parse_leagues_id(league_pages)

    while True:
        for n, league in enumerate(leagues_id):
            print(f"{n} - {league}")
        league_input = int(input(f"Select a league index : ").strip())
        clear()
        if  0 <= league_input < len(leagues_id):
            espn_league_id = list(leagues_id.values())[league_input]
            break
        else:
            print(
                f"Invalid entry. Please select an index between 0 and {len(leagues_id)-1}."
            )
    return espn_league_id


# --------------------------------------------------------------------------------------------------


def select_season_type():
    while True:
        season_type_input = int(
            input(
                "Do you want to scrape (1) the last gameday of the season or (2) a specific year? (1/2): "
            ).strip()
        )
        clear()
        if season_type_input in [1, 2]:
            break
        else:
            print("Invalid entry. Please select 1 or 2.")
    return season_type_input


# --------------------------------------------------------------------------------------------------


def select_season(espn_league_id):
    season_pages = scrape_league_season_urls_page(espn_league_id, 200)
    seasons_year = parse_seasons_year(season_pages)

    while True:
        for n, year in enumerate(seasons_year):
            print(f"{n} - {year}")
        year_input = int(input(f"Select year index : ").strip())
        clear()
        if 0 <= year_input < len(seasons_year):
            year = seasons_year[year_input]
            break
        else:
            print(
                f"Invalid entry.  Please select an index between 0 and {len(seasons_year)-1}."
            )
    return year


# --------------------------------------------------------------------------------------------------


def ui_scraper_config() -> Tuple[int, int, bool]:
    """
    Asks the user for information on the league and season to be scrapped.

    Returns:
        espn_league_id (int): espn league identifier of the selected season
        season_year (int): year of the selected season
        is_full_season_scrape (boolean): indicates the choice of recovering the whole season (True)
                                         or just the last day (False).
    """
    print("Scraper configuration: ")

    # League selection
    espn_league_id = select_league()
    
    # Choix du type de scraping pour la saison
    season_type = select_season_type()
    
    if season_type == 2 :
        is_full_season_scrape = True
        season_year = select_season(espn_league_id)
    else :
        is_full_season_scrape = False
    pause("Press Enter to scrape data ...")
    clear()
    return espn_league_id, season_year, is_full_season_scrape
