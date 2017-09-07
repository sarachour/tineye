import sys
from disasm import EVMCode

def make_indent(n):
    return "   " * n

class Opcodes:

    def __init__(self):
        self.JUMPDEST = "JUMPDEST"
        self.MLOAD = "MLOAD"
        self.MSTORE = "MSTORE"
        self.MSTORE8 = "MSTORE8"
        self.SLOAD = "SLOAD"
        self.SSTORE = "SSTORE"
        self.STOP = "STOP"
        self.ADD = "ADD"
        self.MUL = "MUL"
        self.SHA3 = "SHA3"
        self.LT= "LT"
        self.SLT= "SLT"
        self.GT= "GT"
        self.SGT = "SGT"
        self.EXP= "EXP"
        self.SUB = "SUB"
        self.DIV = "DIV"
        self.AND = "AND"
        self.OR = "OR"
        self.NUMBER = "NUMBER"
        self.BALANCE = "BALANCE"
        self.NOT = "NOT"
        self.CALLER = "CALLER"
        self.ISZERO= "ISZERO"
        self.CALL= "CALL"
        self.ORIGIN = "ORIGIN"
        self.BALANCE = "BALANCE"
        self.OR = "OR"
        self.JUMPI = "JUMPI"
        self.JUMP = "JUMP"
        self.EQ = "EQ"
        self.RETURN= "RETURN"
        self.CALLVALUE = "CALLVALUE"
        self.MSIZE = "MSIZE"
        self.CALLDATACOPY = "CALLDATACOPY"
        self.CALLDATALOAD = "CALLDATALOAD"

    def push(self,name):
        if "PUSH" in name:
            return True;
        return False;

    def swap(self,name):
        if "SWAP" in name:
            return True;
        return False;

    def log(self,name):
        if "LOG" in name:
            return True;
        return False;

    def pop(self,name):
        if "POP" in name:
            return True;
        return False;

    def dup(self,name):
        if "DUP" in name:
            return True;
        return False;

    def swap_n(self,name):
        assert(self.swap(name))
        return int(name.split("SWAP")[1])

    def pop_n(self,name):
        assert(self.pop(name))
        if name == "POP":
            return 1;

        return int(name.split("POP")[1])

    def log_n(self,name):
        assert(self.log(name))
        if name == "LOG":
            return 1;
        return int(name.split("LOG")[1])

    def push_n(self,name):
        assert(self.push(name))
        if name == "PUSH":
            return 1;
        return int(name.split("PUSH")[1])


    def dup_n(self,name):
        assert(self.dup(name))
        return int(name.split("DUP")[1])

    def pretty(self,indent):
        return "%s%s" % (make_indent(indent),str(self))


OP = Opcodes()

class NoArg:

    def __init__(self):
        self.kind ="none"

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

    def make(self):
        return Jump(self.label)

    def set_loc(self,loc):
        self.loc = loc;
        return self;

    def set_pred(self,pred):
        self.pred = pred;
        return self;

    def dynamic(self):
        return self.loc.label != "number"

    def get_loc(self):
        return self.loc.value

    def __repr__(self):
        if self.pred == None:
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
        self.SSTORE = Op2("disk_store","disk.store[%s] := %s")
        self.NUMBER = Op1("number","%s")
        self.ASSIGN = Op2("assign","%s = %s")
        self.VAR = Var("var","v%s")
        self.SHA3 = Op1("sha3","sha3(%s)")
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

class AbsState:

    def __init__(self,bytecode):
        self.stack_size = 1024;
        self.stack = map(lambda i : EXPRS.REGVAL.make(1024-i), range(0,1024+1))
        self.code = bytecode;
        self.pc = 0;
        self.top_counter = 0;


    def jump(self,pc):
        self.pc = self.code.index(pc)
        return self.code.instr_at(self.pc)

    def next(self):
        self.pc = self.pc+1;
        return self.code.instr_at(self.pc)


    def push_1(self,data):
        self.stack.append(data)
        self.top_counter -= 1;
        reg = EXPRS.REGVAL.make(self.top_counter)
        op = EXPRS.REG_STORE.make(reg,data)
        return op;

    def push(self,data):
        ops = []
        for entry in data:
            op = self.push_1(entry)
            ops.append(op)

        return ops;

    def pop_1(self):
        arg = self.stack.pop(-1)
        reg = EXPRS.REGVAL.make(self.top_counter)
        op = EXPRS.REG_DESTROY.make(reg)
        self.top_counter += 1;
        return arg,op

    def pop(self,n):
        ops = [];
        args = [];

        for i in range(0,n):
            arg,op = self.pop_1()
            ops.append(op)
            args.append(arg)

        return args,ops

    def store(self,n1,data):
        self.stack[len(self.stack) - (n1 +1)] = data
        reg = EXPRS.REGVAL.make(self.top_counter + n1)
        return EXPRS.REG_STORE.make(reg, data)

    def swap(self,n1,n2):
        tmp = self.stack[len(self.stack) - (n2+1)]
        op1 =self.store(n2,self.stack[len(self.stack) - (n1+1)])
        op2 = self.store(n1,tmp)
        return [op1,op2]


    def get_stack_val(self,n):
        idx = len(self.stack) - (n+1);
        return self.stack[idx]

class ProgramFrag:
    def __init__(self):
        self.code = [];
        self.terminated = False;


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

import re
class AbsExec:

    def __init__(self,bytecode):
        self.code = bytecode;

    def decode_operands(self,str_data,n):
        data = EXPRS.NUMBER.make(int(str_data,16))
        return [data];

    def execute(self,point):
        prog = ProgramFrag();
        state = AbsState(bytecode)

        pc = state.jump(point)
        assert(pc.name == OP.JUMPDEST or point == 0)

        while not prog.terminated:
            ops = ops1 = ops2 = None;
            if pc == None:
                prog.emit(EXPRS.STOP.make())
                prog.terminate()
                continue;

            prog.emit(EXPRS.OPLABEL.make(pc))

            if OP.push(pc.name):
                n = OP.push_n(pc.name)
                data = self.decode_operands(pc.operand,n)
                ops = state.push(data)
                prog.emit_all(ops);

            elif OP.pop(pc.name):
                n = OP.pop_n(pc.name)
                _,ops = state.pop(n)
                prog.emit_all(ops);

            elif OP.log(pc.name):
                n = OP.log_n(pc.name)
                args,ops = state.pop(n+2)
                prog.emit_all(ops);
                prog.emit(EXPRS.LOG.make(args));


            elif pc.name == OP.SSTORE:
                args,ops1 = state.pop(2);
                ms = EXPRS.SSTORE.make(args[0],args[1])
                prog.emit_all(ops1);
                prog.emit(ms)


            elif pc.name == OP.SLOAD:
                args,ops1 = state.pop(1);
                ml = EXPRS.SLOAD.make(args[0])
                m_var = EXPRS.VAR.make()
                iv = EXPRS.ASSIGN.make(m_var,ml)
                ops2 = state.push([m_var])
                prog.emit_all(ops1 + [iv] + ops2)

            elif pc.name == OP.MSTORE:
                args, ops1 = state.pop(2);
                prog.emit_all(ops1)
                siz = EXPRS.NUMBER.make(32)
                ms = EXPRS.MSTORE.make(args[0],siz,args[1])
                prog.emit(ms)

            elif pc.name == OP.MSTORE8:
                args, ops1 = state.pop(2);
                siz = EXPRS.NUMBER.make(8)
                ms = EXPRS.MSTORE.make(args[0],siz,args[1])
                prog.emit_all(ops1)
                prog.emit(ms)

            elif pc.name == OP.CALL:
                args,ops1 = state.pop(7);
                prog.emit_all(ops1);
                call = EXPRS.CALL.make();
                call.set_gas(args[0]).set_callee(args[1]).set_value(args[2])
                call.set_inputs(args[3],args[4])
                call.set_outputs(args[5],args[6])
                ops2 = state.push([TODO("return_val_for_call")])
                prog.emit(call)
                prog.emit_all(ops2)

            elif pc.name == OP.CALLVALUE:
                ops = state.push([EXPRS.VALUE.make()])
                prog.emit_all(ops)

            elif pc.name == OP.MSIZE:
                ops = state.push([EXPRS.MSIZE.make()])
                prog.emit_all(ops)

            elif pc.name == OP.CALLDATALOAD:
                args,ops1 = state.pop(1);
                siz = EXPRS.NUMBER.make(8)
                ml = EXPRS.ARGLOAD.make(args[0],siz);
                ops2 = state.push([ml])
                prog.emit_all(ops1+ops2)

            elif pc.name == OP.CALLDATACOPY:
                args,ops1 = state.pop(3);
                n_bits = EXPRS.MUL.make(args[2],EXPRS.NUMBER.make(8))
                data = EXPRS.ARGLOAD.make(args[0],n_bits);
                ml = EXPRS.MSTORE.make(args[1],args[2],data)
                prog.emit_all(ops1)
                prog.emit(ml)

            elif pc.name == OP.SHA3:
                args,ops1 = state.pop(2);
                memload = EXPRS.MLOAD.make(args[0],args[1])
                sha3 = EXPRS.SHA3.make(memload)
                ops2 = state.push([sha3])
                prog.emit_all(ops1 + ops2)

            elif pc.name == OP.BALANCE:
                args,ops1 = state.pop(1);
                ml = EXPRS.BALANCE.make(args[0])
                ops2 = state.push([ml])
                prog.emit_all(ops1 + ops2)

            elif pc.name == OP.MLOAD:
                args,ops1 = state.pop(1);
                siz = EXPRS.NUMBER.make(32)
                ml = EXPRS.MLOAD.make(args[0],siz)
                m_var = EXPRS.VAR.make()
                iv = EXPRS.ASSIGN.make(m_var,ml)
                ops2 = state.push([m_var])
                prog.emit_all(ops1 +[iv]+ ops2)

            elif pc.name == OP.EXP:
                args,ops1 = state.pop(2);
                expr = EXPRS.EXP.make(args[0],args[1])
                ops2 = state.push([expr]);
                prog.emit_all(ops1 + ops2)

            elif pc.name == OP.CALLER:
                ops = state.push([EXPRS.CALLER.make()])
                prog.emit_all(ops)

            elif pc.name == OP.NUMBER:
                ops = state.push([EXPRS.BLOCKNUM.make()])
                prog.emit_all(ops)

            elif pc.name == OP.ORIGIN:
                ops = state.push([EXPRS.ORIGIN.make()])
                prog.emit_all(ops)

            elif pc.name == OP.NOT:
                args,ops1 = state.pop(1);
                expr = EXPRS.NOT.make(args[0])
                ops2 = state.push([expr]);
                prog.emit_all(ops1 + ops2)

            elif pc.name == OP.EQ:
                args,ops1 = state.pop(2);
                expr = EXPRS.EQ.make(args[0],args[1])
                ops2 = state.push([expr]);
                prog.emit_all(ops1 + ops2)

            elif pc.name == OP.OR:
                args,ops1 = state.pop(2);
                expr = EXPRS.OR.make(args[0],args[1])
                ops2 = state.push([expr]);
                prog.emit_all(ops1 + ops2)

            elif pc.name == OP.SLT:
                args,ops1 = state.pop(2);
                expr = EXPRS.OR.make(args[0],args[1])
                ops2 = state.push([expr]);
                prog.emit_all(ops1 + ops2)

            elif pc.name == OP.SGT:
                args,ops1 = state.pop(2);
                expr = EXPRS.OR.make(args[0],args[1])
                ops2 = state.push([expr]);
                prog.emit_all(ops1 + ops2)

            elif pc.name == OP.ISZERO:
                args,ops1 = state.pop(1);
                expr = EXPRS.EQ.make(args[0],EXPRS.NUMBER.make(0))
                ops2 = state.push([expr])
                prog.emit_all(ops1+ops2)

            elif pc.name == OP.MUL:
                args,ops1 = state.pop(2);
                expr = EXPRS.MUL.make(args[0],args[1])
                ops2 = state.push([expr]);
                prog.emit_all(ops1 + ops2)

            elif pc.name == OP.DIV:
                args,ops1 = state.pop(2);
                expr = EXPRS.DIV.make(args[0],args[1])
                ops2 = state.push([expr]);
                prog.emit_all(ops1 + ops2)


            elif pc.name == OP.GT:
                args,ops1 = state.pop(2);
                expr = EXPRS.GT.make(args[0],args[1])
                ops2 = state.push([expr]);
                prog.emit_all(ops1 + ops2)

            elif pc.name == OP.LT:
                args,ops1 = state.pop(2);
                expr = EXPRS.LT.make(args[0],args[1])
                ops2 = state.push([expr]);
                prog.emit_all(ops1 + ops2)

            elif pc.name == OP.AND:
                args,ops1 = state.pop(2);
                expr = EXPRS.AND.make(args[0],args[1])
                ops2 = state.push([expr]);
                prog.emit_all(ops1 + ops2)

            elif pc.name == OP.ADD:
                args,ops1 = state.pop(2);
                expr = EXPRS.ADD.make(args[0],args[1])
                ops2 = state.push([expr]);
                prog.emit_all(ops1 + ops2)

            elif pc.name == OP.SUB:
                args,ops1 = state.pop(2);
                expr = EXPRS.SUB.make(args[0],args[1])
                ops2 = state.push([expr]);
                prog.emit_all(ops1 + ops2)

            elif OP.swap(pc.name):
                n = OP.swap_n(pc.name)
                ops = state.swap(0,n);
                prog.emit_all(ops)

            elif OP.dup(pc.name):
                n = OP.dup_n(pc.name)
                arg = state.get_stack_val(n-1);
                ops = state.push([arg])
                prog.emit_all(ops)

            elif pc.name == OP.JUMPI:
                args,ops1 = state.pop(2);
                expr = EXPRS.JUMPIF.make().set_loc(args[0]).set_pred(args[1])
                prog.emit_all(ops1)
                prog.emit(expr)

            elif pc.name == OP.JUMP:
                args,ops1 = state.pop(2);
                expr = EXPRS.JUMP.make().set_loc(args[0])
                prog.emit_all(ops1)
                prog.emit(expr)
                prog.terminate()

            elif pc.name == OP.RETURN:
                args,ops1 = state.pop(2);
                ml = EXPRS.MLOAD.make(args[0],args[1])
                expr = EXPRS.RETURN.make(ml)
                prog.emit_all(ops1)
                prog.emit(expr)
                prog.terminate()

            elif pc.name == OP.JUMPDEST:
                pc = state.next()
                continue;

            elif pc.name == OP.STOP:
                prog.emit(EXPRS.STOP.make())
                prog.terminate()

            else:

                raise Exception("unimpl")
            if prog.terminated:
                continue;

            pc = state.next()

        return prog;

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

class ProgramFragRegister:
    def __init__(self):
        self.regs = {};
        for i in range(0,1024+1):
            self.regs[i] = EXPRS.REGVAL.make(i)

        self.stack = [];
        self.top = range(0,1024+1)
        self.top.reverse();

    def get_reg(self,idx):
        if idx in self.regs:
            return self.regs[idx]
        else:
            return None

    def save(self):
        self.stack.append((self.regs,self.top))
        self.regs = copy.deepcopy(self.regs)
        self.top = copy.deepcopy(self.top)

    def load(self):
        self.regs,self.top = self.stack.pop()

    # remap with current stack
    def remap(self,prog):
        newprog = [];
        top = min(self.top)
        fn = lambda idx: idx + top
        for instr in prog:
            new_instr = instr.remap(fn)
            newprog.append(new_instr)


        return newprog

    def clear(self,idx):
        top = self.top.pop()
        assert(idx == top)

    def store(self,idx,value):
        if idx < self.top[len(self.top) - 1]:
            self.top.append(idx);

        self.regs[idx] = value;

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


class ProgramCF:

    def __init__(self):
        self.preds = [];
        self.entry_points = [];

    def pred_call(self,pred,entry_point):
        self.preds.append(pred)
        self.entry_points.append(entry_point)

    def call(self,entry_point):
        self.entry_points.append(entry_point)
        self.preds.append(None)

    def loops(self,entry_point):
        if entry_point in self.entry_points:
            return True;

        return False;

    def ret(self):
        self.entry_points.pop()
        self.preds.pop()


class ProgramFragExecutor:

    def __init__(self):
        self.regs = ProgramFragRegister();
        self.cf = ProgramCF()

    # transform into a new program
    def execute_code(self,prog,code,block):
        for idx in range(0,len(code)):

            instr = code[idx]
            if instr.label == "reg_store":
                new_expr2 = instr.expr2.access(self.regs.get_reg)
                self.regs.store(instr.expr1.id,new_expr2)
                block.add(EXPRS.REG_STORE.make(instr.expr1,new_expr2))

            elif instr.label == "reg_destroy":
                self.regs.clear(instr.value.id)
                block.add(instr)

            elif instr.kind == "jump":

                # if this creates a loop
                if instr.dynamic() or (instr.dynamic() == False and self.cf.loops(instr.get_loc())):
                        block.add(instr);
                        return;

                if instr.pred != None:
                    new_pred = instr.pred.access(self.regs.get_reg)
                    cond = Conditional(new_pred,instr.get_loc())

                    self.cf.pred_call(instr.pred,None)
                    self.regs.save()
                    self.execute_entry(prog,instr.get_loc(),cond.taken)
                    self.regs.load()
                    self.cf.ret()

                    self.cf.pred_call(EXPRS.NOT.make(instr.pred),None)
                    self.regs.save()
                    self.execute_code(prog,code[(idx+1):],cond.not_taken)
                    self.regs.load()
                    self.cf.ret()

                    block.add(cond)
                    return;
                else:
                    self.execute_entry(prog,instr.get_loc(),block)


            else:
                new_instr = instr.access(self.regs.get_reg)
                block.add(new_instr);

    def execute_entry(self,prog,entry,block):
        self.cf.pred_call(None,entry)
        code = prog.fragments[entry].code
        new_code = self.regs.remap(code)
        self.execute_code(prog,new_code,block)
        self.cf.ret()

class Program:

    def __init__(self):
        self.fragments = {};
        self.graph = {};
        self.sources = [];
        self.end_points= [];

    def reconstruct(self,entry):
        print("===== Reconstructing Entry ====")
        executor = ProgramFragExecutor()
        fxn = Block()
        executor.execute_entry(self,entry,fxn)
        return fxn;



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


filename = sys.argv[1]
fh = open(filename,'r')
binary = fh.read()

print(binary)
disasm= EVMCode()
bytecode = Bytecode(disasm.disassemble(binary))

entry_points = bytecode.entry_points()

abs_mach = AbsExec(bytecode)
prog = Program()

for point in entry_points:
    print("==== Entry Point %d ====" % point)
    prog_frag = abs_mach.execute(point);
    prog.set(point,prog_frag)

prog.build()
prog.print_graph()

for point in prog.entry_points:
    print("==== Entry Point %d ====" % point)
    recon_prog = prog.reconstruct(point)
    print(recon_prog.pretty(0))
