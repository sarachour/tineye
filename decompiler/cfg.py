from cfg import *
from data import make_indent

class BasicBlock:
    def __init__(self):
        self.stmts = [];
        self.next = None;
        self.label = None;
        self.kind = "basic"


    @staticmethod
    def is_block(other):
        return other.kind == "basic"

    def add(self,stmt):
        self.stmts.append(stmt)

    def next_block(self,exit):
        self.next = exit

    def pretty(self,indent,detailed=False):
        s = ""
        if self.label != None:
            s += "%s<BASIC BLOCK %d>\n" % (make_indent(indent),self.label)


        if detailed:
            for stmt in self.stmts:
                s += stmt.pretty(indent) + "\n";
        else:
            s += "%s...\n" % (make_indent(indent))

        s += "\n"
        if self.next != None:
            s += self.next.pretty(indent,detailed=detailed)+"\n"

        return s

class LoopToBB:

    def __init__(self,loc):
        self.loc = loc;
        self.kind = "loopto"
        self.hook = None

    def set_hook(self,blk):
        self.hook = blk

    def get_hook(self):
        return self.hook

    @staticmethod
    def is_block(other):
        return other.kind == "loopto"

    def pretty(self,indent,detailed=False):
        s = "%sLOOPTO %d\n" % (make_indent(indent),self.loc)
        return s

class UninterpJumpBB:

    def __init__(self,loc):
        self.loc = loc
        self.kind = "uninterp_jump"
        self.hook = None

    def set_hook(self,blk):
        self.hook = blk

    def get_hook(self):
        return self.hook

    @staticmethod
    def is_block(other):
        return other.kind == "uninterp_jump"

    def set_loc(self,loc):
        self.loc = loc;

    def pretty(self,indent,detailed=False):
        s = "%sJUMPI %s\n" % (make_indent(indent),self.loc)
        return s


class ExceptionBB:

    def __init__(self):
        self.kind = "exception"
        self.hook = None
        return;

    def set_hook(self,blk):
        self.hook = blk

    @staticmethod
    def is_block(other):
        return other.kind == "exception"

    def pretty(self,indent,detailed=False):
        s = "%sRAISE ERROR\n" % (make_indent(indent))
        return s


class CondBB:

    def __init__(self,cond):
        self.cond = cond;
        self.taken = None;
        self.kind = "cond"
        self.not_taken = None;



    @staticmethod
    def is_block(other):
        return other.kind == "cond"

    def set_taken(self,blk):
        self.taken = blk;

    def set_not_taken(self,blk):
        self.not_taken = blk;

    def pretty(self,indent,detailed=False):
        s = "%sIF(%s):\n" %(make_indent(indent),self.cond)
        if self.taken != None:
            s += self.taken.pretty(indent+1,detailed=detailed)

        if self.not_taken != None:
            s += "%sELSE:\n" %(make_indent(indent))
            s += self.not_taken.pretty(indent+1,detailed=detailed)

        s += "%sEND" % (make_indent(indent))

        return s;
