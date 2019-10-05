import json
import os

import arenaclient.default_test_config as config

from arenaclient.client import Client
from arenaclient.utl import Utl

# Sanity check the config and remind people to check their config
assert config.TEST_MODE, "LOCAL_TEST_MODE config value must must be set to True to run tests." + os.linesep \
                         + "IMPORTANT: Are you configured properly for tests?"
assert config.RUN_LOCAL, "RUN_LOCAL config value must must be set to True to run tests." + os.linesep \
                         + "IMPORTANT: Are you configured properly for tests?"

utl = Utl(config)

games = {
    'loser_bot,T,python,loser_bot,T,python,AutomatonLE': "Tie",
    'basic_bot,T,python,crash,T,python,AutomatonLE': "Player2Crash",
    'basic_bot,T,python,connect_timeout,T,python,AutomatonLE': "InitializationError",
    'basic_bot,T,python,crash_on_first_frame,T,python,AutomatonLE': "Player2Crash",
    'basic_bot,T,python,hang,T,python,AutomatonLE': "Player2Crash",
    'basic_bot,T,python,too_slow_bot,T,python,AutomatonLE': "Player2TimeOut",
    'basic_bot,T,python,instant_crash,T,python,AutomatonLE': "InitializationError",
    'timeout_bot,T,python,timeout_bot,T,python,AutomatonLE': "Tie",
    'crash,T,python,basic_bot,T,python,AutomatonLE': "Player1Crash",
    'connect_timeout,T,python,basic_bot,T,python,AutomatonLE': "Player1Crash",
    'crash_on_first_frame,T,python,basic_bot,T,python,AutomatonLE': "Player1Crash",
    'hang,T,python,basic_bot,T,python,AutomatonLE': "Player1Crash",
    'instant_crash,T,python,basic_bot,T,python,AutomatonLE': "Player1Crash",
    'loser_bot,T,python,basic_bot,T,python,AutomatonLE': "Player2Win",
    'too_slow_bot,T,python,basic_bot,T,python,AutomatonLE': "Player1TimeOut",
    'basic_bot,T,python,loser_bot,T,python,AutomatonLE': "Player1Win",
}

ORIGINAL_MAX_GAME_TIME = config.MAX_GAME_TIME
for key, value in games.items():

    with open(config.MATCH_SOURCE_CONFIG["MATCHES_FILE"], "w+") as f:
        f.write(key + os.linesep)
    if key == 'loser_bot,T,python,loser_bot,T,python,AutomatonLE':
        config.MAX_GAME_TIME = 1000
    else:
        config.MAX_GAME_TIME = ORIGINAL_MAX_GAME_TIME

    ac = Client(config)
    ac.run()

    try:
        with open(config.RESULTS_LOG_FILE, "r") as f:
            result = json.load(f)
        test_result = f"Result ({str(result['Results'][0]['Result'])}) matches expected result ({value}):" + \
                      str(result["Results"][0]["Result"] == value)
        utl.printout(test_result)
        with open('test_results.txt', 'a+') as f:
            f.write(str(key) + '\t' + str(test_result) + '\n')
    except FileNotFoundError:
        utl.printout("Test failed: Results file not found")
    except KeyError:
        utl.printout("Test failed: Result not found in file")
