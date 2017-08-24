import eth
import sqlite3
from web3 import Web3, HTTPProvider, IPCProvider
import json, requests

class EthDebug:

    def __init__(self,loc,port):
        self.url = "http://%s:%d" % (loc,port)
        self.headers = {'content-type':'application/json'};

    def get_trace(self,txid):
        payload = {
            'method':"debug_traceTransaction",
            'params':["%s" % txid,{}],
            'jsonrpc':'2.0',
            'id':1
        }
        resp = requests.post(self.url,data=json.dumps(payload),headers=self.headers).json()
        return json.dumps(resp)

class Database:

    def __init__(self,dbpath):
        self.path = dbpath;
        self.dbfile = "%s/%s" % (self.path,"ethereum.db")
        self.conn = sqlite3.connect(self.dbfile)
        self.curs = self.conn.cursor()
        self.create_tables();

    def clear(self):
        drop_code = "DROP TABLE IF EXISTS code;"
        drop_contract= "DROP TABLE IF EXISTS contracts;"
        drop_txn = "DROP TABLE IF EXISTS txns;"
        self.curs.execute(drop_code);
        self.curs.execute(drop_contract);
        self.curs.execute(drop_txn);



    def create_tables(self):
        create_code = '''CREATE TABLE IF NOT EXISTS code (
            id text PRIMARY KEY,
            code integer NOT NULL
        );'''
        create_contracts = '''
        CREATE TABLE IF NOT EXISTS contracts (
            id text PRIMARY KEY,
            input text,
            code_id integer NOT NULL,
            FOREIGN KEY(code_id) REFERENCES code(id)
        );'''
        create_txns = '''
        CREATE TABLE IF NOT EXISTS txns (
            id text PRIMARY KEY,
            sender text NOT NULL,
            recip text NOT NULL,
            value integer NOT NULL,
            input text,
            code_id integer NOT NULL,
            trace JSON,
            FOREIGN KEY(recip) REFERENCES contracts(id),
            FOREIGN KEY(code_id) REFERENCES code(id)
        );
        '''
        self.curs.execute(create_code)
        self.curs.execute(create_contracts)
        self.curs.execute(create_txns)


    def get_code_usage(self):
        cmd = "SELECT code_id,COUNT(*) FROM txns GROUP BY code_id;"
        self.curs.execute(cmd)
        rows = self.curs.fetchall()
        return rows

    def get_code_dups(self):
        cmd = "SELECT code_id,COUNT(*) FROM contracts GROUP BY code_id;"
        self.curs.execute(cmd)
        rows = self.curs.fetchall()
        return rows

    def get_all_code(self):
        cmd = "SELECT id,code FROM code;"
        self.curs.execute(cmd)
        rows = self.curs.fetchall()
        return rows

    def has_source(self,source):
        source_id = hash(source)
        cmd = "SELECT * FROM code WHERE id=%d;" % source_id
        self.curs.execute(cmd)
        rows = self.curs.fetchall()
        return len(rows) > 0

    def has_contract(self,contract_id):
        cmd = "SELECT * FROM contracts WHERE id='%s';" % contract_id
        self.curs.execute(cmd)
        rows = self.curs.fetchall()
        return len(rows) > 0

    def has_txn(self,txnid):
        cmd = "SELECT * FROM txns WHERE id='%s'" % txnid
        self.curs.execute(cmd)
        rows = self.curs.fetchall()
        return len(rows) > 0

    def add_source(self,source):
        if self.has_source(source):
            return hash(source);

        source_id = hash(source)
        cmd = "INSERT INTO code VALUES(%s,'%s');" % (source_id,source)
        self.curs.execute(cmd)
        print("-> inserted source %s" % source_id)
        return source_id

    def add_contract(self,contractaddr,source,inp):
        source_id = self.add_source(source);
        if self.has_contract(contractaddr):
            return source_id;

        if inp != None:
            cmd = "INSERT INTO contracts VALUES('%s','%s',%s);" % (contractaddr,inp,source_id)
        else:
            cmd = "INSERT INTO contracts VALUES('%s',NULL,%s);" % (contractaddr,source_id)
        self.curs.execute(cmd)
        print("-> inserted contract %s" % contractaddr)
        return source_id

    def add_txn(self,txnid,sender,recipient,value,inp,code,trace):
        code_id = self.add_contract(recipient,code,None)
        if self.has_txn(txnid):
            return;

        cmd = '''
           INSERT INTO txns VALUES('%s','%s','%s',%d,'%s',%d,'%s');
        ''' % (txnid,sender,recipient,value,inp,code_id,str(trace))
        self.curs.execute(cmd)
        print("-> inserted txn %s" % txnid)


    def commit(self):
        self.conn.commit()

    def close(self):
        self.commit()
        self.conn.close()

class Scraper:

    def __init__(self,db,addr):
        self.bc = Web3(IPCProvider())
        self.bc_debug = EthDebug("127.0.0.1",8545)
        self.db = db;


    def trace_contract(self,txn):
        trace = self.bc_debug.get_trace(txn['hash'])
        return trace;

    def crawl_contract(self,txn,addr):
        contract = self.bc.eth.getCode(addr)
        if contract== "0x":
            return;

        if txn['value'] == 0:
            print("[constructor]")
            tr = self.trace_contract(txn)
            self.db.add_txn(txn['hash'],txn['from'],txn['to'],
               txn['value'],txn['input'],contract,tr)
        else:
            print("[invocation]")
            tr = self.trace_contract(txn)

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

        self.db.commit()

    def crawl(self,start_block,nblocks):
        for i in range(start_block,start_block+nblocks):
            print("=== Block %d ===" % i)
            self.crawl_block(i)
