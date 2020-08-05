from TV import TMDB

scraper = TMDB()
scraper.search("白色相簿")
print('\n'.join(scraper.tv_fnames))
