import jsonpickle
import os

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

class InternalTxn:

    def __init__(self,txhash):
        self._id = txhash;

class ExternalTxn:

    def __init__(self,txhash):
        self._id = txhash;


class ContractInfo:
    def __init__(self,addr):
        self._addr = addr;
        self._exists = False;
        self._txs = 0;
        self._int_txs = 0;
        self._name = None;
        self._mined = 0;
        self._compiler_version = None;
        self._creator = None;
        self._creation_txn = None;
        self._optimized = None;
    @property
    def addr(self):
        return self._addr;


    @property
    def compiler_version(self):
        return self._compiler_version;


    @compiler_version.setter
    def compiler_version(self,value):
        self._compiler_version = value;



    @property
    def is_optimized(self):
        return self._optimized;

    @is_optimized.setter
    def is_optimized(self,value):
        self._optimized = value;

     
    @property
    def txs(self):
        return self._txs;

    @txs.setter
    def txs(self,value):
        self._txs = value;

    @property
    def int_txs(self):
        return self._int_txs;

    @int_txs.setter
    def int_txs(self,value):
        self._int_txs = value;

    @property
    def mined(self):
        return self._mined;

    @mined.setter
    def mined(self,address):
        self._mined = address;


    @property
    def name(self):
        return self._name;

    @name.setter
    def name(self,value):
        self._name = value;

    @property
    def mined(self):
        return self._mined;

    @mined.setter
    def mined(self,address):
        self._mined = address;


    @property
    def creator(self):
        return self._creator;

    @creator.setter
    def creator(self,address):
        self._creator = address;

    @property
    def exists(self):
        return self._exists;

    @property
    def creation_txn(self):
        return self._creation_txn;

    @creation_txn.setter
    def creation_txn(self,txn):
        self._creation_txn = txn;

    
    def read(self,dir):
        path=dir+"/src/"+self._addr;
        try:
            with open(path+"/info.json",'r') as f:
                self._exists = True;
                text = f.read();
                self = jsonpickle.decode(text);
        except IOError:
           return;

    def __str__(self):
        repr = "[c][d] ";
        repr += self.addr + "["+str(self.name)+"]\n";
        repr += "creator: "+str(self.creator)+"(txn="+str(self.creation_txn)+")\n";
        repr += "# txns: "+str(self.txns)+", internal: "+str(self.int_txns)+"\n"
        repr += "# mined: "+str(self.mined)+"\n";
        repr += "compiler: "+str(self.compiler_version)
        repr += "(optimized="+str(self.is_optimized)+")\n"
        return repr;

    def write(self,dir):
        path=dir+"/src/"+self._addr;
        if not os.path.exists(path):
            os.makedirs(path);

        with open(path+"/info.json",'w') as f:
            text = jsonpickle.encode(self);
            f.write(text);

class ContractSources:
    def __init__(self,addr):
        self._addr = addr;
        self._srccode = None;
        self._src_lang = None;
        self._bytecode = None;
        self._ctor_args = None;
        self._abi = None;

    @property
    def addr(self):
        return self._addr;

    @property
    def abi(self):
        return self._abi;

    @abi.setter
    def abi(self,value):
        self._abi = value;

    @property
    def bytecode(self):
        return self._bytecode;

    @bytecode.setter
    def bytecode(self,value):
        self._bytecode = value;

    @property
    def srccode(self):
        return self._srccode;

    @srccode.setter
    def srccode(self,value):
        self.detect_language();
        print("set source code, language is "+self.language);
        self._srccode = value;

    def detect_language(self):
        if(self.srccode == None):
            return;

        if self.srccode.find("//sol ") >= 0:
            self.language = "solidity";
        else:
            self.language = "serpent";

    @property
    def ctor_args(self):
        return self._ctor_args;

    @ctor_args.setter
    def ctor_args(self,value):
        self._ctor_args = value;

    @property
    def language(self):
        return self._src_lang;

    @language.setter
    def language(self,value):
        self._src_lang = value;

    def write(self,dir):
        path=dir+"/src/"+self._addr
        if not os.path.exists(path):
            os.makedirs(path);

        self.detect_language();
        if self.srccode != None and self.language == "solidity":
            with open(path+"/"+self._addr+".sol","w") as f:
                print("-> writing source - solidity");
                f.write(self.srccode);

        if self.srccode != None and self.language == "serpent":
            with open(path+"/"+self._addr+".sp","w") as f:
                print("-> writing source - serpent");
                f.write(self.srccode);

        if self.abi != None:
            with open(path+"/"+self.addr+".abi","w") as f:
                print("-> writing abi");
                f.write(self.bytecode);

        if self.bytecode != None:
            with open(path+"/"+self.addr+".byte","w") as f:
                print("-> writing bytecode");
                f.write(self.bytecode);

        if self.ctor_args != None:
            with open(path+"/"+self._addr+".ctor","w") as f:
                print("-> writing constructor args");
                f.write(self.ctor_args)

    def read(self,dir):
        path=dir+"/src/"+self._addr
        try:
            with open(path+"/"+self._addr+".sol") as f:
                self.source = f.read();
        except IOError:
            ();

        try:
            with open(path+"/"+self._addr+".sp") as f:
                self.source = f.read();
        except IOError:
            ();

        try:
            with open(path+"/"+self._addr+".byte") as f:
                self.bytecode = f.read();
        except IOError:
            ();

        try:
            with open(path+"/"+self._addr+".abi") as f:
                self.abi = f.read();
        except IOError:
            ();

        try:
            with open(path+"/"+self._addr+".ctor") as f:
                self._ctor_args = f.read();
        except IOError:
            ();

class ContractDetails:

    def __init__(self,addr):
        self._addr = addr;
        self._info = ContractInfo(addr);
        self._code = ContractSources(addr);
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
    def exists(self):
        return self._exists;

    def read(self,dir):
         self._info.read(dir);
         self._code.read(dir);
         self._exists = self._info.exists;

    def write(self,dir):
        self._info.write(dir);
        self._code.write(dir);
        
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
                for line in f:
                    ctr = jsonpickle.decode(line);
                    self.add_contract(ctr);
        except IOError:
            return;

    def write(self):
        with open(self._dbdir+"/"+self._dbfile,"a+") as f:
            for addr in self._contracts:
                contract = self._contracts[addr];
                text = jsonpickle.encode(contract);
                f.write(text+"\n");
            f.close();

    def write_details(self,addr):
        self._details[addr].write(self._dbdir);

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
            self._details[ctr.addr].read(self._dbdir);

    def add_page(self,i):
        self._pages.append(i);

