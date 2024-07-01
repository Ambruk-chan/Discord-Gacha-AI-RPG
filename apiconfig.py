



import json
import os
from typing import Any

import requests


async def set_api(config_file: str) -> dict[str, Any]:
    # Go grab the configuration file for me
    file = get_file_name("configurations", config_file)
    contents = await get_json_file(file)
    # If contents aren't none, clear the API and shove new data in
    api = {}

    if contents:
        api.update(contents)

    # Return the API
    return api

# Check to see if the API is running (pick any API)
async def api_status_check(link: str, headers):

    try:
        response = requests.get(link, headers=headers)
        status = response.ok
    except requests.exceptions.RequestException as e:
        print("Error occurred Language model not currently running.")
        status = False

    return status


def get_file_name(directory: str, file_name: str) -> str:
    # Create the file path from name and directory and return that information
    filepath = os.path.join(directory, file_name)
    return filepath


async def get_json_file(filename: str) -> dict[str, Any] | None:
    # Try to go read the file!
    try:
        with open(filename, 'r') as file:
            contents = json.load(file)
            return contents
    # Be very sad if the file isn't there to read
    except FileNotFoundError:
        print("File " + filename + "not found. Where did you lose it?")
        return None
    # Be also sad if the file isn't a JSON or is malformed somehow
    except json.JSONDecodeError:
        await print("Unable to parse " + filename + " as JSON.")
        return None
    # Be super sad if we have no idea what's going on here
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
