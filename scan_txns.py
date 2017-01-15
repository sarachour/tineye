#!/usr/bin/python
from bs4 import BeautifulSoup
import cfscrape
from contract import *
import sys


class ContractCodeScraper:

    def __init__(self):
        self._db = ContractDatabase();
        self._scraper = cfscrape.create_scraper();
        self._pages = [];
        self._db.read();

    @property
    def db(self,value):
        self._db = value;

    @property
    def db(self):
        return self._db

    def get_ctor_arg_contents(self,arg):
        text = arg.contents[0];
        dec = text.split("\s")[0];
        return dec;

    def get_contents(self,el,delim):
        strcontents = map(lambda x: (x.string).encode('utf-8'), el.contents);
        repr = delim.join(strcontents)
        return repr;

    def extract_int(self,v):
        numbers = [int(s) for s in v.split() if s.isdigit()]
        return numbers[0]

    def find_row_that_contains(self,tbls,snippet):
        for tbl in tbls:
            for row in tbl.select("tr"):
                text = row.prettify();
                if snippet in text:
                    return row;
        return None;

    def scrape_code_of_contract(self,addr):
        contract = self.db.contracts[addr];
        url = "https://etherscan.io/txs?a="+addr;

        page = self._scraper.get(url).content;
        dom = BeautifulSoup(page, "html.parser");
        tables = dom.select("table")
        for table in tables:
            print(table.prettify())

        sys.exit(0);
        txns = self.db.txns(addr);
        self.db.write_txns(addr);

    def scrape_code_of_contracts(self,nscrapes):
        scrape_count = 0;
        for addr in self.db.contracts:
            contract = self.db.contracts[addr];
            if(self.db.txns(addr).exists == False):
                self.scrape_txns_of_contract(addr);
                scrape_count += 1;
                if(scrape_count >= nscrapes):
                    return;

            else:
                ()

