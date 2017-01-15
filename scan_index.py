#!/usr/bin/python
from bs4 import BeautifulSoup
import cfscrape
from contract import *

class ContractIndexScraper:

    def __init__(self):
        self._db = ContractDatabase();
        self._scraper = cfscrape.create_scraper();
        self._pages = [];

    @property
    def db(self,value):
        self._db = value;

    @property
    def db(self):
        return self._db

    def get_pages(self,n):
        for i in range(1,n):
            self.get_page(i);

    def get_page(self,i):
        if(i in self._pages):
            print("page already scraped.");

        self._pages.append(i);

        url = "https://etherscan.io/accounts/c/"+str(i);
        print("====> Retrieving Page "+str(i))
        page = self._scraper.get(url).content;
        dom = BeautifulSoup(page);

        for row in dom.select('tr'):
            children = row.findChildren(recursive=False);
            if(len(children) < 5):
                print(">unrecognized row format.. skipping..")
                continue;
            contract_addr = children[1];
            contract_wallet = children[2];
            contract_pctmarket = children[3];
            contract_transactions = children[4];

            print("=== Addr ===")
            a_elems = contract_addr.select('a');
            if(len(a_elems) == 0):
                print(">contract field doesn't have address..skipping..")
                continue;
            a_elem = a_elems[0];
            el = Contract(str(a_elem.contents[0]))
            el.url = str("https://etherscan.io"+a_elem['href']);
            if(len(contract_addr.contents) >= 4):
                el.name = str(contract_addr.contents[3]).strip().replace("(","").replace(")","");
            else:
                el.name = "Unknown"

            print("=== Wallet ===")
            if(len(contract_wallet.contents) == 3):
                ldec = str(contract_wallet.contents[0]).replace(",","");
                rdec = str(contract_wallet.contents[2]).split(" ")[0];
                dec = ldec + "." + rdec;
                print(dec);
                el.wallet = float(dec);
            elif(len(contract_wallet.contents) == 1):
                dec = contract_wallet.contents[0].split(" ")[0].replace(",","");
                print(dec);
                el.wallet = float(dec);
            else:
                print(contract_wallet.prettify());
                raise("unknown wallet format.")

            print("=== Pct Market==")
            try:
                el.pctmarket = float(contract_pctmarket.string.replace("%",""))
            except e:
                print("error: could not parse pct-market:<"+contract_pctmarket.string+">");

            print("=== Transactions ==")
            print(contract_transactions.string);
            el.txs = int(contract_transactions.string)
            print("=== Repr ==")
            print(el);
            self._db.add_contract(el);


