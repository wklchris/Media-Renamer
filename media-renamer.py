import argparse
from TV import TMDB

# --- This is an example of media-renamer usage. ---

# # Prepare a setting.json file by replacing "YOUR_TMDB_API_KEY_HERE" with your API key.
# # Please refer to the ReadMe for details.

# # Initialize a TMDB object
# scraper = TMDB(workdir='.')

# # Input '2' to select season 2; and input '2' to select the main (non-SP) part
# scraper.search("白色相簿")  

# # Fake files under 'test' folder to test renaming.
# # In this case, work directory will be set to 'test'. 
# scraper.make_test_files(total=13)

# # Rename videos & subtitles. Press Enter to rename.
# # - Video exts: ['.mp4', '.mkv']
# # - Subtitle exts: ['.ass', '.mkv']
# scraper.rename_local_files()

def set_arg_parser():
    parser = argparse.ArgumentParser(
        description='Media-renamer: A renaming tool for local TV files using TMDB data.'
    )
    # Search by either tvname or tvid.
    parser.add_argument('--ID-mode', '-m', action='store_true',
        help='Search by ID (default by word).')
    parser.add_argument('searchword', help='Search string.')
    
    parser.add_argument('--api', '-a', help="User's TMDB API key (V3). Only for initializing the config file at the first run.")
    parser.add_argument('--config', '-c', help='Config file path.')
    parser.add_argument('--test', '-T', action='store_true', help="Test mode.")
    parser.add_argument('--dir', '-d', help='Local file directory.')
    parser.add_argument('--video-exts', '-v', nargs='+', help='Video file extensions.')
    parser.add_argument('--subtitle-exts', '-s', nargs='+', help='Subtitle file extensions.')
    return parser

def init_scraper(args):
    """Set args for creating a TMDB object."""
    init_args = {
        "workdir": args.dir,
        "api_key": args.api
    }
    if args.config:
        init_args["config_file"] = args.config
    if args.video_exts:
        init_args["video_exts"] = args.video_exts
    if args.subtitle_exts:
        init_args["subtitle_exts"] = args.video_exts
    scraper = TMDB(**init_args)
    print(scraper.video_exts)
    return scraper

def process_renaming(scraper, args):
    """Renaming files according to the scraper and args."""
    # Search by tvname or by tvid
    if args.ID_mode:
        scraper.search_id_series(args.searchword)
    else:
        scraper.search(args.searchword)
    # Enable test mode or not
    if args.test:
        ep_num = len(scraper.tv_fnames)
        scraper.make_test_files(total=ep_num)
    # Rename files
    scraper.rename_local_files()
    return scraper


# --- Main ---

def main():
    parser = set_arg_parser()
    args = parser.parse_args()
    scraper = init_scraper(args)
    scraper = process_renaming(scraper, args)

main()
