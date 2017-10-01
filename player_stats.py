import json
import requests
from ratelimit import *

from private_constants import API_KEY

LABELS_TO_REPORT_TO_USER = ['Wins',
                            'Kills',
                            'Top 10s',
                            'Assists',
                            'K/D Ratio',
                            'Team Kills',
                            'Rounds Played',
                            'Headshot Kills',
                            'Longest Time Survived']

HEADERS = {'content-type': "application/json",
           'trn-api-key': API_KEY}

PUBG_TRACKER = 'https://pubgtracker.com/api/profile/pc/%s'

DEFAULT_PLAYER_STAT_STR = 'Invalid syntax, try: !stats player_name <solo/duo/squad>'

from base_stats import Statistics

class PUBGPlayerStatistics(Statistics):
    def __init__(self, player_name, game_mode):

        self.player_name = player_name
        self.game_mode = game_mode

        title = '%s (%s)' % (self.player_name.upper(), self.game_mode.upper())
        super(PUBGPlayerStatistics, self).__init__(title, default_str=DEFAULT_PLAYER_STAT_STR, headers=['Stat' , 'Value', 'Percentile'])

    @rate_limited(2)
    def get_stats(self):

        important_stats = []
        try:
            pubgtracker_page = requests.get(PUBG_TRACKER % self.player_name, headers=HEADERS)
            if pubgtracker_page.status_code != 200:
                self.get_request_failed = 'Request to query URL %s failed with status code %s.\nIs the game down?' % (PUBG_TRACKER % self.player_name, pubgtracker_page.status_code)
                return

            all_player_data = json.loads(pubgtracker_page.text)

            # Request returns 200, then informs us there is an error.. thanks
            if 'error' in all_player_data:
                self.get_request_failed = 'Pubg Api returned an error: %s' % all_player_data['error']
                return

            all_stats = all_player_data['Stats']
            important_stats = [s for s in all_stats if s['Season'] == all_player_data['defaultSeason'] and
                                                       s['Region'] == 'na' and
                                                       s['Match'].lower() == self.game_mode][0]
        except Exception:
            self.list_of_stats = ['N/A', 'N/A', 'N/A']

        # other useful stuff is statistics_dict['Match'] / statistics_dict['Stats'] / statistics_dict['Season']

        for stat in important_stats['Stats']:
            if stat['label'] in LABELS_TO_REPORT_TO_USER:
                self.list_of_stats.append([stat['label'], stat['displayValue'], stat['percentile']])
