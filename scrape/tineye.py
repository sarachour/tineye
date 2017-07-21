#!/usr/bin/python

from scan_index import ContractIndexScraper
from scan_code import ContractCodeScraper
from scan_txns import ContractTxnScraper
from analyze import CodeAnalyzer 

import sys,argparse
from visualize import *

def main():
    parser = argparse.ArgumentParser();

    subparsers = parser.add_subparsers(dest="subparser_name");

    # general index parser
    scan = subparsers.add_parser('scan');
    scan.add_argument("-n","--num-requests");
    scan.add_argument("-w","--what");
    scan.add_argument("-c","--contract");


    decode = subparsers.add_parser('decode');
    decode.add_argument("-c","--contract");
    decode.add_argument("-w","--what");
    decode.add_argument("-d","--dups");
    decode.add_argument("-o","--output");

    look = subparsers.add_parser('inspect');
    look.add_argument("-w","--what");
    look.add_argument("-k","--kind");
    look.add_argument("-o","--output");

    scrape_txns = subparsers.add_parser('scrape-txns');

    args = parser.parse_args(sys.argv[1:]);
    if(args.subparser_name == "scan" and args.what == "index"):
        npages = int(args.num_requests);
        scraper = ContractIndexScraper();
        scraper.get_pages(npages);
        scraper.db.write();

    elif(args.subparser_name == "scan" and args.what == "txns"):
        scraper = ContractTxnScraper();
        if(args.contract != None):
            scraper.scrape_txns_of_contract(args.contract);
        else:
            ncontracts= int(args.num_requests);
            scraper.scrape_txns_of_contracts(ncontracts);


    elif(args.subparser_name == "scan" and args.what == "code"):
        scraper = ContractCodeScraper();
        if(args.contract != None):
            scraper.scrape_code_of_contract(args.contract);
        else:
            ncontracts= int(args.num_requests);
            scraper.scrape_code_of_contracts(ncontracts);

    elif(args.subparser_name == "decode"):
        analyzer= CodeAnalyzer();
        analyzer.execute(args.what,args.output,args.dups,args.contract);

    elif(args.subparser_name == "inspect" and args.what == "summary"):
        visualizer = SummaryVis();
        viskind = args.kind;
        visout = args.output;
        visualizer.execute(viskind,visout);

    elif(args.subparser_name == "inspect" and args.what == "duplicates"):
        deduper = CodeAnalyzer();
        output = args.output;
        deduper.find_dups();
        deduper.report_dups(output);

    else:
        print("unimplemented");
        sys.exit(1);

if __name__ == "__main__":
    main();
