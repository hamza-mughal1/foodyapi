import json
from pathlib import Path
from fastapi import FastAPI

def update_routes_json(app: FastAPI, file_path: str) -> None:
    """
    Update a JSON file containing routes of a FastAPI app with default roles and add an 'excluded_endpoints' list.

    Args:
        app (FastAPI): The FastAPI application instance.
        file_path (str): The file path to save the updated JSON file.

    Returns:
        None
    """
    # Extract all paths from the app
    app_routes = {route.path for route in app.routes if hasattr(route, "path")}

    # Check if the file exists
    file = Path(file_path)
    if file.exists():
        # Load existing data from the file
        with open(file_path, "r") as f:
            config_data = json.load(f)
    else:
        # Initialize the config with an empty dictionary if it doesn't exist
        config_data = {}

    # Ensure 'excluded_endpoints' exists in the config, create it as an empty list if not present
    if "excluded_endpoints" not in config_data:
        config_data["excluded_endpoints"] = []

    # Update the dictionary for routes
    if "routes" not in config_data:
        config_data["routes"] = {}

    # Add new routes with the default role "all"
    for route in app_routes:
        if route not in config_data["routes"]:
            config_data["routes"][route] = ["all"]

    # Remove routes from the config that are not in the app
    routes_to_remove = [route for route in config_data["routes"] if route not in app_routes]
    for route in routes_to_remove:
        del config_data["routes"][route]

    # Save the updated dictionary to the file
    with open(file_path, "w") as f:
        json.dump(config_data, f, indent=4)