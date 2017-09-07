from data import EXPRS,CodeFrag,TODO,NoArg
from opcodes import OP

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


    def get_stack_pos(self):
        return self.top_counter

    def get_stack_val(self,n):
        idx = len(self.stack) - (n+1);
        return self.stack[idx]




import re
class AbsExec:

    def __init__(self,bytecode):
        self.code = bytecode;

    def decode_operands(self,str_data,n):
        data = EXPRS.NUMBER.make(int(str_data,16))
        return [data];

    def execute(self,point):
        prog = CodeFrag();
        state = AbsState(self.code)

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

            elif pc.name == OP.CALLDATASIZE:
                arg = EXPRS.ARGSIZE.make()
                ops = state.push([arg])
                prog.emit_all(ops)

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

                new_base = EXPRS.ADD.make(EXPRS.GETBASEREG.make(),EXPRS.NUMBER.make(state.get_stack_pos()))
                expr = EXPRS.JUMPIF.make().set_loc(args[0]).set_pred(args[1]).set_hook([EXPRS.SETBASEREG.make(new_base)])

                prog.emit_all(ops1)
                prog.emit(expr)

            elif pc.name == OP.JUMP:
                args,ops1 = state.pop(1);

                new_base = EXPRS.ADD.make(EXPRS.GETBASEREG.make(),EXPRS.NUMBER.make(state.get_stack_pos()))
                expr = EXPRS.JUMP.make().set_loc(args[0]).set_hook([EXPRS.SETBASEREG.make(new_base)])
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

                raise Exception("unimpl:%s" % (repr(pc)))
            if prog.terminated:
                continue;

            pc = state.next()

        return prog;
