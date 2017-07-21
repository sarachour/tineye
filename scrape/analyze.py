from contract import *
import subprocess as sp
from table import Table

class CodeAnalyzer:

    def __init__(self):
        self._db = ContractDatabase();
        self._db.read();
        self.groups = {};
        self.addrs = [];
        self.disasm_cmd = ["node","disasm/disasm.js"];
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

    def disassemble(self,code):
        bytecode_file = "bytecode.byte";
        opcode_file = "opcode.opc";

        args = self.disasm_cmd[:];
        args.append(bytecode_file);
        args.append(opcode_file);

        if code == None:
            return [];

        bytecode=open(bytecode_file,"w+");
        bytecode.write(code);
        bytecode.close();

        p = sp.Popen(args);
        exit_code = p.wait();
        #print(exit_code);

        opcode = open(opcode_file,"r");
        code = [];
        for l in opcode:
            line = l.strip();
            code.append(line);
        opcode.close();

        return code 


    def read_dedup(self,filename):
        if(filename == None):
            raise("must specify dedup file (addr file)")

        dedup = open(filename,"r");
        for l in dedup:
            args = l.strip().split(",");
            grp = args[1:];
            grpid = int(args[0]);
            self.groups[grpid] = {"addr":grp[0],"n":len(grp)}; 

    def disassemble_summary(self,output):
        header = ["group","addr","nmembers","ninsts"];
        dataset = {};
        for grp in self.groups:
            print("-> Proc group "+str(grp));
            addr =self.groups[grp]["addr"];
            self.db.read_details(addr);
            bcode = self.db.details(addr).code.bytecode;
            pcode = self.disassemble(bcode);
            data = {}
            data["addr"] = addr;
            data["ninsts"] = 0;

            for line in pcode:
                inst = line.split(" ")[0];
                if not (inst in header):
                    header.append(inst);

                if not (inst in data):
                    data[inst] = 0;
                else:
                    data[inst] += 1;

                data["ninsts"] += 1;

            dataset[grp] = data;

        tbl = Table(header);
        for grp in dataset:
            d = dataset[grp];
            tbl.add_cell("group",grp);
            tbl.add_cell("nmembers",self.groups[grp]["n"]);
            for field in d:
                v = d[field];
                tbl.add_cell(field,v);
            tbl.finish_row();

        tbl.write(output+".txt");

    def execute(self,kind,output,dedup=None,contract=None):
        if(dedup != None):
            self.read_dedup(dedup);

        if kind == "disasm":
            if contract != None:
                self.db.read_details(contract);
                code = self.db.details(contract).code.bytecode;
                pcode = self.disassemble(code)
                print(pcode);
            else:
                self.disassemble_summary(output);
