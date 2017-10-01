from gun_stats import PUBGGunStatistics, DEFAULT_GUN_STAT_STR
from player_stats import PUBGPlayerStatistics, DEFAULT_PLAYER_STAT_STR

def handle_message_help():
    '''
    Provides help for the user.
    @return: all of the messages the bot can understand and react to
    @rtype: str
    '''
    return 'Accepted commands are: %s' % ', '.join(PUBLIC_MESSAGE_HANDLER_FUNCTIONS)

def handle_message_gun(message):
    '''
    The user can specify a gun name, and the bot will provides stats about the gun.
    @return: some useful stats about the gun name the user provided (or a list of all of the guns, if an invalid/null gun name was provided)
    @rtype: str
    '''
    try:
        gun = message.content.lower().split(' ')[1].strip()
        gun_stats = PUBGGunStatistics(gun)
        gun_stats.get_stats()
    except Exception as e:
        print('message_handler.py, handle_message_gun(): %s' % e)
        return DEFAULT_GUN_STAT_STR

    return gun_stats.__str__()

def handle_message_debug():
    '''
    A debug function for the developer.
    @return: whatever string is necessary for debugging. This string will be printed to discord chat.
    @rtype: str
    '''
    return ':chicken:'

def handle_message_invalid():
    '''
    Handle an invalid message. Bot will react to all messages that begin with token '!',
    but it only knows how to handle certain commands
    @return: prompts the user to try the !help command
    @rtype: str
    '''
    return 'I don\'t understand your accent. Try !help'

def handle_message_stats(message):
    '''
    The user can specify a players in-game name and game mode, and the bot will provides stats about that player.
    Usage is: !stats player_name <solo/duo/squad>.
    @return: some useful stats about the player name for a specific game mode
    @rtype: str
    '''
    try:
        player_name = message.content.lower().split(' ')[1].strip()
        game_mode = message.content.lower().split(' ')[2].strip()
        player_stats = PUBGPlayerStatistics(player_name, game_mode)
        player_stats.get_stats()
    except Exception as e:
        print('message_handler.py, handle_message_stats(): %s' % e)
        return DEFAULT_PLAYER_STAT_STR

    return player_stats.__str__()

MESSAGE_HANDLER_FUNCTIONS_NO_ARGS = {'!help': handle_message_help,
                                     '!debug': handle_message_debug,
                                     '!invalid': handle_message_invalid}

MESSAGE_HANDLER_FUNCTIONS_ARGS = {'!gun': handle_message_gun,
                                  '!stats': handle_message_stats}

MESSAGE_HANDLER_FUNCTIONS_ALL = dict(MESSAGE_HANDLER_FUNCTIONS_NO_ARGS, **MESSAGE_HANDLER_FUNCTIONS_ARGS)

PUBLIC_MESSAGE_HANDLER_FUNCTIONS = list(MESSAGE_HANDLER_FUNCTIONS_ALL.keys())
PUBLIC_MESSAGE_HANDLER_FUNCTIONS.remove('!invalid')
