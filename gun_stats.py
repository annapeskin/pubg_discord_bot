import requests
from bs4 import BeautifulSoup
from ratelimit import *
from util import dev_print
import re
from base_stats import Statistics

ONLY_IN_AIR_DROP_MESSAGE = 'it can only be found in air drops'
SOMETIMES_IN_AIR_DROPS_MESSAGE = 'it can be found in air drops'
GUN_STATS_REGEX = r'%s\s\n\s.+'
GUN_STATS = ['Hit Damage', 'Initial Bullet Speed', 'Body Hit Impact Power',
             'Zero Range', 'Ammo Per Mag', 'Time Between Shots', 'Ammo Type', 'Firing Modes', '\n\sType']
PUBG_GAMEPEDIA = r'https://pubg.gamepedia.com/%s'


# TODO: CACHE

OFFICAL_GUN_NAMES = ['AKM', 'AWM',
                     'Crossbow',
                     'Groza',
                     'Karabiner 98 Kurz',
                     'M16A4', 'M24', 'M249', 'M416', 'Micro UZI', 'Mini 14', 'Mk14 EBR',
                     'P18C', 'P1911', 'P92',
                     'R1895',
                     'S12K', 'S1897', 'S686', 'SCAR-L', 'SKS',
                     'Tommy Gun',
                     'UMP9',
                     'Vector', 'VSS Vintorez']

DEFAULT_GUN_STAT_STR = '```\nAVALIABLE GUNS:\n------------------------------\n%s\n```' % ''.join([gun_name.ljust(20) for gun_name in OFFICAL_GUN_NAMES])


class PUBGGunStatistics(Statistics):
    '''
    Provides printable block of statistics on a given gun, assuming it is in OFFICIAL_GUN_NAMES.
    '''
    
    def __init__(self, gun_name):
        self.gun_name = self.get_official_gun_name(gun_name)
        super(PUBGGunStatistics, self).__init__(self.gun_name.upper(), default_str=DEFAULT_GUN_STAT_STR, headers=['Stat', 'Value'])

    def get_official_gun_name(self, gun_name):
        '''
        Interprets input and returns an official name if it can recognize a gun name in the input.
        @argtype: str
        @return: official gun name from OFFICIAL_GUN_NAMES
        @rtype: str
        @raise: LookupError
        '''
        
        dev_print('gun_stats.py, get_official_gun_name(): gun_name: %s' % gun_name)

        if gun_name == 'scarl':
            return 'SCAR-L'

        if 'kar' in gun_name:
            return 'Karabiner 98 Kurz'

        # TODO: show user all gun names that match the input if there is more than one

        for official_gun_name in OFFICAL_GUN_NAMES:
            if gun_name in official_gun_name.lower():
                return official_gun_name

        raise LookupError('Invalid gun name passed: %s' % gun_name)

    @rate_limited(2)
    def get_stats(self):
        '''
        Queries the Pubg Gamepedia for stats on the gun associated with this instance.
        Updates the instance with this information but does not return anything.
        Use __str__() to see changes.
        '''
        try:
            url = PUBG_GAMEPEDIA % self.gun_name.replace(' ', '_')
            gamepedia_page = requests.get(url)
            if gamepedia_page.status_code != 200:
                self.get_request_failed = '```\nRequest to query URL %s failed with status code %s.\nIs the website down?\n```' % (url, gamepedia_page.status_code)
                return

            gun_stats_html = gamepedia_page.text
            parse_gun_stats_html = BeautifulSoup(gun_stats_html, 'html.parser').get_text()
        except Exception as e:
            print('gun_stats.py: get_stats()1: %s' % e)
            return

        for stat in GUN_STATS:
            try:
                stat_name, stat_value = re.findall(GUN_STATS_REGEX % stat, parse_gun_stats_html)[0].strip().split('\n')
            except Exception as e:
                print('gun_stats.py: get_stats()2: %s' % e)
                stat_name = stat
                stat_value = 'N/A'
            self.list_of_stats.append([stat_name.strip(), stat_value.strip()])

        gun_can_be_found_location = 'On the Map'
        if ONLY_IN_AIR_DROP_MESSAGE in parse_gun_stats_html.lower():
            gun_can_be_found_location = 'Air Drops'
        elif SOMETIMES_IN_AIR_DROPS_MESSAGE in parse_gun_stats_html.lower():
            gun_can_be_found_location += ', Air Drops'

        self.list_of_stats.append(['Location', gun_can_be_found_location])
