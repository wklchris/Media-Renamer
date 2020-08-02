import requests
from bs4 import BeautifulSoup

class TVEpisode():
    def __init__(self, tvtitle=None, season=1, episode=None, eptitle=None):
        self.tvtitle = tvtitle
        self.season = season
        self.episode = episode
        self.eptitle = eptitle
        self.filename = self._stringfy()
    
    def _stringfy(self):
        filename = f"{self.tvtitle}-S{self.season:0>2d}E{self.episode:0>2d}.{self.eptitle}"
        return filename


class TVSeason():
    def __init__(self, title=None, url=None, language="zh-CN"):
        self.tvtitle = title
        self.url = url
        self.language = language
        self.episode_group = []
        self.html = None
        if self.url:
            self.parse_tmdb_html()
            
    
    def __str__(self):
        if not self.episode_group:
            return self.tvtitle if self.tvtile else 'Unknown TV Season'
        else:
            return '\n'.join([ep.filename for ep in self.episode_group])

    def get_url_from_input(self):
        self.url = input("Input URL: ")

    def _check_tmdb_language(self):
        # If no given language
        if not self.language:
            return
        # Force a display language of the webpage
        if not self.url.endswith(self.language):
            self.url = f"{self.url}?language={self.language}"

    def _fetch_tmdb_html(self):
        if not self.url:
            self.get_url_from_input()
        self._check_tmdb_language()

        html = requests.get(self.url, auth=('user', 'pass')).text
        self.html = BeautifulSoup(html, 'html.parser')

    def parse_tmdb_html(self):
        if not self.html:
            self._fetch_tmdb_html()
        self.tvtitle = self.html.title.string.split('Season')[0].rstrip()[:-1]
        self.episode_group = []
        for h3 in self.html.find_all('h3'):
            ep = h3.find('a', class_="no_click open")
            if ep:
                season, episode  = int(ep['season']), int(ep['episode'])
                eptitle = ep.text
                single_ep = TVEpisode(
                    tvtitle=self.tvtitle,
                    season=season,
                    episode=episode,
                    eptitle=ep.text
                )
                self.episode_group.append(single_ep)
        print(f"\n{self}")
