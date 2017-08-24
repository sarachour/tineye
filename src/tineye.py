import sys
import argparse
from database import Database,Scraper
from paths import paths

def __main__():
    parser = argparse.ArgumentParser(description='Analyze smart contracts.')

    subparsers = parser.add_subparsers(help='perform various operations over the blockchain.',
                                       dest='tool')

    # load all the unique contracts.
    p_bootstrap = subparsers.add_parser('bootstrap',
                                     help='load unique contracts into database.')

    # trace all the executions for a unique contract
    p_trace = subparsers.add_parser('trace',
                                     help='generate a trace for a contract through the blockchain.')

    # load all the unique contracts.
    p_clean = subparsers.add_parser('clean',
                                     help='load unique contracts into database.')

    args = parser.parse_args()

    database = Database(paths.db_dir);
    scraper = Scraper(database,"..")
    if args.tool == "bootstrap":
        print("=== Bootstrapping ===");
        scraper.crawl()
        database.close()

    elif args.tool == "clean":
        print("=== Clearing ===");
        database.clear()
        database.close()

    else:
        print("=== Unimpl ===");


__main__()
