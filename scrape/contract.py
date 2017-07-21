import jsonpickle
import os
from transaction import *
from code import *


class Contract():
    def __init__(self,addr):
        self._addr = addr;

    @property
    def addr(self):
        return self._addr;

    @property
    def name(self):
        return self._name;

    @property
    def name(self,value):
        self._name = value;

    @property
    def url(self, value):
        self._url = value;

    @property
    def url(self):
        return self._url;

    @property
    def txs(self,value):
        self._txs = value;

    @property
    def pctmarket(self,value):
        self._pctmarket = value;

    @property
    def wallet(self,value):
        self._wallet = value;

    def __str__(self):
        repr = "[c] "
        repr += self.addr+" ["+self.name+"]\n"
        repr += self.url+"\n"
        repr += "wallet:"+str(self.wallet)+"\n"
        repr += "txs:"+str(self.txs)+"/pct-market:"+str(self.pctmarket)+"\n"
        return repr

class ContractDetails:

    def __init__(self,addr):
        self._addr = addr;
        self._info = ContractInfo(addr);
        self._code = ContractSources(addr);
        self._txns = ContractTxns(addr);
        self._exists = False;

    @property
    def addr(self):
        return self._addr;

    @property
    def code(self):
        return self._code;
    
    @property
    def info(self):
        return self._info;

    @property
    def txns(self):
        return self._txns;

    @property
    def code_exists(self):
        return self._code_exists;

    @property
    def txns_exists(self):
        return self._txns_exists;

    def read(self,dir):
         self._info.read(dir);
         self._code.read(dir);
         self._txns.read(dir);
         self._code_exist = self._info.exists;
         self._txns_exist = self._txns.exists;

    def write_code(self,dir):
        self._info.write(dir);
        self._code.write(dir);

    def write_txns(self,dir):
        self._txns.write(dir);

class ContractDatabase:
    def __init__(self):
        self._pages = [];
        self._contracts = {};
        self._details = {};
        self._dbdir = "db";
        self._dbfile = "index.json"

    def read(self):
        try:
            with open(self._dbdir+"/"+self._dbfile,"r") as f:
                currline = 0;
                for line in f:
                    if currline % 5000 == 0:
                        print(str(currline));

                    ctr = jsonpickle.decode(line);
                    self.add_contract(ctr);
                    currline += 1;
        except IOError:
            return;

    def write(self):
        with open(self._dbdir+"/"+self._dbfile,"a+") as f:
            for addr in self._contracts:
                contract = self._contracts[addr];
                text = jsonpickle.encode(contract);
                f.write(text+"\n");
            f.close();

    def write_txns(self,addr):
        self._details[addr].write_txns(self._dbdir);

    def write_code(self,addr):
        self._details[addr].write_code(self._dbdir);

    def read_details(self,addr):
        self._details[addr].read(self._dbdir);

    @property
    def contracts(self):
        return self._contracts;

    @property
    def pages(self):
        return self._pages;

    def details(self,addr):
        return self._details[addr];

    def add_contract(self,ctr):
        if ctr.addr in self._contracts:
            print("> contract already exists...");
            return;
        else:
            self._contracts[ctr.addr] = ctr;
            self._details[ctr.addr] = ContractDetails(ctr.addr);
            #self._details[ctr.addr].read(self._dbdir);

    def add_page(self,i):
        self._pages.append(i);

