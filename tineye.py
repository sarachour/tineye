import sys
import argparse
from base.database import Database,Scraper
from base.paths import paths
from retina import Retina
from decompiler.decompile import disasm,decompile,reconstruct
import os

def analyze_subtool(database,codeid,do_decompile=True,do_reconstruct=True,do_traces=True):
    if codeid == None:
        raise Exception("must specify a program id.")

    base_dir = "%s/%s" % (paths.prog_dir,codeid);
    trace_dir = "%s/traces" % base_dir;

    print("src-dir: %s" % base_dir)
    print("trace-dir: %s" % trace_dir)

    if not os.path.exists(trace_dir):
        os.makedirs(trace_dir)


    code_file = lambda x : "%s/%s" % (base_dir,x)
    trace_file = lambda x : "%s/%s" % (trace_dir,x)

    print("=== Getting Code ===")
    source = database.get_code(codeid)

    f = open(code_file("code.byte"),'w')
    f.write(source)
    f.close()

    print("=== Disassembling ===")
    f = open(code_file("code.byte.pretty"),'w')
    f.write(str(disasm(source)))
    f.close()

    if do_decompile:
        print("=== Decompiling ===")
        decompiled = decompile(source)

        f = open(code_file("code.ir"),'w')
        f.write(decompiled.pretty());
        f.close()

        if do_reconstruct:
            reconstructed = reconstruct(decompiled)

            f = open(code_file("code.recon"),'w')
            f.write(reconstructed.pretty());
            f.close()


    if do_traces:
        print("=== Retrieving Traces ===")
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
    p_analyze = subparsers.add_parser('analyze',
                                      help='given the id of the program, download all of the traces.')

    p_analyze.add_argument('--prog', help='the identifier of the program to analyze')
    p_analyze.add_argument('--decompile', action='store_true', default=False,
                           help='decompile the program into entry-points and code segments.')
    p_analyze.add_argument('--reconstruct', action='store_true', default=False,
                           help='reconstruct the decompiled program.')
    p_analyze.add_argument('--trace', action='store_true', default=False,
                           help='retrieve the program traces.')


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

    elif args.tool == "analyze":
        do_decompile=args.decompile
        do_reconstruct=args.reconstruct
        do_traces=args.trace
        analyze_subtool(database,args.prog,
                        do_decompile=do_decompile,
                        do_reconstruct=do_reconstruct,
                        do_traces=do_traces)

    else:
        raise Exception("unknown command: %s. try the --help tag." % args.tool)

__main__()
