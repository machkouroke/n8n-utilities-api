from datetime import datetime

import requests


def get_api_odds_teams(ligue: str):
    """
    Get the list of teams from the odds API `https://the-odds-api.com/account/`
    :param ligue: the id of the ligue in the odds API
    :return: the list of teams in the liguue on the odds API
    """
    API_KEY = '1c4d52bcc762be6253526a6cb2179978'
    url = f"https://api.the-odds-api.com/v4/sports/{ligue}/participants?apiKey={API_KEY}"

    response = requests.request("GET", url)
    return [{'team_name': team['full_name'], 'team_ligue': ligue} for team in response.json()]


