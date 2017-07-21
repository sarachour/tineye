
class Table:
    def __init__(self,header):
        self.header = header;
        self.n = 1;
        self.rows = {};
        for h in header:
            self.init_row(h);

    def init_row(self,header):
        self.rows[header] = [];
        self.rows[header].append(header);

    def add_cell(self,header,v):
        self.rows[header].append(v);
        if len(self.rows[header]) > self.n:
            self.n = len(self.rows[header]);

    def finish_row(self):
        for header in self.rows:
            r = self.rows[header];
            while len(self.rows[header]) < self.n:
                self.add_cell(header,None);

    def write(self,fn):
        f = open(fn,"w+");
        for i in range(0,self.n):
            row = "";
            for h in self.header:
                c = self.rows[h][i];
                row += str(c)+","
            f.write(row+"\n")
