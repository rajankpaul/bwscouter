# BWScouter

BWScouter (short for BedWars Scouter) is a Python script that allows you to retrieve various statistics for a player in Hypixel's popular game mode, BedWars. With BWScouter, you can easily view a player's Bedwars experience, Bedwars stars, win/loss ratio, final kill/death ratio, and more.

## Features

- Retrieve Bedwars statistics for any player in Hypixel's Bedwars game mode
- Calculate Bedwars stars for a player based on their Bedwars experience
- View win/loss ratio and final kill/death ratio for a player

## Future Plans

We plan to add the following features to BWScouter in the future:

- Support for other game modes in Hypixel, such as SkyWars and Mega Walls
- Integration with Discord, allowing users to easily retrieve Bedwars statistics for any player in their Discord server
- Ability to view historical data for a player, including changes in their Bedwars stats over time

## How to Use

To use BWScouter, simply run the Python script and enter the name of the player you want to view statistics for. If the player is found, BWScouter will display their Bedwars stats, including their Bedwars experience, Bedwars stars, win/loss ratio, final kill/death ratio, and more. You can also enter the command `/top1` to view the top player on the Bedwars leaderboard, or `/top10` to view the top 10 players.

Please note that to use BWScouter, you will need to have a valid Hypixel API key. You can obtain an API key by following the instructions on the [Hypixel API website](https://api.hypixel.net/). Once you have obtained an API key, enter it into the `config.ini` file included with the script.

**Note:** The `config.ini` file is not included with the script in order to prevent people from accidentally uploading their API keys to GitHub. Please be cautious and aware that accidentally uploading your API key can be a security risk and may lead to your account being banned.

Here is an example format for the `config.ini` file:

    [hypixel]
    api_keys = YOUR_API_KEY_HERE_1, YOUR_API_KEY_HERE_2, YOUR_API_KEY_HERE_3

## Changes Made

- Implemented a function `calculate_optimal_sleep_time()` to calculate the optimal sleep time between API requests based on the number of API keys available and the API request limit per minute.
- Updated the main loop to use the optimal sleep time instead of a fixed sleep time of 1 second.
- Implemented a check to ensure that the total number of API requests per minute does not exceed the Hypixel API server's request limit of 120 queries per minute.
- Added error handling to catch and display errors that may occur during API requests.
- Updated the README to include information about the changes made to the code, and added an example format for the `config.ini` file.