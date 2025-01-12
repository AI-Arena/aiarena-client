#########################################################
#                                                       #
# DEFAULT CONFIG                                        #
#                                                       #
# !!!! DO NOT UPDATE THIS FILE WITH LOCAL SETTINGS !!!! #
# Create a config.py file to override config values     #
#                                                       #
#########################################################
import importlib
import logging
import os
import platform

# GENERAL
from ..match.matches import FileMatchSource

ARENA_CLIENT_ID = "aiarenaclient_000"  # ID of arenaclient. Used for AiArena
API_TOKEN = "12345"  # API Token to retrieve matches and submit results. Used for AiArena
ROUNDS_PER_RUN = 5  # Set to -1 to ignore this
BASE_WEBSITE_URL = ""
USE_PID_CHECK = False
RUN_REPLAY_CHECK = False  # Validate replays
DEBUG_MODE = True  # Enables debug mode for more logging
PYTHON = "python3"  # Which python version to use
RUN_LOCAL = False  # Run on AiArena or locally
CLEANUP_BETWEEN_ROUNDS = True  # Clean up files between rounds
SYSTEM = platform.system()  # What OS are we on?
SC2_PROXY = {"HOST": "127.0.0.1", "PORT": 8765}  # On which host and port to run the proxy between SC2 and bots

# Secure mode will ignore the BOTS_DIRECTORY config setting and instead run each bot in their home directory.
SECURE_MODE = False
# Specify the users (if any) to run the bots as.
RUN_PLAYER1_AS_USER = None
RUN_PLAYER2_AS_USER = None

# LOGGING
LOGGING_HANDLER = logging.FileHandler("../supervisor.log", "a+")
LOGGING_LEVEL = logging.DEBUG

# PATHS AND FILES
TEMP_ROOT = "/tmp/"
TEMP_PATH = os.path.join(TEMP_ROOT, "aiarena")
LOCAL_PATH = os.path.dirname(__file__)
WORKING_DIRECTORY = LOCAL_PATH  # same for now
LOG_FILE = os.path.join(WORKING_DIRECTORY, "client.log")
REPLAYS_DIRECTORY = os.path.join(WORKING_DIRECTORY, "replays")
BOTS_DIRECTORY = os.path.join(WORKING_DIRECTORY, "bots")  # Ignored when SECURE_MODE == True
CLEAN_BOT_DIRECTORIES_BEFORE_MATCH_START = True  # a quick fix to stop attempting to clean a non-existent bot directory

MATCH_SOURCE_CONFIG = FileMatchSource.FileMatchSourceConfig(
    matches_file=os.path.join(WORKING_DIRECTORY, "matches"),
    results_file=os.path.join(WORKING_DIRECTORY, "results")
)

# STARCRAFT
SC2_HOME = "/home/aiarena/StarCraftII/"
SC2_BINARY = os.path.join(SC2_HOME, "Versions/Base75689/SC2_x64")
MAX_GAME_TIME = 60486
MAX_REAL_TIME = 7200  # 2 hours in seconds
MAX_FRAME_TIME = 40
STRIKES = 10
REALTIME = False
VISUALIZE = False

# MATCHES
DISABLE_DEBUG = True
VALIDATE_RACE = False

def from_model_import_star(module: str):
    # get a handle on the module
    mdl = importlib.import_module(module)

    # is there an __all__?  if so respect it
    if "__all__" in mdl.__dict__:
        names = mdl.__dict__["__all__"]
    else:
        # otherwise we import all names that don't begin with _
        names = [x for x in mdl.__dict__ if not x.startswith("_")]

    # now drag them in
    globals().update({k: getattr(mdl, k) for k in names})

# Override values a standard config template
CONFIG_TEMPLATE = os.getenv('MODE')
if CONFIG_TEMPLATE is not None:
    module_to_import = f'arenaclient.configs.{CONFIG_TEMPLATE}_config_template'
    try:
        from_model_import_star(module_to_import)
    except ImportError as e:
        if e.name == module_to_import:
            raise f"Could not locate a config template called {module_to_import}!"
        else:
            raise

# Override values with environment specific config
try:
    from config import *
except ImportError as e:
    if e.name == "config":
        pass
    else:
        raise
