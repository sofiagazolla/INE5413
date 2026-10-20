import sys
from collections import deque

class GrafoTopologico:
    def __init__(self):
        self.adj = {}
        self.vertices = {}
        self.grau_entrada = {}

    def carregar_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'r') as f:
            linhas = [l.strip() for l in f.readlines() if l.strip()]
        
        lendo_arcos = False
        for linha in linhas:
            if linha.startswith('*vertices'):
                continue
            if linha.startswith('*arcs') or linha.startswith('*edges'):
                lendo_arcos = True
                continue
            
            partes = linha.split()
            if not lendo_arcos:
                idx = int(partes[0])
                rotulo = " ".join(partes[1:]).replace('"', '')
                self.vertices[idx] = rotulo
                self.adj[idx] = []
                self.grau_entrada[idx] = 0
            else:
                u, v = int(partes[0]), int(partes[1])
                self.adj[u].append(v)
                self.grau_entrada[v] = self.grau_entrada.get(v, 0) + 1

def ordenacao_topologica(grafo):

    fila = deque([v for v in grafo.vertices if grafo.grau_entrada[v] == 0])
    ordem = []

    while fila:
        u = fila.popleft()
        ordem.append(grafo.vertices[u])
        
        for v in grafo.adj.get(u, []):
            grafo.grau_entrada[v] -= 1
            if grafo.grau_entrada[v] == 0:
                fila.append(v)

    return ordem

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)
        
    g = GrafoTopologico()
    g.carregar_arquivo(sys.argv[1])
    resultado = ordenacao_topologica(g)
    
    print(", ".join(resultado))