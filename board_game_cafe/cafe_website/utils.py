import requests
import os
import sys
import django
import xml.etree.ElementTree as ET

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'board_game_cafe.settings')
django.setup()

from cafe_website.models import Game, Author


def save_games_to_database(game_ids):
    ids = ",".join(map(str, game_ids))
    url = f"https://boardgamegeek.com/xmlapi2/thing?id={ids}"
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        print("Saving games to database...")

        for game in root.findall("item"):
            title = game.find("name[@type='primary']").attrib['value']
            min_players = game.find("minplayers").attrib['value']
            max_players = game.find("maxplayers").attrib['value']
            description = game.find("description").text
            thumbnail = game.find("thumbnail").text

            authors = game.findall("link[@type='boardgamedesigner']")
            authors_data = []
            for author in authors:
                author_name = author.attrib['value']
                author_object, _ =Author.objects.get_or_create(name=author_name)
                authors_data.append(author_object)


            game, created = Game.objects.get_or_create(
                name=title,
                defaults={
                    'min_players': int(min_players),
                    'max_players': int(max_players),
                    'description': description or '',
                    'thumbnail': thumbnail
                }
            )
            if created:
                game.author.set(authors_data)
                print(f"{title} created.")
            else:
                print(f"{title} already exists.")
    else:
        print(f"Failed to save games to database: {response.status_code}")
        print("Error message:", response.text)

if __name__ == "__main__":
    ids = [199792,266192,174430,1406,342942,233078,224517,316554,167791,162886,220308,12333,182028,169786,167355,177736,124361,341169,312484,251247]
    save_games_to_database(ids)
