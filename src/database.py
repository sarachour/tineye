from eth import Trace
import sqlite3
from web3 import Web3, HTTPProvider, IPCProvider
import json, requests
import hashlib

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
            code text NOT NULL
        );'''
        create_contracts = '''
        CREATE TABLE IF NOT EXISTS contracts (
            id text PRIMARY KEY,
            code_id text NOT NULL,
            FOREIGN KEY(code_id) REFERENCES code(id)
        );'''
        create_txns = '''
        CREATE TABLE IF NOT EXISTS txns (
            id text PRIMARY KEY,
            sender text NOT NULL,
            recip text NOT NULL,
            value integer NOT NULL,
            input text,
            code_id text NOT NULL,
            is_ctor boolean,
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


    def get_code(self,codeid):
        cmd = "SELECT code FROM code where id='%s';" % codeid
        self.curs.execute(cmd)
        rows = self.curs.fetchall()
        code = rows[0]
        return code

    def get_traces(self,codeid):
        cmd = "SELECT id,sender,recip,input,is_ctor FROM txns where code_id='%s';" % codeid
        self.curs.execute(cmd)
        rows = self.curs.fetchall()
        debugger = EthDebug("127.0.0.1",8545)
        traces = []
        for (ident,sender,recip,inp,is_ctor) in rows:
            trace = json.loads(debugger.get_trace(ident))
            if "error" in trace:
                print(trace["error"])
                continue;

            trace_obj = Trace(ident,sender,recip,inp,trace['result']['structLogs'],is_ctor)
            traces.append(trace_obj)

        return traces

    def get_all_code(self):
        cmd = "SELECT id,code FROM code;"
        self.curs.execute(cmd)
        rows = self.curs.fetchall()
        return rows

    def code_to_id(self,code):
        hash_obj = hashlib.sha1(code)
        hash_dig = hash_obj.hexdigest()
        return hash_dig

    def has_source(self,source):
        source_id = self.code_to_id(source)
        cmd = "SELECT * FROM code WHERE id='%s';" % source_id
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
        source_id = self.code_to_id(source)
        if self.has_source(source):
            return source_id;

        cmd = "INSERT INTO code VALUES('%s','%s');" % (source_id,source)
        self.curs.execute(cmd)
        print("-> inserted source %s" % source_id)
        return source_id

    def add_contract(self,contractaddr,source):
        source_id = self.add_source(source);
        if self.has_contract(contractaddr):
            return source_id;

        cmd = "INSERT INTO contracts VALUES('%s','%s');" % (contractaddr,source_id)
        self.curs.execute(cmd)
        print("-> inserted contract %s" % contractaddr)
        return source_id

    def add_txn(self,txnid,sender,recipient,value,inp,code,is_ctor):
        code_id = self.add_contract(recipient,code)
        if self.has_txn(txnid):
            return;

        is_ctor_val = 0;
        if is_ctor:
            is_ctor_val = 1

        cmd = '''
           INSERT INTO txns VALUES('%s','%s','%s',%d,'%s','%s',%d);
        ''' % (txnid,sender,recipient,value,inp,code_id,is_ctor_val)
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
        self.db = db;



    def crawl_contract(self,txn,addr):
        contract = self.bc.eth.getCode(addr)
        if contract== "0x":
            return;

        if txn['value'] == 0:
            print("   [constructor]")
            self.db.add_txn(txn['hash'],txn['from'],txn['to'],
               txn['value'],txn['input'],contract,True)
        else:
            print("   [invocation]")
            self.db.add_txn(txn['hash'],txn['from'],txn['to'],
               txn['value'],txn['input'],contract,False)

    def crawl_block(self,bnum):

        blk = self.bc.eth.getBlock(bnum)
        for txnhash in blk['transactions']:
            txn = self.bc.eth.getTransaction(txnhash)
            if callable(txn):
                continue;

            print("-> %s" % txnhash)
            self.crawl_contract(txn,txn['to'])
            self.crawl_contract(txn,txn['from'])

        self.db.commit()

    def crawl(self,start_block,nblocks):
        for i in range(start_block,start_block+nblocks):
            print("=== Block %d ===" % i)
            self.crawl_block(i)
