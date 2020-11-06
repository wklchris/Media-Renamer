from TV import TMDB

# --- This is an example of media-renamer usage. ---

# Prepare a setting.json file by replacing "YOUR_TMDB_API_KEY_HERE" with your API key.
# Please refer to the ReadMe for details.

# Initialize a TMDB object
scraper = TMDB(workdir='.')

# Input '2' to select season 2; and input '2' to select the main (non-SP) part
scraper.search("白色相簿")  

# Fake files under 'test' folder to test renaming.
# In this case, work directory will be set to 'test'. 
scraper.make_test_files(total=13)

# Rename videos & subtitles. Press Enter to rename.
# - Video exts: ['.mp4', '.mkv']
# - Subtitle exts: ['.ass', '.mkv']
scraper.rename_local_files()
