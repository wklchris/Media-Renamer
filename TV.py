import json
import re
import requests

class TMDB():
    def __init__(self, config_file='settings.json'):
        self.data = {'media_type': 'tv'}
        self.regex_unit = re.compile(r'{\w.*?}')
        self.load_config(config_file)

    def __str__(self):
        if hasattr(self, 'selected'):
            infostr = self._info_stringfy(self.selected)
        else:
            infostr = 'Nothing selected yet.'
        return infostr

    def load_config(self, config_file):
        """Load/Update the settings JSON file."""
        with open(config_file, 'r') as f:
            for k, v in json.load(f).items():
                self.data[k] = v            

    def search(self, search_str, media_type=None):
        """Search key words in TMDB's TV database and return results as a dict."""
        self.data['media_type'] = media_type if media_type else self.data['media_type']
        self.data['search_str'] = search_str
        self.search_type, self._data_key = 'api_search', 'results'
        self._get_search_data()
        self.search_id_series()  # Select a TV and check its seasons

    def search_id_series(self, search_id=None, media_type=None):
        """Search the TMDB id of a TV in the database and return a season of it."""
        self.data['media_type'] = media_type if media_type else self.data['media_type']
        self.data['media_id'] = search_id if search_id else self.selected.get('id')
        self.search_type, self._data_key = 'api_id_series', 'seasons'
        self._get_search_data()
        self.data['media_title'] = self.search_data['name']
        self.show_episode_list()  # Select a season and check its episodes
    
    def show_episode_list(self, search_id=None):
        """Show the list of episode of the selected season."""
        self.data['media_type'] = 'tv'
        self.data['order_season'] = self.selected.get('season_number')
        self.search_type, self._data_key = 'api_id_season', 'episodes'
        self._get_search_data(select=False)
        self._get_filenames()

    def _get_filenames(self):
        n = len(self.search_data[self._data_key])
        self.tv_fnames = [None for _ in range(n)]
        for i, ep in enumerate(self.search_data[self._data_key]):
            self.data['tv_season'] = ep['season_number'] 
            self.data['tv_episode'] = ep['episode_number']
            self.data['tv_eptitle'] = ep['name']
            self.tv_fnames[i] = self._regex_stringfy(self.data['filename_format_tv'])

    def _get_search_data(self, select=True):
        self.url = self._regex_stringfy(self.data[self.search_type])
        try:
            self.search_data = json.loads(requests.get(self.url).text)
        except Exception as e:
            print(e, f"\nError: Can't fetch searching results from:\n{self.url}.")
        # The request will contain a 'status_code' key if anything wrong
        if "status_code" in self.search_data.keys():
            print(f"Code {self.search_data.get('status_code')}: {self.search_data.get('status_message')}")
            exit()
        # Select a single item from the returned list
        if select:
            self._select_search_results()

    def _info_stringfy(self, media_dict):
        media_id = media_dict.get('id')
        title = media_dict.get('name')
        if self.search_type == 'api_search':
            date = media_dict.get('first_air_date', 'Unknown date')
            country = ','.join(media_dict.get('origin_country', ['Unknown country']))
            language = media_dict.get('original_language', 'Unknown language')
            info_str = f"[{media_id}] {title} ({date}; {language}; {country})"
        else:  # self.search_type == 'api_id_series'
            date = media_dict.get('air_date', 'Unknown date')
            episode_count = media_dict.get('episode_count', 'Unknown number of episodes')
            current_season = media_dict.get('season_number', 'Unknown season')
            info_str = f"[{media_id}] {title} (Season {current_season:0>2d}, {date}; total {episode_count:0>3d} episodes)"
        return info_str

    def _regex_stringfy(self, input_str):
        s = re.sub(self.regex_unit, lambda x: self._regex_unit_stringfy(x), input_str)
        return s

    def _regex_unit_stringfy(self, regex_match):
        key = regex_match.group().strip('{}')
        value = self.data.get(key, f"{key}")
        if type(value) == int:
            value = f"{value:0>2d}"
        return value

    def _select_search_results(self):
        """Select the desired one from the list of searching results."""
        data_key = self._data_key
        num_results = len(self.search_data[data_key])
        if num_results == 0:
            print(f"\nNo {self.data['media_type']} matching results: 0 {data_key}.")
        elif num_results == 1:
            self.selected = self.search_data[data_key][0]
        else:
            print("\nChoose the one that matches:")
            for i in range(num_results):
                infostr = self._info_stringfy(self.search_data[data_key][i])
                print(f"{i+1:0>2d} ~ {infostr}")
            # User select from the printed list by number #1 to #num_results
            user_select = -1
            while user_select < 0:
                user_input = int(input(f"---\nSelect from above (1~{num_results}): "))
                user_select = user_input-1 if 0 < user_input <= num_results else -1
            self.selected = self.search_data[data_key][user_select]
        print(f"Select: {self._info_stringfy(self.selected)}")
