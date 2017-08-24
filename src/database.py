import eth
import sqlite3
from web3 import Web3, HTTPProvider, IPCProvider

class Database:

    def __init__(self,dbpath):
        self.path = dbpath;
        self.dbfile = "%s/%s" % (self.path,"ethereum.db")
        self.conn = sqlite3.connect(self.dbfile)
        self.curs = self.conn.cursor()


    def clear(self):
        print("unimpl")

    def close(self):
        self.conn.close()

class Scraper:

    def __init__(self,db,addr):
        self.bc = Web3(IPCProvider())
        self.db = db;


    def crawl_contract(self,txn,addr):
        contract = self.bc.eth.getCode(addr)
        if contract== "0x":
            return;

        if txn['value'] == 0:
            print("[constructor]")

        else:
            print("[invocation]")

    def crawl_block(self,bnum):

        blk = self.bc.eth.getBlock(bnum)
        for txnhash in blk['transactions']:
            txn = self.bc.eth.getTransaction(txnhash)
            if callable(txn):
                continue;

            print("============")
            print("sender: %s" % txn['from'])
            print("receiver: %s" % txn['to'])
            print("value: %d" % txn['value'])
            print("input: %s" % txn['input'])

            self.crawl_contract(txn,txn['to'])
            self.crawl_contract(txn,txn['from'])

    def crawl(self):
        base = 1000*1000*3
        for i in range(base+2,base+10):
            print("=== Block %d ===" % i)
            self.crawl_block(i)
