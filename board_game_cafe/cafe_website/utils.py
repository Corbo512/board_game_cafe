import requests
import xml.etree.ElementTree as ET


def fetch_game_details(filename, game_id):
    tree = ET.parse('games.xml')
    root = tree.getroot()

    games = []

    for game in root.findall("item"):
        title = game.find("name[@type='primary']").attrib['value']
        min_players = game.find("minplayers").attrib['value']
        max_players = game.find("maxplayers").attrib['value']
        min_age = game.find("minage").attrib['value']
        description = game.find("description").text

        games.append({"title": title,
                  "min_players": min_players,
                  "max_players": max_players,
                  "min_age": min_age,
                  "description": description
                  })

    return games


def save_games_to_file(game_ids, filename):
    ids = ",".join(map(str, game_ids))
    url = f"https://boardgamegeek.com/xmlapi2/thing?id={ids}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
