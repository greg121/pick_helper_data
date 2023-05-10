import json
from tqdm import tqdm
from riotwatcher import ApiError
import os
import helper as h

def main():
    try:
        summoner_name, top_enemy, matchlist = h.get_basic_info()
        match_history = []

        # Read existing match history data from JSON file
        cwd = os.getcwd()
        file_path = os.path.join(cwd, 'data', 'match_data.json')
        if os.path.isfile(file_path):
            with open(file_path, 'r') as infile:
                match_history = json.load(infile)

        # Loop through the match history and add new matches' data to the list
        for match in tqdm(matchlist):
            # Check if match data already exists in match history
            if any(match_data['match_id'] == match for match_data in match_history):
                continue
            print(f'{match} added to json file')    
            gold_lead_15, build_order, final_build, runes, own_champs, enemy_champs, game_datetime = h.get_match_details(match, summoner_name)
            if not top_enemy or top_enemy in enemy_champs:
                match_data = {
                    'match_id': match,
                    'date_and_time': str(game_datetime),
                    'gold_lead_15': gold_lead_15,
                    'build_order': build_order,
                    'final_build': final_build,
                    'runes': runes,
                    'own_champs': own_champs,
                    'enemy_champs': enemy_champs
                }
                match_history.append(match_data)

        # Write the updated match history data to the JSON file
        with open(file_path, 'w') as outfile:
            json.dump(match_history, outfile)

    except ApiError as e:
        if e.response.status_code == 429:
            print('Rate limit exceeded, try again later.')
        elif e.response.status_code == 404:
            print('Summoner not found.')
        else:
            print(f'An error occurred: {e.response.status_code}')

if __name__ == "__main__":
    main()