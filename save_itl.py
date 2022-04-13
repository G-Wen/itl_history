from email.mime import base
import requests
import json
import os
import datetime
import time
import pathlib
import tarfile
from gsendpoints import *

def get_leaderboard():
    r = requests.get(leaderboard_endpoint)
    leaderboard = json.loads(r.text)
    return leaderboard

def get_song_list():
    r = requests.get(song_list_endpoint)
    song_list = json.loads(r.text)
    return song_list

def get_song_scores(song_id):
    r = requests.get(f"{song_scores_endpoint}{song_id}")
    song_scores = json.loads(r.text)
    return song_scores

def get_song_info(song_id):
    r = requests.get(f"{song_info_endpoint}{song_id}")
    song_info = json.loads(r.text)
    return song_info

def get_song_ids():
    ids = []
    song_list = get_song_list()
    for song in song_list:
        ids.append(song['song_id'])
    return ids

def get_entrant_ids():
    # Return a list of entrant ids with non-zero score or at least 1 pass
    # We need the pass condition because IN THEORY someone can only have 0% EX passes
    entrants = get_leaderboard()['entrants']
    time.sleep(1)
    ids = []
    for entrant in entrants:
        if entrant['entrant_ranking_points'] or entrant['entrant_total_songs_pass']:
            ids.append(entrant['entrant_id'])
    return ids

def save_leaderboard(folder=None):
    if not folder:
        path = f"leaderboard.json"
    else:
        path = folder / f"leaderboard.json"

    if not os.path.exists(folder):
        os.makedirs(folder)
   
    try:
        r = requests.get(leaderboard_endpoint)
        time.sleep(1)
        if not json.loads(r.text)['success']:
            raise
        with open(path, "w+") as f:
            f.write(r.text)
    except:
        print(f"Failed to save leaderboard.")
 
def save_song_info(song_id, folder=None):
    if not folder:
        path = f"{song_id}.json"
    else:
        path = folder / f"{song_id}.json"

    try:
        r = requests.get(f"{song_info_endpoint}{song_id}")
        if not json.loads(r.text)['success']:
            raise
        with open(path, "w+") as f:
            f.write(r.text)
    except:
        print(f"Failed to save song info: {song_id}")
        raise

def save_song_scores(song_id: int, folder=None):
    if not folder:
        path = f"{song_id}.json"
    else:
        path = folder / f"{song_id}.json"

    try:
        r = requests.get(f"{song_scores_endpoint}{song_id}")
        if not json.loads(r.text)['success']:
            raise
        with open(path, "w+") as f:
            f.write(r.text)
    except:
        print(f"Failed to save song scores: {song_id}")
        raise

def save_songs(song_ids: list, scores_folder=None, info_folder=None):
    dayhour = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H")
    if not scores_folder:
        scores_folder = pathlib.Path().resolve() / "data" / dayhour / "song_scores"
    if not os.path.exists(scores_folder):
        os.makedirs(scores_folder)

    failed_scores = []
    for id in song_ids:
        try: 
            save_song_scores(id, scores_folder)
            time.sleep(1)
        except:
            failed_scores.append(id)
    if failed_scores:
        print(f"Failed to save song scores for: {failed_scores}")
    
    if not info_folder:
        info_folder = pathlib.Path().resolve() / "data" / dayhour / "song_info"
    if not os.path.exists(info_folder):
        os.makedirs(info_folder)

    failed_info = []
    for id in song_ids:
        try: 
            save_song_info(id, info_folder)
            time.sleep(1)
        except:
            failed_info.append(id)
    if failed_info:
        print(f"Failed to save song info for: {failed_info}")

def save_entrant_info(entrant_id: int, folder=None):
    if not folder:
        path = f"{entrant_id}.json"
    else:
        path = folder / f"{entrant_id}.json"

    try:
        r = requests.get(f"{entrant_info_endpoint}{entrant_id}")
        if not json.loads(r.text)['success']:
            raise
        with open(path, "w+") as f:
            f.write(r.text)
    except:
        print(f"Failed to save entrant info: {entrant_id}")
        raise

def save_entrant_scores(entrant_id: int, folder=None):
    if not folder:
        path = f"{entrant_id}.json"
    else:
        path = folder / f"{entrant_id}.json"

    try:
        r = requests.get(f"{entrant_scores_endpoint}{entrant_id}")
        if not json.loads(r.text)['success']:
            raise
        with open(path, "w+") as f:
            f.write(r.text)
    except:
        print(f"Failed to entrant scores: {entrant_id}")
        raise

def save_entrants(entrant_ids: list, scores_folder=None, info_folder=None):
    dayhour = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H")
    if not scores_folder:
        scores_folder = pathlib.Path().resolve() / "data" / dayhour / "entrant_scores"
    if not os.path.exists(scores_folder):
        os.makedirs(scores_folder)

    failed_scores = []
    for id in entrant_ids:
        try: 
            save_entrant_scores(id, scores_folder)
            time.sleep(1)
        except:
            failed_scores.append(id)
    if failed_scores:
        print(f"Failed to save entrant scores for: {failed_scores}")

    if not info_folder:
        info_folder = pathlib.Path().resolve() / "data" / dayhour / "song_info"
    if not os.path.exists(info_folder):
        os.makedirs(info_folder)

    failed_info = []
    for id in entrant_ids:
        try: 
            save_entrant_info(id, info_folder)
            time.sleep(1)
        except:
            failed_info.append(id)
    if failed_info:
        print(f"Failed to save entrant info for: {failed_info}")

def take_itl_snapshot(dayhour, basefolder=None):
    if not basefolder:
        leaderboard_folder = pathlib.Path().resolve() / "data" / dayhour
        song_scores_folder = pathlib.Path().resolve() / "data" / dayhour / "song_scores"
        entrant_scores_folder = pathlib.Path().resolve() / "data" / dayhour / "entrant_scores"
        song_info_folder = pathlib.Path().resolve() / "data" / dayhour / "song_info"
        entrant_info_folder = pathlib.Path().resolve() / "data" / dayhour / "entrant_info"
    else:
        leaderboard_folder = basefolder
        song_scores_folder = basefolder/ "song_scores"
        entrant_scores_folder = basefolder / "entrant_scores"
        song_info_folder = basefolder / "song_info"
        entrant_info_folder = basefolder / "entrant_info"

    song_ids = [1, 3, 4, 5, 6, 8, 9, 13, 14, 15, 16, 18, 19, 21, 23, 24, 25, 26, 27, 31, 32, 34, 35, 36, 38, 39, 42, 43, 44, 46, 47, 48, 49, 51, 53, 55, 56, 58, 59, 60, 61, 62, 65, 67, 69, 72, 73, 75, 76, 77, 78, 81, 83, 85, 86, 87, 89, 90, 91, 93, 94, 96, 98, 99, 100, 84, 101, 102, 103, 104, 106, 108, 109, 110, 111, 113, 115, 117, 119, 121, 122, 123, 124, 125, 126, 129, 130, 136, 137, 138, 140, 141, 142, 143, 147, 148, 149, 150, 151, 152, 153, 158, 159, 161, 162, 179, 146, 165, 166, 167, 168, 169, 170, 171, 173, 175, 177, 178, 180, 183, 187, 144, 164, 181, 189, 191, 193, 196, 199, 200, 201, 202, 203, 204, 207, 209, 210, 211, 212, 213, 214, 217, 220, 221, 222, 223, 224, 226, 229, 230, 231, 232, 234, 235, 236, 237, 238, 228, 242, 243, 244, 245, 247, 248, 250, 251, 241, 253, 257, 258, 259, 260, 262, 263, 264, 265, 268, 269, 271, 272, 274, 275, 279, 280, 283, 277, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 300]
    entrant_ids = get_entrant_ids()
    save_leaderboard(leaderboard_folder)
    save_songs(song_ids, song_scores_folder, song_info_folder)
    save_entrants(entrant_ids, entrant_scores_folder, entrant_info_folder)

def zip_data(folder, dayhour):
    tf = folder.parent / f"itl_{dayhour}.tar.gz"
    with tarfile.open(tf, "x:gz") as tar:
        tar.add(folder, arcname=f"itl_{dayhour}")
    return

def save_itl():
    # Hashtag Save ITL
    dayhour = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H")
    basefolder = pathlib.Path().resolve() / "data" / dayhour
    print(dayhour)

    take_itl_snapshot(dayhour)
    zip_data(basefolder, dayhour)

save_itl()

"""
# Get info for song we missed, ie do a partial rerun of a job
failed = []
dayhour = ""
basefolder = pathlib.Path().resolve() / "data" / dayhour
song_scores_folder = pathlib.Path().resolve() / "data" / dayhour / "song_scores"
song_info_folder = pathlib.Path().resolve() / "data" / dayhour / "song_info"
save_songs(failed, song_scores_folder, song_info_folder)
"""

"""
# Zip the new version after renaming the old tar
dayhour = "2022-04-12-08"
basefolder = pathlib.Path().resolve() / "data" / dayhour
zip_data(basefolder, dayhour)
"""