from decompiler.opcodes import OP

def make_indent(n):
    return "   " * n

class NoArg:

    def __init__(self):
        self.kind ="no_arg"

    def remap(self,i):
        return self;

    def access(self,fn):
        return self;

    def __repr__(self):
        return "_no_arg_"

    def pretty(self,indent):
        return "%s%s" % (make_indent(indent),str(self))

class TODO:

    def __init__(self,msg):
        self.kind ="todo"
        self.msg = msg

    def remap(self,i):
        return self;

    def access(self,fn):
        return self;

    def __repr__(self):
        return ("todo:%s" % self.msg)

    def pretty(self,indent):
        return "%s%s" % (make_indent(indent),str(self))

class Op0:

    def __init__(self,label,tostr):
        self.label = label;
        self.repr = tostr;
        self.kind = "op0"

    def make(self):
        return self;

    def __repr__(self):
        return self.repr

    def pretty(self,indent):
        return "%s%s" % (make_indent(indent),str(self))

    def remap(self,i):
        return self;

    def access(self,i):
        return self;


class Var:
    nvars = 0;

    def __init__(self,label,tostr):
        self.label = label
        self.var_id = Var.nvars
        self.repr = tostr;
        self.kind = "vars"
        Var.nvars += 1;

    def make(self):
        return Var(self.label,self.repr);

    def remap(self,i):
        return self;

    def access(self,i):
        return self;

    def __repr__(self):
        return self.repr % self.var_id

    def pretty(self,indent):
        return "%s%s" % (make_indent(indent),str(self))


class RegVal:

    def __init__(self,label,tostr):
        self.label = label;
        self.repr = tostr;
        self.id = None;
        self.kind = "regval"

    def make(self,value):
        op = RegVal(self.label,self.repr)
        op.id = int(value)
        return op


    def __repr__(self):
        return self.repr % (str(self.id))


    def pretty(self,indent):
        return "%s%s" % (make_indent(indent),str(self))

    def remap(self,i):
        rv = RegVal(self.label,self.repr)
        rv.id= i(self.id)
        return rv

    def access(self,get_i):
        reg_val = get_i(self.id)
        if reg_val == None:
            return self;
        else:
            return reg_val
class Op1:

    def __init__(self,label,tostr):
        self.label = label;
        self.repr = tostr;
        self.value = NoArg();
        self.kind = "op1"

    def make(self,value):
        op = Op1(self.label,self.repr)
        op.value = value;
        return op;

    def __repr__(self):
        return self.repr % (str(self.value))


    def pretty(self,indent):
        return "%s%s" % (make_indent(indent),str(self))

    def map(self,fn):
        o = Op1(self.label,self.repr)
        try:
            o.value = fn(self.value)
        except Exception:
            return self;
        return o


    def remap(self,i):
        return self.map(lambda x: x.remap(i))

    def access(self,i):
        return self.map(lambda x: x.access(i))

class OpN:

    def __init__(self,label,tostr):
        self.label = label;
        self.repr = tostr;
        self.value = [NoArg()];
        self.kind = "opn"

    def make(self,value):
        op = OpN(self.label,self.repr)
        op.value = value;
        return op;

    def __repr__(self):
        return self.repr % (str(self.value))

    def pretty(self,indent):
        return "%s%s" % (make_indent(indent),str(self))

    def remap(self,i):
        o = OpN(self.label,self.repr)
        o.value = la

    def map(self,fn):
        o = OpN(self.label,self.repr)
        o.value = map(fn,self.value)
        return o

    def remap(self,i):
        return self.map(lambda x: x.remap(i))

    def access(self,i):
        return self.map(lambda x: x.access(i))

class Op2:

    def __init__(self,label,tostr):
        self.label = label;
        self.repr = tostr;
        self.expr1 = NoArg();
        self.expr2 = NoArg();
        self.kind = "op2"

    def args(self,e1,e2):
        self.expr1 = e1;
        self.expr2 = e2;

    def make(self,e1,e2):
        op = Op2(self.label,self.repr)
        op.args(e1,e2)
        return op

    def __repr__(self):
        return self.repr % (str(self.expr1),str(self.expr2))


    def pretty(self,indent):
        return "%s%s" % (make_indent(indent),str(self))


    def map(self,fn):
        o = Op2(self.label,self.repr)
        o.expr1 = fn(self.expr1)
        o.expr2 = fn(self.expr2)
        return o

    def remap(self,i):
        return self.map(lambda x: x.remap(i))

    def access(self,i):
        return self.map(lambda x: x.access(i))

class Op3:

    def __init__(self,label,tostr):
        self.label = label;
        self.repr = tostr;
        self.expr1 = NoArg();
        self.expr2 = NoArg();
        self.expr3 = NoArg();
        self.kind = "op3"

    def args(self,e1,e2,e3):
        self.expr1 = e1;
        self.expr2 = e2;
        self.expr3 = e3;

    def make(self,e1,e2,e3):
        op = Op3(self.label,self.repr)
        op.args(e1,e2,e3)
        return op

    def __repr__(self):
        return self.repr % (str(self.expr1),str(self.expr2),str(self.expr3))

    def pretty(self,indent):
        return "%s%s" % (make_indent(indent),str(self))

    def map(self,fn):
        o = Op3(self.label,self.repr)
        o.expr1 = fn(self.expr1)
        o.expr2 = fn(self.expr2)
        o.expr3 = fn(self.expr3)
        return o


    def remap(self,i):
        return self.map(lambda x: x.remap(i))

    def access(self,i):
        return self.map(lambda x: x.access(i))

class Call:

    def __init__(self,label):
        self.label = label
        self.kind = "call"

    def make(self):
        return Call(self.label)

    def set_gas(self,data):
        self.gas = data;
        return self;

    def set_callee(self,data):
        self.to = data;
        return self;

    def set_value(self,data):
        self.value = data;

    def set_inputs(self,offset,size):
        self.inputs = (offset,size)

    def set_outputs(self,offset,size):
        self.outputs = (offset,size)

    def __repr__(self):
        base = "call(%s,%s,%s)" % (self.to,self.value,self.gas)
        inps = "ins[%s,%s]" % (self.inputs[0],self.inputs[1])
        outs = "outs[%s,%s]" % (self.outputs[0],self.outputs[1])
        return "%s : %s -> %s" % (base,inps,outs)

    def pretty(self,indent):
        return "%s%s" % (make_indent(indent),str(self))

    def map(self,fn):
        rc = Call(self.label)
        rc.gas = fn(self.gas)
        rc.to = fn(self.to)
        rc.value = fn(self.value)
        rc.inputs = map(fn,self.inputs)
        rc.outputs = map(fn,self.outputs)
        return rc

    def remap(self,i):
        return self.map(lambda x: x.remap(i))

    def access(self,i):
        return self.map(lambda x: x.access(i))

class Jump:
    def __init__(self,label):
        self.label = label
        self.kind = "jump"
        self.loc =NoArg()
        self.pred =NoArg()
        self.hook = [];


    def set_hook(self,hook):
        self.hook = hook
        return self

    def make(self):
        return Jump(self.label)

    def set_loc(self,loc):
        self.loc = loc;
        return self;

    def set_pred(self,pred):
        self.pred = pred;
        return self;

    def has_pred(self):
        return self.pred.kind != "no_arg"

    def dynamic(self):
        return self.loc.label != "number"

    def get_loc(self):
        if self.dynamic():
            return self.loc
        else:
            return self.loc.value

    def __repr__(self):
        if self.pred.kind == "no_arg":
            return "goto %s" % self.loc
        else:
            return "if(%s): goto %s" %(self.pred,self.loc)

    def pretty(self,indent):
        return "%s%s" % (make_indent(indent),str(self))

    def map(self,fn):
        rj = Jump(self.label)
        rj.loc = fn(self.loc);
        rj.pred = fn(self.pred);
        return rj;

    def remap(self,i):
        return self.map(lambda x: x.remap(i))

    def access(self,i):
        return self.map(lambda x: x.access(i))

class ExprSpec:
    def __init__(self):
        # n is number of bits
        self.MLOAD = Op2("mem_load","mem.load[%s,n=%s]")
        self.MSTORE = Op3("mem_store","mem.store[%s,n=%s] := %s")
        self.SLOAD = Op1("disk_load","disk.load[%s]")
        self.ARGLOAD = Op2("arg_load","args.word(%s,n=%s)")
        self.ARGSIZE= Op0("arg_load","args.size")
        self.ARG= Op1("arg","arg%s")

        self.SSTORE = Op2("disk_store","disk.store[%s] := %s")
        self.NUMBER = Op1("number","%s")
        self.ASSIGN = Op2("assign","%s = %s")
        self.VAR = Var("var","v%s")
        self.SHA3 = Op1("sha3","sha3(%s)")
        self.SETBASEREG = Op1("set_base_reg","reg.base = %s")
        self.BALANCE = Op1("balance","bal(%s)")
        self.NOT = Op1("not","!%s")
        self.OPLABEL = Op1("lbl","// %s")
        self.RETURN = Op1("return","return %s")
        self.REGVAL = RegVal("reg_val","reg[%s]")
        self.ADD = Op2("add","(%s+%s)")
        self.AND = Op2("and","(%s & %s)")
        self.OR = Op2("or","(%s | %s)")
        self.LT = Op2("lt","%s < %s")
        self.GT = Op2("gt","%s > %s")
        self.SLT= Op2("slt","%s ~< %s")
        self.SGT = Op2("sgt","%s ~> %s")
        self.SUB = Op2("sub","(%s-%s)")
        self.EQ = Op2("eq","(%s==%s)")
        self.EXP = Op2("exp","exp(%s,%s)")
        self.MUL = Op2("mul","(%s*%s)")
        self.JUMPIF= Jump("jump_if")
        self.JUMP = Jump("jump")
        self.DIV = Op2("div","%s/%s")
        self.STOP = Op0("stop","stop")
        self.GETBASEREG = Op0("base_reg","reg.base")
        self.CALLER = Op0("caller","tx.caller")
        self.VALUE = Op0("value","tx.value")
        self.BLOCKNUM= Op0("block_num","blk.number")
        self.MSIZE = Op0("mem_size","mem.size")
        self.ORIGIN = Op0("tx.origin","tx.origin")
        self.LOG = OpN("log","log(%s)")
        self.CALL = Call("call")
        self.THROW = Op0("throw","throw exception")
        self.REG_STORE = Op2("reg_store","%s := %s")
        self.REG_LOAD = Op1("reg_load","%s")
        self.REG_DESTROY = Op1("reg_destroy","delete %s")
        self.COMMENT = Op1("comment","// %s")

EXPRS = ExprSpec()

class Bytecode:

    def __init__(self,bytecode):
        self.addrs = {};
        self.code = [];

        for inst in bytecode:
            self.addrs[inst.address] = len(self.code);
            self.code.append(inst);

    def index(self,pc):
        return self.addrs[pc]

    def entry_points(self):
        entry = [0];
        for instr in self.code:
            if instr.name == OP.JUMPDEST:
                entry.append(instr.address)

        return entry;

    def instr_at(self,idx):
        if idx < len(self.code):
            return self.code[idx]
        return None

import copy

class CodeFrag:
    def __init__(self):
        self.code = [];
        self.terminated = False;

    def get_code(self):
        return self.code

    def emit(self,st):
        self.code.append(st);

    def emit_all(self,sts):
        for st in sts:
            self.emit(st)

    def terminate(self):
        self.terminated = True;

    def cf(self):
        dests = []
        for instr in self.code:
            if instr.kind == "jump":
                dests.append(instr)

        return dests;

    def endpoint(self):

        for instr in self.code:
            if instr.kind == "jump" and instr.pred == None:
                    return False

        return True

    def __repr__(self):
        stmts = "";
        for stmt in self.code:
            stmts += "%s\n" % (str(stmt))

        return stmts;

    def pretty(self,indent):
        sts = ""
        for st in self.code:
            if st.label == "lbl":
                continue;
            sts+= st.pretty(indent)+"\n"

        return sts




class Block:
    def __init__(self):
        self.stmts = [];
        self.kind = self.label = "block"

    def add(self,b):
        self.stmts.append(b)

    def pretty(self,indent):
        sts = ""
        for st in self.stmts:
            if st.label == "reg_destroy" or st.label == "reg_store" or st.label == "lbl":
                continue;
            sts+= st.pretty(indent)+"\n"

        return sts

class Conditional:
    def __init__(self,cond,label):
        self.cond = cond;
        self.taken = Block();
        self.not_taken = Block();
        self.ident = label;
        self.kind = self.label = "cond"

    def pretty(self,indent):
        sts = "%sif(%s) @%s\n" % (make_indent(indent),self.cond,self.ident)
        sts += self.taken.pretty(indent+1)
        sts += "%selse\n" % make_indent(indent)
        sts += self.not_taken.pretty(indent+1)
        sts += "%send\n" % (make_indent(indent))
        return sts


class FragmentedProgram:

    def __init__(self):
        self.fragments = {};
        self.graph = {};
        self.sources = [];
        self.end_points= [];


    def get_frag(self,entry):
        if entry in self.fragments:
            return self.fragments[entry]
        else:
            None

    def set(self,entry,fragment):
        self.fragments[entry] = fragment


    def build(self):
        for entry in self.fragments:
            fragment = self.fragments[entry]
            cf_endpts = fragment.cf()
            self.graph[entry] = []
            for endpt in cf_endpts:
                self.graph[entry].append(endpt.loc)

            if fragment.endpoint():
                self.end_points.append(entry)

        self.entry_points = self.fragments.keys()[:]

        for entry in self.fragments.keys():
            ends = self.graph[entry]
            for end in ends:
                if end in self.entry_points and end != entry:
                    self.entry_points.remove(end)

    def print_graph(self):
        print("=== Entry points===")
        for entry in self.entry_points:
            print("in %s" % entry)
        print("=== End points ===")
        for endpt in self.end_points:
            print("end %s" % endpt)

        print("=== Control Flow ===")
        for entry in self.graph:
            for exit in self.graph[entry]:
                print("%s -> %s" % (entry,exit))


    def pretty(self):
        rep = ""
        for point in self.fragments:
            modif = "LOC "
            if point in self.entry_points:
                modif += "IN "

            if point in self.end_points:
                modif += "OUT "

            sinks = [];
            if point in self.graph:
                sinks = self.graph[point]

            rep += "%s %d => LOC [%s]\n" % (modif,point,str(sinks))
            rep += self.fragments[point].pretty(1)
            rep += "\n\n\n"

        return rep;

    def dump(self):
        js = {
        }
        return json.dumps(js)

class ReconstructedProgram:

    def __init__(self):
        self.blocks = {};

    def add_func(self,entry_point,code):
        self.blocks[entry_point] = code
