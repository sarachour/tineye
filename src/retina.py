import json;


class Retina:

    def __init__(self,source,traces):
        print(source)
        self.source = source;
        self.traces = {};
        for (ident,tr) in traces:
            print(ident)
            self.traces[ident] = json.loads(tr)

    def coverage(self):
        print("unimpl")
