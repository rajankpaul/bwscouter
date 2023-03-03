import requests
import json
import configparser
import time

def calculate_bedwars_stars(bedwars_xp):
    # Initialize variables
    stars = 0
    xp_remaining = bedwars_xp

    # Calculate the number of stars based on Bedwars XP
    while xp_remaining > 0:
        # Determine how much XP is needed for the next star
        if stars % 100 == 0:
            xp_needed = 500
        elif stars % 100 == 1:
            xp_needed = 1000
        elif stars % 100 == 2:
            xp_needed = 2000
        elif stars % 100 == 3:
            xp_needed = 3500
        else:
            xp_needed = 5000

        # Add a star if there's enough XP, otherwise exit the loop
        if xp_remaining >= xp_needed:
            stars += 1
            xp_remaining -= xp_needed
        else:
            break

    return stars

def get_player_stats(api_key, player_uuid):
    # Make API request to get player's Bedwars stats
    response = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={player_uuid}&game=bedwars")
    data = json.loads(response.text)

    if data.get('player') is None:
        # Player not found, return None
        print("Player not found.")
        return None
    else:
        # Extract player's Bedwars stats from JSON data
        bedwars_stats = data['player']['stats'].get('Bedwars')
        if bedwars_stats is None:
            # Player has not played Bedwars before
            print("This player has not played Bedwars before.")
            return None

        bedwars_xp = bedwars_stats.get('Experience', 0)
        bedwars_wins = bedwars_stats.get('wins_bedwars', 0)
        bedwars_losses = bedwars_stats.get('losses_bedwars', 0)
        bedwars_final_kills = bedwars_stats.get('final_kills_bedwars', 0)
        bedwars_final_deaths = bedwars_stats.get('final_deaths_bedwars', 0)
        bedwars_beds_broken = bedwars_stats.get('beds_broken_bedwars', 0)
        bedwars_beds_lost = bedwars_stats.get('beds_lost_bedwars', 0)

        # Calculate win/loss ratio and final kill/death ratio
        w_l_ratio = bedwars_wins / bedwars_losses if bedwars_losses > 0 else bedwars_wins
        fkd_ratio = bedwars_final_kills / bedwars_final_deaths if bedwars_final_deaths > 0 else bedwars_final_kills

        # Calculate Bedwars stars
        stars = calculate_bedwars_stars(bedwars_xp)

        # Return a dictionary containing the player's Bedwars stats
        return {
            'bedwars_xp': bedwars_xp,
            'bedwars_stars': stars,
            'wins': bedwars_wins,
            'losses': bedwars_losses,
            'w_l_ratio': w_l_ratio,
            'final_kills': bedwars_final_kills,
            'final_deaths': bedwars_final_deaths,
            'fkd_ratio': fkd_ratio,
            'beds_broken': bedwars_beds_broken,
            'beds_lost': bedwars_beds_lost,
        }

def print_player_stats(player_stats):
    # Print the player's Bedwars Stats
    print(f"Bedwars XP: {player_stats['bedwars_xp']}")
    print(f"Bedwars Stars: {player_stats['bedwars_stars']}")
    print(f"Wins: {player_stats['wins']}")
    print(f"Losses: {player_stats['losses']}")
    print(f"Win/Loss Ratio: {player_stats['w_l_ratio']:.2f}")
    print(f"Final Kills: {player_stats['final_kills']}")
    print(f"Final Deaths: {player_stats['final_deaths']}")
    print(f"Final Kill/Death Ratio: {player_stats['fkd_ratio']:.2f}")
    print(f"Beds Broken: {player_stats['beds_broken']}")
          
# Load API key from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['hypixel']['api_key']

# Hypixel API endpoint for the Bedwars leaderboard
leaderboard_url = f"https://api.hypixel.net/leaderboards?key={api_key}&type=bedwars"

# Make a request to the API to get the Bedwars leaderboard data
leaderboard_response = requests.get(leaderboard_url)
leaderboard_data = json.loads(leaderboard_response.text)

while True:
    # Ask the user for the player name
    player_name = input("Enter the player name (or '/exit' to quit): ")
    
    # Exit the loop if '/exit' is entered
    if player_name == '/exit':
        break
    
    elif player_name == '/top1':
        # Extract the top player's data from the leaderboard JSON data
        top_player_data = leaderboard_data["leaderboards"]["BEDWARS"][0]["leaders"][0]

        # Mojang API endpoint for UUID to name conversion
        mojang_url = f"https://sessionserver.mojang.com/session/minecraft/profile/{top_player_data}"

        # Make a request to the Mojang API
        mojang_response = requests.get(mojang_url)

        # Get the JSON data from the Mojang API response
        mojang_data = json.loads(mojang_response.text)

        # Extract the top player's name from the Mojang API data
        top_player_name = mojang_data["name"]

        # Calculate the top player's Bedwars stars
        top_player_stats = get_player_stats(api_key, top_player_data)
        top_player_stars = top_player_stats['bedwars_stars']

        # Print the top player's name and Bedwars stars
        print("The top player on the Bedwars leaderboard is:", top_player_name)
        print(f"Bedwars Stars: {top_player_stars}")
    
    elif player_name == '/top10':
        # Extract the top 10 players' data from the leaderboard JSON data
        top_players_data = leaderboard_data["leaderboards"]["BEDWARS"][0]["leaders"][:10]

        # Mojang API endpoint for UUID to name conversion
        mojang_url = "https://sessionserver.mojang.com/session/minecraft/profile/"

        # Loop through the top 10 players' data and extract their names and stars
        top_player_names_and_stars = []
        for player_data in top_players_data:
            # Make a request to the Mojang API to get the player's name
            mojang_response = requests.get(mojang_url + player_data)
            mojang_data = json.loads(mojang_response.text)
            player_name = mojang_data["name"]
            
            # Calculate the player's Bedwars stars
            player_stats = get_player_stats(api_key, player_data)
            player_stars = player_stats['bedwars_stars']
            
            # Add the player's name and stars to the list of top player names and stars
            top_player_names_and_stars.append((player_name, player_stars))

        # Print the list of top player names and stars
        print("The top 10 players on the Bedwars leaderboard are:")
        for i, (player_name, player_stars) in enumerate(top_player_names_and_stars):
            print(f"{i+1}. {player_name} - {player_stars} stars")

    else:
        # Make API request to get player's UUID
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}")
        data = json.loads(response.text)

        if data.get('id') is None:
            print("Player not found.")
        else:
            player_uuid = data['id']

            # Make API request to get player's Bedwars stats
            player_stats = get_player_stats(api_key, player_uuid)
            if player_stats is not None:
                print_player_stats(player_stats)
    
    # Wait for a short time before taking the next input
    time.sleep(1)