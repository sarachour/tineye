import jsonpickle
import os
from time import strftime

class InternalTransaction:
    def __init__(self,name):
        self._name = name;
        self.sender = self.to = self.value = None;

    @property
    def name(self):
        return self._name;

    @property
    def to(self):
        return self._to;

    @to.setter
    def to(self,v):
        self._to = v;

    @property
    def sender(self):
        return self._sender;

    @sender.setter
    def sender(self,v):
        self._sender = v;

    @property
    def value(self):
        return self._value;

    @value.setter
    def value(self,v):
        self._value = v;

    def __str__(self):
        repr = "[itx] "+str(self.name)+" ("+str(self.value)+" Ether)\n"
        repr += str(self.sender)+" -> "+str(self.to);
        return repr;
        


class Transaction:

    def __init__(self,hashv):
        self._txhash = hashv;
        self._internal = {};
        self.value = None;
        self.confirms = None;
        self.failed = False;
        self.reason = None;
        self.gas = self.gas_used = self.gas_price = None;
        self.to = self.sender = None;
        self.time = self.args = None;

    @property
    def reason(self):
        return self._reason;

    @reason.setter
    def reason(self, v):
        self._reason = v;


    @property
    def failed(self):
        return self._failed;

    @failed.setter
    def failed(self, v):
        self._failed = v;

    @property
    def txhash(self):
        return self._txhash;

    @property
    def kind(self):
        return self._kind;

    @kind.setter
    def kind(self,v):
        self._kind = v;


    @property
    def block(self):
        return self._block;

    @block.setter
    def block(self,value):
        self._block = value;

    @property
    def value(self):
        return self._value;

    @value.setter
    def value(self,value):
        self._value = value;

    @property
    def to(self):
        return self._to;

    @to.setter
    def to(self,v):
        self._to = value;

    @property
    def sender(self):
        return self._sender;

    @sender.setter
    def sender(self,v):
        self._sender = v;

    @property
    def time(self):
        return self._time;

    @time.setter
    def time(self,v):
        self._time = v;

    @property
    def gas(self):
        return self._gas;

    @gas.setter
    def gas(self,v):
        self._gas = v;

    @property
    def gas_used(self):
        return self._gas_used;

    @gas_used.setter
    def gas_used(self,v):
        self._gas_used = v;

    @property
    def gas_price(self):
        return self._gas_price;

    @gas_price.setter
    def gas_price(self,v):
        self._gas_price = v;

    @property
    def confirms(self):
        return self._confirms;

    @confirms.setter
    def confirms(self,v):
        self._confirms = v;

    @property
    def args(self):
        return self._args;

    @args.setter
    def args(self,v):
        self._args = v;

    def add_internal_txn(self,txn):
        self._internal[txn.name] = txn;


    def __str__(self):
        repr = "[tx]";
        repr += self.txhash + "("+str(self.confirms)+" confirms)\n";
        if self.failed:
            repr += "[FAILED] "+self.reason+"\n";
        repr += "time: " + strftime("%b/%d/%Y %H:%M:%S %Z",self.time) + "\n";
        repr += "value: "+ str(self.value) + "\n"
        repr += str(self.sender) + "->" + str(self.to) + "\n"
        repr += "gas: "+str(self.gas_used) + "/" + str(self.gas);
        repr += " ("+str(self.gas_price)+" ether/gas)\n";
        repr += "args:\n";
        repr += self.args +"\n";
        repr += "-- Internal Transactions --\n"
        for k in self._internal:
            itxn = self._internal[k];
            repr += " "+str(itxn)+"\n";


        return repr

class ContractTxns:

    def __init__(self,addr):
        self._addr = addr;
        self._exists = False;
        self._txns = {};

    def add_txn(self,txn):
        self._txns[txn.txhash] = txn;

    def txn(self,txhash):
        return self._txns[txn.txhash];

    @property
    def addr(self):
        return self._addr;

    @property
    def exists(self):
        return self._exists;


    def write(self,dir):
        path = dir+"/txns/"+self._addr;
        if not os.path.exists(path):
            os.makedirs(path);

        with open(path+"/txns.json",'w') as f:
            self._exists = True;
            text = jsonpickle.encode(self);
            f.write(text);

    def read(self,dir):
        path = dir+"/txns/"+self._addr;
        if not os.path.exists(path):
            self._exists = False;
        try:
            with open(path+"/txns.json",'r') as f:
                self._exists = True;
                text = f.read();
                self = jsonpickle.decode(text);
        except IOError:
            self._exists = False;
            return;
