import plotly;

class SummaryVis:

    def wallet_breakdown(contract_db):
        raise("todo: wallet breakdown")

    def transaction_count_breakdown(contract_db):
        raise("todo: transaction count breakdown")

    def assembly_length_breakdown(contract_db):
        raise("todo")

    def source_avail_breakdown(contract_db):
        raise("todo");

    def source_length_breakdown(contract_db):
        raise("todo");

    def execute(name,db):
        if name == "wallet":
            self.wallet_breakdown(db);
        elif name == "txns":
            self.transaction_count_breakdown(db);
        else:
            raise("unsupported:"+name)

