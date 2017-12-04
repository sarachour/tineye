import sys
from decompiler.disasm import EVMCode
import json
from decompiler.data import Bytecode,ReconstructedProgram,FragmentedProgram

def disasm(binary):
    disasm= EVMCode()
    bytecode = Bytecode(disasm.disassemble(binary))

    return bytecode

def decompile(binary):
    print(binary)
    bytecode = disasm(binary)

    entry_points = bytecode.entry_points()

    from decompiler.to_inf_reg import AbsExec
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
        fxn = reconstruct(prog,point)
        recon_prog.add_func(point,fxn)

    return recon_prog 

def main():
    filename = sys.argv[1]
    fh = open(filename,'r')
    binary = fh.read()
    frag = decompile(binary)
    prog = reconstruct(frag)

