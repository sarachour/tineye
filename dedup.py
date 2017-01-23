from contract import *

class DedupCode:

    def __init__(self):
        self._db = ContractDatabase();
        self._db.read();
        self.groups = {};
        self.addrs = [];
        self.n = 0;

    @property
    def db(self):
        return self._db

    def same(self,code1,code2):
        if code1 == None and code2 == None:
            return True;
        elif code1 == None or code2 == None:
            return False;

        if code1.strip() == code2.strip():
            return True;
        else:
            return False;

    def find_dups(self):
        for addr in self.db.contracts:
            self.db.read_details(addr);
            src = self.db.details(addr).code.bytecode

            # for each existing gorup
            found_group = False;
            for groupid in self.groups:
                group = self.groups[groupid];
                repr_addr = group[0];
                repr_src = self.db.details(repr_addr).code.bytecode;

                if self.same(src,repr_src):
                    self.groups[groupid].append(addr);
                    found_group = True;
                    print("added to group:"+str(groupid)+":"+addr);
                    break;

            if found_group == False:
                self.groups[self.n] = [addr];
                print("new group:"+addr);
                self.n += 1;
        

    def report_dups(self,out):

        f = open(out+"_grps.txt","w+");

        for groupid in self.groups:
            row = str(groupid);
            for el in self.groups[groupid]:
                row += ","+str(el)
            f.write(row+"\n")

        f = open(out+"_addrs.txt","w+");

        for groupid in self.groups:
            for el in self.groups[groupid]:
                f.write(el+","+str(groupid)+"\n");

        
