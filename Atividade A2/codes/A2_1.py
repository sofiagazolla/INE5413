import sys

class GrafoDirigido:
    def __init__(self):
        self.adj = {}
        self.vertices = {}

    def carregar_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'r') as f:
            linhas = [l.strip() for l in f.readlines() if l.strip()]
        
        lendo_arcos = False
        for linha in lines_parser(linhas):
            if linha.startswith('*vertices'):
                continue
            if linha.startswith('*arcs') or linha.startswith('*edges'):
                lendo_arcos = True
                continue
            
            partes = linha.split()
            if not lendo_arcos:
                idx = int(partes[0])
                rotulo = " ".join(partes[1:])
                self.vertices[idx] = rotulo
                if idx not in self.adj:
                    self.adj[idx] = []
            else:
                u, v = int(partes[0]), int(partes[1])
                if u not in self.adj:
                    self.adj[u] = []
                if v not in self.adj:
                    self.adj[v] = []
                self.adj[u].append(v)

def lines_parser(linhas):
    return linhas

def tarjan_scc(grafo):
    index = 0
    stack = []
    indices = {}
    lowlink = {}
    on_stack = {}
    sccs = []

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack[v] = True

        for w in grafo.adj.get(v, []):
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif on_stack.get(w, False):
                lowlink[v] = min(lowlink[v], indices[w])

        if lowlink[v] == indices[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                scc.append(w)
                if w == v:
                    break
            sccs.append(sorted(scc))

    for v in grafo.vertices.keys():
        if v not in indices:
            strongconnect(v)
    return sccs

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)
    
    g = GrafoDirigido()
    g.carregar_arquivo(sys.argv[1])
    sccs = tarjan_scc(g)
    
    for scc in sorted(sccs, key=lambda x: x[0]):
        print(",".join(map(str, scc)))