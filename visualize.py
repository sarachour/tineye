from contract import *
import seaborn as sns

class SummaryVis:
    def __init__(self):
        self._db = ContractDatabase();
        self._db.read();

    @property
    def db():
        return self._db

    def wallet_breakdown(output):
        vls = [];
        for addr in self.db.contracts:
            contract = self.db.contracts[addr]
            vls.append(contract.wallet);

        fig = sns.kdeplot(vls,shade=True)
        fig.safefig(output);
        raise("todo: wallet breakdown")

    def transaction_count_breakdown(contract_db):
        raise("todo: transaction count breakdown")

    def assembly_length_breakdown(contract_db):
        raise("todo")

    def source_avail_breakdown(contract_db):
        raise("todo");

    def source_length_breakdown(contract_db):
        raise("todo");

    def execute(name,output):
        if name == "wallet":
            self.wallet_breakdown(output);

        else:
            raise("unsupported:"+name)

