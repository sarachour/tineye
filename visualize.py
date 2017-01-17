from contract import *
import seaborn as sns
import numpy as np

class SummaryVis:
    def __init__(self):
        self._db = ContractDatabase();
        self._db.read();

    @property
    def db(self):
        return self._db

    def wallet_breakdown(self,output):
        vls = [];
        empty = 0;
        nonempty = 0;
        for addr in self.db.contracts:
            contract = self.db.contracts[addr]
            if contract.wallet > 0:
                vls.append(contract.wallet);
                nonempty += 1;
            else:
                empty += 1;

        print("empty wallets:"+str(empty));
        print("nonempty wallets:"+str(nonempty))
        #snsplot = sns.boxplot(np.array(vls),showfliers=False);
        #snsplot = sns.boxplot(np.array(vls));
        snsplot = sns.distplot(np.array(vls));
        #snsplot = sns.boxplot(np.array(vls));
        #snsplot = sns.kdeplot(np.array(vls),shade=True)
        #snsplot.set(xscale='log')
        #snsplot.set(xlim=(0,1000))
        snsplot.set(xlabel="Ether in Wallet")
        fig = snsplot.get_figure()
        fig.savefig(output);

    def execute(self,name,output):
        if name == "wallet":
            self.wallet_breakdown(output);

        else:
            raise("unsupported:"+name)

