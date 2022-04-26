import json
import os
import pathlib
from collections import defaultdict

rev_rivals = defaultdict(dict)

def load_stats(dayhour):
    entrant_info_folder = pathlib.Path().resolve() / "data" / dayhour / "entrant_info"
    entrant_jsons = [f for f in os.listdir(entrant_info_folder)]
    for entrant_json in entrant_jsons:
        entrant_info_path = entrant_info_folder / entrant_json
        with open(entrant_info_path, 'r') as f:
            data = json.loads(f.read())
            entrant = data['entrant']
            rivals = data['rivals']
            if entrant['entrant_id'] not in rev_rivals:
                rev_rivals[entrant['entrant_id']] = {'entrant_name': entrant['members_name'], 'rivals': {}}
            for rival in rivals:
                rev_rivals[rival['entrant_id']]['entrant_name'] = rival['members_name']
                if 'rivals' not in rev_rivals[rival['entrant_id']]:
                    rev_rivals[rival['entrant_id']]['rivals'] = {}
                rev_rivals[rival['entrant_id']]['rivals'][entrant['entrant_id']] = entrant['members_name']
    """
    for entrant in rev_rivals:
        rivald = {}
        for rival in entrant['rivals']:
            for k in rival:
                rivald[k] = rival[k]
        entrant['rivals'] = rivald
    """

def get_most_rivaled(size):
    most_rivaled = sorted(rev_rivals, key=lambda x: len(rev_rivals[x]['rivals']), reverse=True)
    for i, entrant in enumerate(most_rivaled[:size]):
        print(f"{i+1}: {rev_rivals[entrant]['entrant_name']} ({len(rev_rivals[entrant]['rivals'])})")

def find_rivals(entrant_id):
    for k in rev_rivals[entrant_id]['rivals']:
        print(rev_rivals[entrant_id]['rivals'][k])

def save_reverse_rival_info():
    with open('reverse_rivals.json', "w") as f:
        f.write(json.dumps(rev_rivals))

load_stats("2022-04-25-06")
find_rivals(61)