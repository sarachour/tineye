import sys
from disasm import EVMCode
import json
from data import Bytecode,ReconstructedProgram,FragmentedProgram

def disasm(binary):
    disasm= EVMCode()
    bytecode = Bytecode(disasm.disassemble(binary))
    for instr in bytecode.code:
        print(repr(instr))

    return bytecode

def decompile(binary):
    print(binary)
    bytecode = disasm(binary)

    entry_points = bytecode.entry_points()

    from to_inf_reg import AbsExec
    abs_mach = AbsExec(bytecode)
    prog = FragmentedProgram()

    for point in entry_points:
        print("==== Entry Point %d ====" % point)
        prog_frag = abs_mach.execute(point);
        prog.set(point,prog_frag)

    prog.build()
    return prog;


def reconstruct(prog):
    prog.print_graph()
    recon_prog = ReconstructedProgram()

    from reconstruct import reconstruct

    for point in prog.entry_points:
        print("==== Entry Point %d ====" % point)
        recon_prog = reconstruct(prog,point)
        recon_prog.add_func(point,recon_prog)


        
def __main__():
    filename = sys.argv[1]
    fh = open(filename,'r')
    binary = fh.read()
    frag = decompile(binary)
    prog = reconstruct(frag)

__main__()
