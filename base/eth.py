import web3
import json

class Trace:

    def __init__(self,txnid,sender,recip,args,trace,is_ctor):
        self.trace = trace;
        self.txn = txnid;
        self.sender = sender;
        self.recip = recip;
        self.is_ctor = False
        if is_ctor == 1:
            self.is_ctor = True

        input_str = args.split("0x")[1];
        # first eight bytes is function entry point
        self.entry_point = input_str[0:8];
        self.args = input_str[9:];


    def dump(self):
        js = {
            'trace':self.trace,
            'txn':self.txn,
            'from':self.sender,
            'to':self.recip,
            'ctor':self.is_ctor,
            'entry_point':self.entry_point,
            'args': self.args
        }
        return json.dumps(js)
