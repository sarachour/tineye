from data import make_indent,EXPRS
from cfg import *
import copy

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



class ProgramFragRegister:
    def __init__(self):
        self.regs = {};
        for i in range(0,1024+1):
            self.regs[i] = EXPRS.ARG.make(i)

        self.stack = [];
        self.base_reg = 0;
        self.top = range(0,1024+1)
        self.top.reverse()

    def base_reg(self):
        return base_reg;

    def abs_idx(self,idx):
        return idx + self.base_reg;

    def set_base_reg(self,expr):
        math_expr = str(expr).replace("reg.base",str(self.base_reg))
        self.base_reg = eval(math_expr)
        #print("base_reg_upd: %d = %s" % (self.base_reg,math_expr))

    def get_reg(self,rel_idx):
        idx = self.abs_idx(rel_idx)
        if idx in self.regs:
            return self.regs[idx]
        else:
            return None

    def save(self):
        self.stack.append((self.regs,self.top,self.base_reg))
        self.regs = copy.deepcopy(self.regs)
        self.top = copy.deepcopy(self.top)
        self.base_reg = int(self.base_reg)

    def load(self):
        self.regs,self.top,self.base_reg = self.stack.pop()


    def clear(self,rel_idx):
        idx = self.abs_idx(rel_idx)
        top = self.top.pop()
        assert(idx == top)

    def store(self,rel_idx,value):
        idx = self.abs_idx(rel_idx)
        if idx < self.top[len(self.top) - 1]:
            self.top.append(idx);

        self.regs[idx] = value;


def execute_block(reg,cfg):

    if UninterpJumpBB.is_block(cfg):
        locval = cfg.loc.access(reg.get_reg)
        if locval.label == "number":
            print("VAL: %s -> %s" % (cfg.loc,locval))
            cfg.set_loc(locval)
            return

        else:
            print("VAR: %s -> %s" % (cfg.loc,locval))
            cfg.set_loc(locval)
            return

    elif ExceptionBB.is_block(cfg):
        return;

    elif LoopToBB.is_block(cfg):
        return

    assert(BasicBlock.is_block(cfg))
    for instr in cfg.stmts:
        #print(instr.pretty(2))
        if instr.label == "reg_store":
            new_expr = instr.expr2.access(reg.get_reg)
            reg.store(instr.expr1.id,new_expr)

        elif instr.label == "reg_destroy":
            reg.clear(instr.value.id)


        elif instr.label == "set_base_reg":
            reg.set_base_reg(instr.value);

    next_block = cfg.next

    if next_block == None:
        return;

    if CondBB.is_block(next_block):
        reg.save()
        execute_block(reg,next_block.taken)
        reg.load()
        reg.save()
        execute_block(reg,next_block.not_taken)
        reg.load()
        return

    else:
        execute_block(reg,next_block)


def resolve_symbolic_jumps(reg,cfg):
    # this must be a basic block
    execute_block(reg,cfg);

def derive_code_cfg(prog,stack,code):

    blk = BasicBlock();
    for idx in range(0,len(code)):
        instr = code[idx]
        # if we have a dynamic, unresolved jump mark as a symbolic jump
        if instr.kind == "jump" and instr.dynamic():
            jmp_hook = derive_code_cfg(prog,stack,instr.hook)
            jmp = UninterpJumpBB(instr.get_loc())
            jmp.set_hook(jmp_hook)

            if instr.has_pred():
                nt_blk = derive_code_cfg(prog,stack, code[(idx+1):])
                cond = CondBB(instr.pred)
                cond.set_taken(jmp)
                cond.set_not_taken(nt_blk)
                blk.next_block(cond)
                return blk;

            else:
                blk.next_block(jmp)
                return blk;

        elif instr.kind == "jump" and instr.dynamic() == False:
            loc = instr.get_loc()
            frag_child = prog.get_frag(loc)

            jump_hook= derive_code_cfg(prog,stack,instr.hook)

            if frag_child == None:
                jump_blk = ExceptionBB();
            else:
                code_child = frag_child.get_code()

                if loc in stack:
                    jump_blk  = LoopToBB(loc)
                    jump_blk.set_hook(jump_hook)
                else:
                    jump_body = derive_code_cfg(prog,[loc] + stack, code_child)
                    jump_body.label = loc
                    jump_hook.next_block(jump_body)
                    jump_blk = jump_hook


            if instr.has_pred():
                nt_blk = derive_code_cfg(prog,stack,code[(idx+1):])
                cond = CondBB(instr.pred)
                cond.set_taken(jump_blk)
                cond.set_not_taken(nt_blk)
                blk.next_block(cond)
                return blk

            else:
                blk.next_block(jump_blk)
                return blk

        else:
            blk.add(instr)

    return blk;



def derive_cfg(prog,entry):
    frag = prog.get_frag(entry)
    code = frag.get_code()
    top_block = derive_code_cfg(prog,[entry],code);
    top_block.label = entry
    resolve_symbolic_jumps(ProgramFragRegister(),top_block)
    #print(top_block.pretty(0,detailed=True))
    return top_block



def reconstruct(prog,entry):
    print("===== Reconstructing Entry ====")
    #executor = ProgramFragExecutor()
    par_block = derive_cfg(prog,entry)
