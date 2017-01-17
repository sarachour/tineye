#!/usr/bin/python
from bs4 import BeautifulSoup
import cfscrape
from contract import *
import sys
import re
import time

class ContractTxnScraper:

    def __init__(self):
        self._db = ContractDatabase();
        self._scraper = cfscrape.create_scraper();
        self._db.read();
        self._pages = [];

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

    def none_to_str(self,x):
        if x == None:
            return "";
        else:
            return x;

    def get_contents(self,el,delim=""):
        strcontents = map(lambda x: self.none_to_str((x.string)).encode('utf-8'), el.contents);
        repr = delim.join(strcontents)
        return repr;

    def extract_int(self,vstr):
        v = vstr.strip();
        numbers = [int(s) for s in v.split() if s.isdigit()]
        return numbers[0]

    def isfloat(self,v):
        try:
            float(v)
            return True
        except ValueError:
            return False

    def extract_float(self,vstr):
        v = vstr.strip();
        numbers = [float(s) for s in v.split() if self.isfloat(s)]
        return numbers[0]

    def find_table_that_contains(self,pars,snippet):
        for par in pars:
            tbls = par.select("table");
            for tbl in tbls:
                text = tbl.prettify();
                if text.find(snippet) != -1:
                    return tbl;
        return None;

    def find_row_that_contains(self,tbls,snippet):
        for tbl in tbls:
            rows = tbl.select("tr");
            for row in rows:
                text = row.prettify();
                if text.find(snippet) != -1:
                    return row;
        return None;

    def get_value_from_row_that_contains(self,tbls,snippet):
        row = self.find_row_that_contains(tbls,snippet);
        if row != None:
            return row.select("td")[1]
        else:
            return None;

    def scrape_txn_details(self,txn):
        url = "https://etherscan.io/tx/" + txn.txhash;
        print(url);
        page = self._scraper.get(url).content;
        dom = BeautifulSoup(page, "html.parser");
        tables = dom.select("table");
        toplevel = [dom];


        height = self.get_value_from_row_that_contains(tables,"Block Height");
        if height != None:
            txn.confirms = self.extract_int(self.get_contents(height.select("span")[0]))

        timestamp = self.get_value_from_row_that_contains(tables,"TimeStamp :");
        if timestamp != None:
            tsstring = re.search('\([^\)]+\)',self.get_contents(timestamp)).group(0);
            timev = time.strptime(tsstring,'(%b-%d-%Y %I:%M:%S %p +%Z)')
            txn.time = timev;

        fromfld = self.get_value_from_row_that_contains(toplevel,"From:");
        if fromfld != None:
            txn.sender = self.get_contents(fromfld.select("a")[0])

        tofld = self.get_value_from_row_that_contains(toplevel,"To:");
        if tofld != None:
            txn.to = self.get_contents(fromfld.select("a")[0]);

        value = self.get_value_from_row_that_contains(toplevel,"Value:");
        if value != None:
            valuestr = self.get_contents(value.select("span")[0]).replace(",","")
            txn.value = self.extract_float(valuestr);

        gas = self.get_value_from_row_that_contains(toplevel,"Gas:");
        if gas != None:
            txn.gas = self.extract_int(self.get_contents(gas.select("span")[0]));

        gasprice = self.get_value_from_row_that_contains(toplevel,"Gas Price:");
        if gasprice != None:
            result = self.get_contents(gasprice.select("span")[0]);
            txn.gas_price = self.extract_float(result);

        failure = self.get_value_from_row_that_contains(toplevel,"Error encountered during contract execution");
        if failure != None:
            txn.reason = failure.select("b")[0];
            txn.failed = True

        gasused = self.get_value_from_row_that_contains(toplevel,"Gas Used By Transaction:");
        if gasused != None:
            txn.gas_used = self.extract_int(self.get_contents(gasused.select("span")[0]));

        inp = self.get_value_from_row_that_contains(toplevel,"Input Data:");
        if inp != None:
            txn.args = self.get_contents(inp.select("textarea")[0]);

        icall_table = self.find_table_that_contains(dom.find_all("div",attrs={"id":"internal"}),"Type_TraceAddress");
        if icall_table != None:
            icall_rows = icall_table.select("tr")[1:]
            for row in icall_rows:
                cols = row.select("td");
                # get identifier
                ident = self.get_contents(cols[0]);

                itxn = InternalTransaction(ident);
                itxn.sender = self.get_contents(cols[1])
                itxn.to = self.get_contents(cols[3])
                valstr = self.get_contents(cols[4]).replace(",","");
                itxn.value = self.extract_float(valstr);
                txn.add_internal_txn(itxn);
                

        return txn;

    def scrape_txns_of_contract(self,addr):
        gurl = "https://etherscan.io/txs?a="+addr;
        txns = self.db.details(addr).txns;
    
        print(": "+gurl);
        npages = 500;
        try:
            for page in range(1,npages):
                print("=== Page "+str(page)+" ===")
                url = "https://etherscan.io/txs?a="+addr+"&p="+str(page);
                page = self._scraper.get(url).content;
                dom = BeautifulSoup(page, "html.parser");
                tables = dom.select("tbody");

                for row in tables[0].select("tr"):
                    cols = row.select("td");
                    txhash = self.get_contents(cols[0],"");
                    print("-> "+txhash);
                    txn = Transaction(txhash);
                    self.scrape_txn_details(txn);
                    txns.add_txn(txn);
        except Exception:
            ()

        self.db.write_txns(addr);

    def scrape_txns_of_contracts(self,nscrapes):
        scrape_count = 0;
        for addr in self.db.contracts:
            contract = self.db.contracts[addr];
            self.db.read_details(addr);
            if(self.db.details(addr).txns.exists == False):
                print("[scraping] "+str(addr))
                self.scrape_txns_of_contract(addr);
                scrape_count += 1;
                if(scrape_count >= nscrapes):
                    return;

            else:
                print("[read] "+str(addr))
                ()

