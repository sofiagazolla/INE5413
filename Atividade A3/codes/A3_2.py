import sys
from collections import deque

class HopcroftKarp:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.pair_u = [0] * (n + 1)  # pareamento atual do lado esquerdo
        self.pair_v = [0] * (n + 1)  # pareamento atual do lado direito
        self.dist = [0] * (n + 1)

    def add_edge(self, u, v):
        self.adj[u].append(v)

    def bfs(self):
        # constroi as camadas por distancia a partir dos vertices livres
        queue = deque()
        for u in range(1, self.n // 2 + 1):
            if self.pair_u[u] == 0:
                self.dist[u] = 0
                queue.append(u)
            else:
                self.dist[u] = float('inf')
        self.dist[0] = float('inf')

        while queue:
            u = queue.popleft()
            if self.dist[u] < self.dist[0]:
                for v in self.adj[u]:
                    if self.dist[self.pair_v[v]] == float('inf'):
                        self.dist[self.pair_v[v]] = self.dist[u] + 1
                        queue.append(self.pair_v[v])
        return self.dist[0] != float('inf')

    def dfs(self, u):
        # busca caminho aumentante respeitando as camadas do bfs
        if u != 0:
            for v in self.adj[u]:
                if self.dist[self.pair_v[v]] == self.dist[u] + 1:
                    if self.dfs(self.pair_v[v]):
                        self.pair_v[v] = u
                        self.pair_u[u] = v
                        return True
            self.dist[u] = float('inf')  # evita reprocessar esse vertice na fase atual
            return False
        return True

    def max_matching(self):
        matching = 0
        while self.bfs():
            for u in range(1, self.n // 2 + 1):
                if self.pair_u[u] == 0:
                    if self.dfs(u):
                        matching += 1
        return matching

def carregar_grafo(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = [l.strip() for l in f.readlines() if l.strip()]
    
    n = int(linhas[0].split()[1])
    hk = HopcroftKarp(n)
    
    lendo_arestas = False
    for linha in linhas:
        if linha.startswith('*edges') or linha.startswith('*arcs'):
            lendo_arestas = True
            continue
        if lendo_arestas:
            u, v = map(int, linha.split()[:2])
            hk.add_edge(u, v)
    return hk

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)
        
    hk = carregar_grafo(sys.argv[1])
    matching_size = hk.max_matching()
    
    # imprime quantidade
    print(matching_size)
    
    # imprime arestas
    arestas = []
    for u in range(1, hk.n // 2 + 1):
        if hk.pair_u[u] != 0:
            arestas.append(f"{u}-{hk.pair_u[u]}")
    print(", ".join(arestas))