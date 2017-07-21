#!/usr/bin/python
from bs4 import BeautifulSoup
import cfscrape
from contract import *


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
        page = self._scraper.get(contract.url+"#code").content;
        dom = BeautifulSoup(page, "html.parser");

        print(addr);
        details = self.db.details(addr);
        # extract meta info
        tables = dom.select("table");

        #get the number of mined blocks
        row = self.find_row_that_contains(tables,"Mined");
        if row != None:
            self.db.details(addr).info.mined = \
                self.extract_int(self.get_contents(row.select("td")[1],""))

        #get compiler information
        row = self.find_row_that_contains(tables,"Optimization Enabled:");
        if row != None:
            is_optimized = self.get_contents(row.select("td")[1],"");
            if is_optimized == "Yes":
                details.info.is_optimized = True
            else:
                details.info.is_optimized = False
        
        row = self.find_row_that_contains(tables,"Contract Name:");
        if row != None:
            details.info.name= self.get_contents(row.select("td")[1],"").strip();

        row = self.find_row_that_contains(tables,"Compiler Version:");
        if row != None:
            details.info.compiler_version = self.get_contents(row.select("td")[1],"").strip();

        row = self.find_row_that_contains(tables,"No Of Transactions:");
        #get transactions
        if row != None:
            spans = row.select("span");
            details.info.txns = \
                self.extract_int(self.get_contents(spans[0],""));
            if(len(spans) > 1):
                details.info.int_txns = \
                    self.extract_int(self.get_contents(spans[1],""));
            else:
                details.info.int_txns = 0

        row = self.find_row_that_contains(tables,"Contract Creator")
        if row != None:
            links = row.select("a");
            #get the creater info
            details.info.creator = self.get_contents(links[0],"");
            details.info.creation_txn = self.get_contents(links[1],"");

        print("=== Details ===");
        print(str(details.info));

        code_divs = dom.select("pre");
        # if only one code snippt, it's a code div.
        print("> fetching details for: "+addr);
        if len(code_divs) == 1:
            print("  : found bytecode");
            details.code.bytecode = self.get_contents(code_divs[0],"");

        elif len(code_divs) == 2:
            details.code.bytecode = self.get_contents(code_divs[0],"");
            details.code.abi = self.get_contents(code_divs[1],"");

        elif len(code_divs) == 3:
            print("  : found bytecode,abi & source");
            details.code.srccode = self.get_contents(code_divs[0],"\n");
            details.code.abi = self.get_contents(code_divs[1],"");
            details.code.bytecode = self.get_contents(code_divs[2],"");

        elif len(code_divs) == 4:
            details.code.srccode = self.get_contents(code_divs[0],"\n");
            details.code.abi = self.get_contents(code_divs[1],"");
            details.code.bytecode = self.get_contents(code_divs[2],"");
            print(code_divs[3].prettify())
            details.code.ctor_args = self.get_ctor_arg_contents(code_divs[3]);

        else:
            for pre in code_divs:
                print(pre.prettify());
                print("scrape please: "+addr+" -> "+str(len(code_divs)));
            return;

        self.db.write_code(addr);

    def scrape_code_of_contracts(self,nscrapes):
        scrape_count = 0;
        for addr in self.db.contracts:
            contract = self.db.contracts[addr];
            if(self.db.details(addr).info.exists == False):
                self.scrape_code_of_contract(addr);
                scrape_count += 1;
                if(scrape_count > nscrapes):
                    return;

            else:
                ()

# 4 args:  
