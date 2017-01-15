import jsonpickle
import os

class IntTransaction:
    def __init__(self,name):
        self._name;

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
        return self._sender = v;

    @property
    def value(self):
        return self._value;

    @value.setter
    def value(self,v):
        return self._value = v;


class Transfer:

    def __init__(self,recip,val):
        self._to = recip;
        self._value = val;

    @property
    def value(self):
        return self._value;

    @property
    def to(self):
        return self._to;

class Transaction:

    def __init__(self,hashv):
        self._txhash = hashv;
        self._internal = {};
        self._transfers = {};

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
    def input(self):
        return self._input;

    @input.setter
    def input(self,v):
        self._input = v;

    def add_int_txn(self,txn):
        self._internal[txn.name] = txn;

    def add_recip(self,tfr):
        self._transfers[tfr.to] = tfr;

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

    def read(self,dir):
        path = dir+"/txns/"+self._addr;
