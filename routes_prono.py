from fastapi import APIRouter

from models.League import League
from utilities import create_mapping_table
import psycopg2
from psycopg2 import sql

router = APIRouter()

db_config = {
    'dbname': 'leagues',  # Remplacez par le nom de votre base de données
    'user': 'avnadmin',  # Remplacez par votre nom d'utilisateur
    'password': 'AVNS_yjrlufaPbvwZdzs8XrY',  # Remplacez par votre mot de passe
    'host': 'n8n-machkouroke-a3c1.b.aivencloud.com',  # Remplacez par l'hôte de votre base de données
    'port': 28399  # Remplacez par le port de votre base de données
}


@router.get("leagues")
async def get_leagues():
    connection = None
    cursor = None
    try:
        # Établir la connexion
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Requête SQL pour récupérer les données
        query = sql.SQL("SELECT name, odd_api_key, api_football_key FROM leagues;")
        cursor.execute(query)

        # Récupérer les résultats et les convertir en liste de dictionnaires
        columns = [desc[0] for desc in cursor.description]  # Récupérer les noms des colonnes
        leagues = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return {
            "detail": {
                "leagues": leagues,
                "nb_leagues": len(leagues)
            }
        }
    except (Exception, psycopg2.DatabaseError) as error:
        return {
            "detail": {
                "error": "Erreur lors de la récupération des données"
            }}

    finally:
        # Fermer la connexion
        if connection:
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée.")


@router.post("/mapping-table")
async def get_mapping_table(leagues: list[League]):
    """
    Get the mapping table of the teams between the odds API and the football API
    :param leagues: the list of leagues to compare
    :return: the mapping table in a dict
    """
    mapping_table = create_mapping_table(leagues)
    return {
        "detail": {
            "mapping_table": mapping_table,
            "nb_teams_mapped": len(mapping_table)
        }
    }


@router.get('/historical-data')
async def get_historical_data(home_team_id: int, away_team_id: int):
    """
    Get the historical data of the matches
    :return: the historical data
    """
    return {
        "detail": {

        }
    }
