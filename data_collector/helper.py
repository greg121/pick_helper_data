import requests
from datetime import datetime
from riotwatcher import LolWatcher
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config.get('General', 'api_key')
watcher = LolWatcher(api_key)
region = config.get('General', 'region')

item_data = None
rune_data = None
champion_data = None

# Get the latest version of Data Dragon
versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
versions = requests.get(versions_url).json()
latest_version = versions[0]

def get_basic_info():
    summoner_name = config.get('General', 'summoner_name')
    top_enemy = config.get('General', 'top_enemy')
    download_count = config.get('General', 'download_count')
    # Get summoner details
    summoner = watcher.summoner.by_name(region, summoner_name)
    # Get match history
    matchlist = watcher.match.matchlist_by_puuid(region, summoner['puuid'], count=download_count)
    return summoner_name, top_enemy, matchlist



def get_latest_data_dragon_version():
    versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    versions = requests.get(versions_url).json()
    return versions[0]


def get_champion_data():
    champion_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
    champion_data = requests.get(champion_url).json()
    return champion_data['data']


def get_champion_name(champ_id):
    global champion_data

    if champion_data is None:
        champion_data = get_champion_data()

    for champ_name, champ_info in champion_data.items():
        if int(champ_info['key']) == champ_id:
            return champ_name
    return None

def get_champion_icon_url(champ_id):
    global champion_data

    if champion_data is None:
        champion_data = get_champion_data()

    for champ_name, champ_info in champion_data.items():
        if int(champ_info['key']) == champ_id:
            champ_icon_url = f'http://ddragon.leagueoflegends.com/cdn/{latest_version}/img/champion/{champ_name}.png'
            return champ_icon_url
    return None

def download_item_data():
    item_url = f"http://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/item.json"
    item_data = requests.get(item_url).json()
    return item_data


def download_rune_data():
    rune_url = f"http://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/runesReforged.json"
    rune_data = requests.get(rune_url).json()
    return rune_data


def get_rune_name(rune_id):
    global rune_data

    if rune_data is None:
        rune_data = download_rune_data()

    rune_name = None

    if rune_data:
        for rune_category in rune_data:
            for rune in rune_category['slots']:
                for inner_rune in rune['runes']:
                    if inner_rune['id'] == rune_id:
                        rune_name = inner_rune['name']
                        break
                if rune_name:
                    break
            if rune_name:
                break

    return rune_name


def get_item_name(item_id):
    global item_data

    if item_data is None:
        item_data = download_item_data()

    item_name = None

    if item_data and str(item_id) in item_data['data']:
        item_name = item_data['data'][str(item_id)]['name']

    return item_name


def get_item_url(item_id):
    global item_data

    if item_data is None:
        item_data = download_item_data()

    item_url = None

    if item_data and str(item_id) in item_data['data']:
        item_url = f"http://ddragon.leagueoflegends.com/cdn/{latest_version}/img/item/{item_id}.png"

    return item_url


def get_match_details(match_id, summoner_name):
    '''
    This function retrieves the details of a specific match for a given summoner.
    
    Args:
        match_id (int): The ID of the match to retrieve details for.
        summoner_name (str): The name of the summoner whose match details are to be retrieved.

    Returns:
        gold_lead_15: The gold lead at the 15-minute mark of the game.
        build_order: A list of item build orders for the summoner during the game.
        final_build: A list of the final item build for the summoner at the end of the game.
        runes: A list of runes used by the summoner during the game.
        own_champs: A list of the champions on the summoner's team.
        enemy_champs: A list of the champions on the enemy team.
        game_datetime: The date and time of the match.
    '''
    match = watcher.match.by_id(region, match_id)
    timeline = watcher.match.timeline_by_match(region, match_id)
    participant_id = find_participant_id(match, summoner_name)

    if participant_id is not None:
        gold_lead_15 = get_gold_lead_15(timeline, participant_id)
        build_order, final_build = get_builds(timeline, participant_id)
        runes = get_runes(match, participant_id)
        own_champs, enemy_champs = get_teams_champions(match, participant_id)
        game_datetime = datetime.fromtimestamp(match['info']['gameCreation'] / 1000)

        return gold_lead_15, build_order, final_build, runes, own_champs, enemy_champs, game_datetime
    else:
        return None, None, None, None, None, None, None


def find_participant_id(match, summoner_name):
    for participant in match['info']['participants']:
        if participant['summonerName'].lower() == summoner_name.lower():
            return participant['participantId']
    return None


def get_gold_lead_15(timeline, participant_id):
    for frame in timeline['info']['frames']:
        if frame['timestamp'] >= 15 * 60 * 1000:
            return frame['participantFrames'][str(participant_id)]['totalGold']
    return None


def get_builds(timeline, participant_id):
    build_order = []
    final_build = []

    for frame in timeline['info']['frames']:
        for event in frame['events']:
            if 'participantId' in event and event['participantId'] == participant_id:
                process_item_events(event, build_order, final_build)

    # Convert timestamps from milliseconds to minutes with two decimal places
    for i in range(len(build_order)):
        build_order[i][0] = round(build_order[i][0] / 60000, 2)

    return build_order, final_build


def process_item_events(event, build_order, final_build):
    if 'itemId' not in event:
        return

    item_name = get_item_name(event['itemId'])
    item_icon_url = get_item_url(event['itemId'])
    purchase_time = event['timestamp']

    if event['type'] == 'ITEM_PURCHASED':
        final_build.append([item_name, item_icon_url])
        update_build_order(build_order, purchase_time, item_name, item_icon_url)

    elif event['type'] == 'ITEM_SOLD' or event['type'] == 'ITEM_DESTROYED':
        if [item_name, item_icon_url] in final_build:
            final_build.remove([item_name, item_icon_url])

    elif event['type'] == 'ITEM_UNDO':
        process_item_undo_event(event, build_order, final_build, purchase_time)


def update_build_order(build_order, purchase_time, item_name, item_icon_url):
    if not build_order or purchase_time - build_order[-1][0] > 30000:
        build_order.append([purchase_time, [[item_name, item_icon_url]]])
    else:
        build_order[-1][1].append([item_name, item_icon_url])


def process_item_undo_event(event, build_order, final_build, purchase_time):
    old_item_name = get_item_name(event['beforeId'])
    new_item_name = get_item_name(event['afterId'])
    old_item_icon_url = get_item_url(event['beforeId'])
    new_item_icon_url = get_item_url(event['afterId'])

    if event['beforeId'] == 0:  # Item was sold
        final_build.append([new_item_name, new_item_icon_url])
        update_build_order(build_order, purchase_time, new_item_name, new_item_icon_url)

    elif event['afterId'] == 0:  # Item was bought
        if [old_item_name, old_item_icon_url] in final_build:
            final_build.remove([old_item_name, old_item_icon_url])

    else:  # Item was upgraded
        if [old_item_name, old_item_icon_url] in final_build:
            final_build.remove([old_item_name, old_item_icon_url])
        final_build.append([new_item_name, new_item_icon_url])
        update_build_order(build_order, purchase_time, new_item_name, new_item_icon_url)


def get_runes(match, participant_id):
    runes = []

    for participant in match['info']['participants']:
        if participant['participantId'] == participant_id:
            if 'perks' in participant:  # Use the 'perks' key instead of 'runes'
                for rune in participant['perks']['styles']:
                    for perk in rune['selections']:
                        runes.append(get_rune_name(perk['perk']))

    return runes


def get_teams_champions(match, participant_id):
    summoner_team_id = None
    for participant in match['info']['participants']:
        if participant['participantId'] == participant_id:
            summoner_team_id = participant['teamId']
            break

    own_champs = []
    enemy_champs = []
    for participant in match['info']['participants']:
        if participant['teamId'] != summoner_team_id:
            enemy_champs.append({'name': get_champion_name(participant['championId']), 'icon_url': get_champion_icon_url(participant['championId'])})
        else:
            own_champs.append({'name': get_champion_name(participant['championId']), 'icon_url': get_champion_icon_url(participant['championId'])})

    return own_champs, enemy_champs