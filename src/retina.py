import json;
from evmdasm import EVMDisAssembler
import matplotlib as mp
from colormap import rgb2hex

class CoverageMap:

    def __init__(self,code):
        self.code = code;
        self.freqmap = {};
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
        self.traces += 1;
        for el in trace['result']['structLogs']:
            print("%d: %s" %(el['pc'],el['op']))
            self.exec_op(el)

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
                print((r,g,b),hexv,execs)
                f.write("<div style='background-color:%s'>%s</div>" % (hexv,instr_str))

        f.close()

class Retina:

    def disassemble(self,code):
        bytecode = code[0].split("0x")[1]

        disasm = EVMDisAssembler()
        code = {};
        for opc in disasm.disassemble(bytecode):
            print("%d: %s" % (opc.address,opc));
            code[opc.address] = opc


        return code;

    def __init__(self,source,traces):
        self.code = self.disassemble(source)
        self.traces = {};
        for (ident,tr) in traces:
            self.traces[ident] = json.loads(tr)

    def coverage(self):
        coverage = CoverageMap(self.code);
        for ident in self.traces:
            print("-> proc %s" % ident)
            trace = self.traces[ident]
            coverage.exec_trace(trace)

        coverage.write('coverage')
        print("done")
