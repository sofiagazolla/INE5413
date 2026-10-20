import sys
from collections import deque

class GrafoFluxo:
    def __init__(self):
        self.capacidade = {}
        self.vertices = set()

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
                self.vertices.add(int(partes[0]))
            else:
                u, v, cap = int(partes[0]), int(partes[1]), float(partes[2])
                if u not in self.capacidade: self.capacidade[u] = {}
                if v not in self.capacidade: self.capacidade[v] = {}
                self.capacidade[u][v] = cap
                if u not in self.capacidade[v]: self.capacidade[v][u] = 0.0  # arco reverso p/ desfazer fluxo depois

def bfs(capacidade, s, t, parent):
    # busca caminho de s até t usando só arcos com capacidade residual > 0
    parent.clear()
    parent[s] = s
    fila = deque([s])
    while fila:
        u = fila.popleft()
        for v, cap in capacidade.get(u, {}).items():
            if v not in parent and cap > 0:
                parent[v] = u
                if v == t: return True
                fila.append(v)
    return False

def edmonds_karp(grafo, s, t):
    fluxo_total = 0
    parent = {}
    
    while bfs(grafo.capacidade, s, t, parent):
        # calcula o fluxo do caminho encontrado
        path_flow = float('inf')
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, grafo.capacidade[u][v])
            v = u
            
        fluxo_total += path_flow
        
        # atualiza capacidades residuais (direta e reversa)
        v = t
        while v != s:
            u = parent[v]
            grafo.capacidade[u][v] -= path_flow
            grafo.capacidade[v][u] += path_flow
            v = u
            
    return fluxo_total

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(1)
    
    g = GrafoFluxo()
    g.carregar_arquivo(sys.argv[1])
    s, t = int(sys.argv[2]), int(sys.argv[3])
    resultado = edmonds_karp(g, s, t)
    
    print(resultado)