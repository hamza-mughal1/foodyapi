import json
from fastapi import HTTPException, Request, status
from utilities.dependencies import uncheck_token
from pathlib import Path

def get_config_file_path(filename: str = "access_config.json") -> str:
    """
    Returns the absolute path to the configuration file in the same directory as the script.
    """
    # Get the directory of the current script
    script_dir = Path(__file__).resolve().parent
    # Construct the full path to the config file
    config_file_path = script_dir / filename
    return str(config_file_path)

def check_access(request: Request, token: uncheck_token):
    CONFIG_FILE = get_config_file_path(filename="access_config.json")
    endpoint_path = request.url.path
    user_role = token["role"]
    try:
        with open(CONFIG_FILE, "r") as f:
            roles_config = json.load(f)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Roles config file not found",
        )

    allowed_roles = roles_config.get(endpoint_path)
    print("user_role", user_role, "allowed_roles",allowed_roles)
    if (allowed_roles is None or user_role not in allowed_roles) or not "all" in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: insufficient permissions",
        )
        
    return token