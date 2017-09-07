from cfg import *
from data import make_indent

class BasicBlock:
    def __init__(self):
        self.stmts = [];
        self.next = None;
        self.label = None;
        self.kind = "basic"


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
            s += self.next.pretty(indent)+"\n"

        return s

class LoopToBB:

    def __init__(self,loc):
        self.loc = loc;
        self.kind = "loopto"


    def pretty(self,indent):
        s = "%sLOOPTO %d\n" % (make_indent(indent),self.loc)
        return s

class UninterpJumpBB:

    def __init__(self,loc):
        self.loc = loc
        self.kind = "uninterp_jump"


    def is_block(other):
        return other.kind == "uninterp_jump"

    def pretty(self,indent):
        s = "%sJUMPI %s\n" % (make_indent(indent),self.loc)
        return s


class ExceptionBB:

    def __init__(self):
        self.kind = "exception"
        return;


    def is_block(other):
        return other.kind == "exception"

    def pretty(self,indent):
        s = "%sRAISE ERROR\n" % (make_indent(indent))
        return s


class CondBB:

    def __init__(self,cond):
        self.cond = cond;
        self.taken = None;
        self.kind = "cond"
        self.not_taken = None;



    def is_block(other):
        return other.kind == "cond"

    def set_taken(self,blk):
        self.taken = blk;

    def set_not_taken(self,blk):
        self.not_taken = blk;

    def pretty(self,indent):
        s = "%sIF(%s):\n" %(make_indent(indent),self.cond)
        if self.taken != None:
            s += self.taken.pretty(indent+1)

        if self.not_taken != None:
            s += "%sELSE:\n" %(make_indent(indent))
            s += self.not_taken.pretty(indent+1)

        s += "%sEND" % (make_indent(indent))

        return s;
