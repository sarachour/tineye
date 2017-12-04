import sys
import argparse
from database import Database,Scraper
from paths import paths
from retina import Retina
from decompiler.decompile import disasm
import os

def analyze_subtool(database,codeid):

    base_dir = "data/%s" % codeid;
    trace_dir = "%s/traces" % base_dir;

    if not os.path.exists(trace_dir):
        os.makedirs(trace_dir)


    code_file = lambda x : "%s/%s" % (base_dir,x)
    trace_file = lambda x : "%s/%s" % (trace_dir,x)

    print("=== Collecting Code ===")
    source = database.get_code(codeid)

    f = open(code_file("code.byte"),'w')
    f.write(source)
    f.close()

    f = open(code_file("code.byte.pretty"),'w')
    f.write(disasm(source))
    f.close()

    decompiled = decompile(source)
    f = open(code_file("code.ir"),'w')
    f.write(decompiled.dump());
    f.close()

    f = open(code_file("code.ir.pretty"),'w')
    f.write(decompiled.pretty());
    f.close()

    return;


    print("=== Collecting Traces ===")
    txns = database.get_traces(codeid)
    for trace in txns:
        f = open(trace_file("%s.trace" % trace.txn),'w')
        f.write(trace.dump())
        f.close()

def stats_subtool(database,metric):
    if metric == "usage":
        results = database.get_code_usage()
        print("=== Number of Traces per Contract ===")
        for (ident,ntxns) in results:
            print("%s\t%d" % (ident,ntxns))

    elif metric == "size":
        results = database.get_all_code()
        print("=== Code Size ===")
        for (ident,code) in results:
            print("%s\t%d" % (ident,len(code)))

    elif metric == "dups":
        results = database.get_code_dups()
        print("=== Code Dups ===")
        for (ident,dups) in results:
            print("%s\t%d" % (ident,dups))

def __main__():
    parser = argparse.ArgumentParser(description='Analyze smart contracts.')

    subparsers = parser.add_subparsers(help='perform various operations over the blockchain.',
                                       dest='tool')

    # load all the unique contracts.
    p_bootstrap = subparsers.add_parser('download',
                                     help='download the contracts from the blockchain.')

    p_bootstrap.add_argument('--start', required=True,help='the starting block')
    p_bootstrap.add_argument('--n', required=True,help='the number of blocks to download')
    # trace all the executions for a unique contract
    p_analyze = subparsers.add_parser('traces',
                                      help='given the id of the program, download all of the traces.')

    p_analyze.add_argument('--prog', help='the identifier of the program to analyze')

    # trace all the executions for a unique contract
    p_stats= subparsers.add_parser('stats',
                                     help='produce the trace stats for the blockchain.')

    p_stats.add_argument('--metric',help='the statistic to produce')
    # load all the unique contracts.
    p_clean = subparsers.add_parser('clean',
                                     help='load unique contracts into database. [usage/size/dups].')


    args = parser.parse_args()

    database = Database(paths.db_dir);
    if args.tool == "download":
        print("=== Retrieving Data From The Blockchain ===");
        scraper = Scraper(database,"..")

        scraper.crawl(int(args.start), int(args.n))
        database.close()

    elif args.tool == "clean":
        print("=== Clearing ===");
        database.clear()
        database.close()

    elif args.tool == "stats":
        stats_subtool(database,args.metric)

    elif args.tool == "traces":
        analyze_subtool(database,args.code)

    else:
        raise Exception("unknown command: %s. try the --help tag." % args.tool)

__main__()
