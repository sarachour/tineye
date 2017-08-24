import sys
import argparse
from database import Database,Scraper
from paths import paths
from retina import Retina

def analyze_subtool(database,codeid):
    source = database.get_code(codeid)
    txns = database.get_traces(codeid)
    eye = Retina(source,txns);
    eye.coverage()

def stats_subtool(database,metric):
    if metric == "usage":
        results = database.get_code_usage()
        print("=== Number of Traces per Contract ===")
        for (ident,ntxns) in results:
            print("%d\t%d" % (ident,ntxns))

    elif metric == "size":
        results = database.get_all_code()
        print("=== Code Size ===")
        for (ident,code) in results:
            print("%s\t%d" % (ident,len(code)))

    elif metric == "dups":
        results = database.get_code_dups()
        print("=== Code Dups ===")
        for (ident,dups) in results:
            print("%d\t%d" % (ident,dups))

def __main__():
    parser = argparse.ArgumentParser(description='Analyze smart contracts.')

    subparsers = parser.add_subparsers(help='perform various operations over the blockchain.',
                                       dest='tool')

    # load all the unique contracts.
    p_bootstrap = subparsers.add_parser('load',
                                     help='load unique contracts into database.')

    p_bootstrap.add_argument('--start', help='the identifier of the code to analyze')
    p_bootstrap.add_argument('--n', help='the identifier of the code to analyze')
    # trace all the executions for a unique contract
    p_analyze = subparsers.add_parser('analyze',
                                     help='analyze some source code blockchain.')

    p_analyze.add_argument('--code', help='the identifier of the code to analyze')

    # trace all the executions for a unique contract
    p_stats= subparsers.add_parser('stats',
                                     help='produce the trace stats for the blockchain.')

    p_stats.add_argument('--metric',help='the statistic to produce')
    # load all the unique contracts.
    p_clean = subparsers.add_parser('clean',
                                     help='load unique contracts into database.')


    args = parser.parse_args()

    database = Database(paths.db_dir);
    if args.tool == "bootstrap":
        print("=== Retrieving Data From The Blockchain ===");
        scraper = Scraper(database,"..")
        scraper.crawl(args.start, args.n)
        database.close()

    elif args.tool == "clean":
        print("=== Clearing ===");
        database.clear()
        database.close()

    elif args.tool == "stats":
        stats_subtool(database,args.metric)

    elif args.tool == "analyze":
        analyze_subtool(database,int(args.code))

    else:
        print("=== Unimpl ===");


__main__()
