import json;
import matplotlib as mp
from colormap import rgb2hex
import sys
class CoverageExec:
    def __init__(self,code,pc):
        self.code = code;
        self.freqmap = {};
        self.entry = pc;
        self.known = 0;
        self.unknown = 0;
        self.traces = 0;

    def exec_op(self,el):
        inst = el['pc']
        if not (inst in self.freqmap):
            self.freqmap[inst] = 0
        self.freqmap[inst] += 1

        if inst in self.code:
            inst_code  = self.code[inst]
            assert(el['op'] == inst_code.name)
            self.known += 1;
        else:
            self.unknown += 1;


    def exec_trace(self,trace):
        for opc in trace.trace:
            self.exec_op(opc);

        self.traces += 1;

    def write(self,filename):
        n = self.traces
        f = open('%s.html' % filename,'w')
        colormap = mp.cm.get_cmap('RdYlGn')

        for pc in self.code:
            instr = self.code[pc]
            if pc in self.freqmap:
                execs = float(self.freqmap[pc])/n
            else:
                execs = 0.0;

            instr_str = "%d: %s" % (pc,instr)

            if execs == 0.0:
                f.write("<div>%s</div>" % instr_str)
            else:
                r,g,b,a = colormap(execs)
                hexv = rgb2hex(r*255,g*255,b*255)
                f.write("<div style='background-color:%s'>%s</div>" % (hexv,instr_str))

        f.close()

class CoverageMap:

    def __init__(self,code):
        self.code = code;
        self.entry_points = {};


    def exec_trace(self,trace):
        entry_point = trace.entry_point
        print(entry_point)
        # the first jump determines the function.
        if not (entry_point in self.entry_points):
            self.entry_points[entry_point] = CoverageExec(self.code,entry_point)

        self.entry_points[entry_point].exec_trace(trace);

    def write(self,name):
        for entry_point in self.entry_points:
            ep = self.entry_points[entry_point]
            ep.write("%s_%s" % (name,entry_point))


class Retina:

    def __init__(self,path,source,traces):
        self.path = path;
        self.code = self.disassemble(source)
        self.traces = {};
        for trace in traces:
            self.traces[trace.txn] = trace


    def disassemble(self,code):
        bytecode = code[0].split("0x")[1]

        disasm = EVMDisAssembler()
        code = {};
        for opc in disasm.disassemble(bytecode):
            print("%d: %s" % (opc.address,opc));
            code[opc.address] = opc


        return code;


    def coverage(self):
        coverage = CoverageMap(self.code);
        for ident in self.traces:
            print("-> proc %s" % ident)
            trace = self.traces[ident]
            coverage.exec_trace(trace)

        coverage.write('coverage')
        print("done")
