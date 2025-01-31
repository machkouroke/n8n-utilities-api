from pprint import pprint
from typing import Optional

from pydantic import BaseModel

top_leagues = {
    "France": {  # Source [2], [7], [11]
        "name": "Ligue 1",
        "teams": {
            "Paris Saint Germain", "Marseille", "Olympique Lyonnais", "Lille",
            "Monaco", "Montpellier", "Nantes", "Nice", "Rennes",
            "Strasbourg", "Lens", "Stade de Reims", "Toulouse", "Auxerre",
            "Saint Etienne", "Angers", "LE Havre", "Brest"
        }
        # 18 équipes confirmées
    },
    "Spain": {  # Source [3], [8]
        "name": "La Liga",
        "teams": {
            "Real Madrid", "Atletico Madrid", "Barcelona", "Athletic Club",
            "Villarreal", "Mallorca", "Real Sociedad", "Girona", "Real Betis",
            "Osasuna", "Sevilla", "Rayo Vallecano", "Celta Vigo", "Las Palmas",
            "Leganes", "Getafe", "Alaves", "Espanyol", "Valencia",
            "Valladolid"
        }
        # 20 équipes confirmées
    },
    "England": {  # Source [4], [9]
        "name": "Premier League",
        "teams": {
            "Liverpool", "Wolverhampton W", "Bournemouth", "Southampton",
            "Brighton", "Manchester City", "Crystal Palace", "Brentford",
            "Tottenham", "Leicester", "Aston Villa", "West Ham", "Fulham",
            "Manchester United", "Arsenal", "Newcastle", "Nottingham Forest",
            "Chelsea", "Everton", "Ipswich"
        }
        # 20 équipes confirmées
    },
    "Germany": {  # Source [5], [10]
        "name": "Bundesliga",
        "teams": {
            "Bayern München", "Bayer Leverkusen", "Eintracht Frankfurt",
            "VfB Stuttgart", "RB Leipzig", "Borussia Dortmund",
            "1899 Hoffenheim", "1. FC Heidenheim", "Werder Bremen", "SC Freiburg",
            "FC Augsburg", "VfL Wolfsburg", "FSV Mainz 05",
            "Borussia Mönchengladbach", "Union Berlin", "VfL Bochum",
            "FC St. Pauli", "Holstein Kiel"
        }
        # 18 équipes confirmées
    },
    "Italy": {  # Source [6]
        "name": "Serie A",
        "teams": {
            "Napoli", "Inter", "Atalanta", "Lazio", "Juventus",
            "Fiorentina", "AC Milan", "Bologna", "AS Roma", "Torino",
            "Udinese", "Genoa", "Como", "Empoli", "Cagliari",
            "Parma", "Verona", "Lecce", "Venezia", "Monza"
        }
        # 20 équipes confirmées
    }
}


class BaseTeam(BaseModel):
    ID: int
    Name: str
    Country: str
    League: Optional[str] = None

    @staticmethod
    def edit_name(data: list["BaseTeam"], name: str, new_name: str):
        for team in data:
            if team.Name == name:
                team.Name = new_name
                break
        return data


def filter_top_division_teams(data: list[BaseTeam]) -> list[BaseTeam]:
    # Liste pour stocker les équipes filtrées
    filtered_teams = []

    # Traitement de chaque équipe
    for team in data:
        country = team.Country
        name = team.Name

        # Vérifier si l'équipe appartient à un des 5 grands championnats
        if country in top_leagues and name in top_leagues[country]["teams"]:
            filtered_teams.append(BaseTeam(
                ID=team.ID,
                Name=name,
                Country=country,
                League=top_leagues[country]["name"]
            ))

    return filtered_teams


if __name__ == "__main__":
    import json

    with open('footapipaid.json', 'r', encoding='utf-8') as file:
        data: list[BaseTeam] = [BaseTeam(**team) for team in json.load(file)]
    to_update = [
        {"Stade Brestois 29": "Brest"},
        {"Reims": "Stade de Reims"},
    ]
    for update in to_update:
        for old_name, new_name in update.items():
            data = BaseTeam.edit_name(data, old_name, new_name)
    filtered_teams: list[BaseTeam] = filter_top_division_teams(data)
    # Group by country
    countries = {}
    for team in filtered_teams:
        country = team.Country
        if country not in countries:
            countries[country] = []
        countries[country].append(team)
    # size of each country
    for country in countries:
        print(f"{country}: {len(countries[country])}")
    # Display for each country the team that are in the top_leagues dict but not in the filtered_teams
    for country in countries:
        print(f"{country}:")
        for team in top_leagues[country]["teams"]:
            if team not in [t.Name for t in countries[country]]:
                print(f"\t{team}")

    with open('filtered_teams.json', 'w', encoding='utf-8') as file:
        json.dump([
            team.model_dump() for team in filtered_teams
        ], file, ensure_ascii=False, indent=4)
