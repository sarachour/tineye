from contract import *
import seaborn as sns
import numpy as np
import pandas as pd
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

    def write(self,f):
        for i in range(0,self.n):
            row = "";
            for h in self.header:
                c = self.rows[h][i];
                row += str(c)+","
            f.write(row+"\n")

class SummaryVis:
    def __init__(self):
        self._db = ContractDatabase();
        self._db.read();

    @property
    def db(self):
        return self._db

    def general_breakdown(self,output):
        header = [ "addr","name","wallet","txns_internal","txns_external","mined", \
                  "has_source","compiler","optimized","suicide"];
        tbl = Table(header);

        for addr in self.db.contracts:
            self.db.read_details(addr);
            contract = self.db.contracts[addr]
            details = self.db.details(addr).info

            print(str(details))
            if self.db.details(addr).info.exists == False:
                raise("general_breakdown: no code for "+addr)

            tbl.add_cell("wallet",contract.wallet);
            tbl.add_cell("txns_internal",details.int_txns);
            tbl.add_cell("txns_external",details.txns);
            tbl.add_cell("mined",details.mined);
            tbl.add_cell("name",details.name);
            tbl.add_cell("optimized", details.is_optimized);
            tbl.add_cell("compiler", details.compiler_version);
            tbl.add_cell("has_source", not (details.compiler_version == None));
            tbl.finish_row();
            
        f = open(output+".txt","w+")
        tbl.write(f);

    # emit snapshot wallet
    def txns_breakdown(self,output):
        tvls = [];
        wvls = [];
	addrs = [];

        for addr in self.db.contracts:
            contract = self.db.contracts[addr]
            tvls.append(contract.wallet);
            wvls.append(contract.txs);
	    addrs.append(addr)

	pairs = sorted(zip(addrs,tvls,wvls), key=lambda (k,t,v) : t);

        f = open(output+".txt","w+");
	for (addr,tvl,wvl) in pairs:
		f.write(addr+","+str(tvl)+","+str(wvl)+"\n");



        snsplot = sns.distplot(np.array(tvls));
        snsplot.set(xlabel="Num of Txns")
        snsplot.set(ylabel="Proportion")
        snsplot.set(xlim=(0,100000));
        fig = snsplot.get_figure()
        fig.savefig(output+"_hist"+".png");

        df = pd.DataFrame();
        df["x"] = tvls;
        df["y"] = wvls;
        snsplot = sns.lmplot("x","y",data=df,fit_reg=False);
        snsplot.set(xlim=(0,100000));
        snsplot.set(ylim=(0,100000));
        snsplot.set(xlabel="Num of Txns")
        snsplot.set(ylabel="Size of Wallet")
        snsplot.savefig(output+"_scatter"+".png");

    # emit snapshot wallet
    def wallet_breakdown(self,output):
        vls = [];
        pvls = [];
	addrs = [];

        for addr in self.db.contracts:
            contract = self.db.contracts[addr]
            pvls.append(contract.pctmarket);
            vls.append(contract.wallet);
	    addrs.append(addr)

	pairs = sorted(zip(addrs,vls,pvls), key=lambda (k,v,p) : v);

        f = open(output+".txt","w+");
	for (addr,vl,pct) in pairs:
		f.write(addr+","+str(vl)+","+str(pct)+"\n");


	vls_plot = filter(lambda v: v < 1000 and v > 5, vls);

        #snsplot = sns.boxplot(np.array(vls),showfliers=False);
        #snsplot = sns.boxplot(np.array(vls));
        snsplot = sns.distplot(np.array(vls_plot),bins=40);
        #snsplot = sns.boxplot(np.array(vls));
        #snsplot = sns.kdeplot(np.array(vls),shade=True)
        #snsplot.set(xlim=(0,1000))
        snsplot.set(xlabel="Ether in Wallet")
        snsplot.set(ylabel="Number of Contracts")
        fig = snsplot.get_figure()
        fig.savefig(output+".png");

    def execute(self,name,output):
        if name == "wallet":
            self.wallet_breakdown(output);

        if name == "txns":
            self.txns_breakdown(output);

        if name == "general":
            self.general_breakdown(output);

        else:
            raise("unsupported:"+name)

