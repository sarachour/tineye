
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
        self.TIMESTAMP = "TIMESTAMP"
        self.SHA3 = "SHA3"
        self.LT= "LT"
        self.SLT= "SLT"
        self.GT= "GT"
        self.SGT = "SGT"
        self.CALLDATASIZE = "CALLDATASIZE"
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
        self.CALLCODE = "CALLCODE"
        self.ORIGIN = "ORIGIN"
        self.GAS = "GAS"
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

    def unknown(self,name):
        if "UNKNOWN" in name:
            return True
        return False

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
