import sys

class DSU:
    def __init__(self, n):
        self.pai = list(range(n + 1))
        self.rank = [0] * (n + 1)

    def find(self, i):
        if self.pai[i] == i:
            return i
        self.pai[i] = self.find(self.pai[i])
        return self.pai[i]

    def union(self, i, j):
        raiz_i = self.find(i)
        raiz_j = self.find(j)
        if raiz_i != raiz_j:
            if self.rank[raiz_i] < self.rank[raiz_j]:
                self.pai[raiz_i] = raiz_j
            elif self.rank[raiz_i] > self.rank[raiz_j]:
                self.pai[raiz_j] = raiz_i
            else:
                self.pai[raiz_j] = raiz_i
                self.rank[raiz_i] += 1
            return True
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)

    arestas = []
    num_vertices = 0

    with open(sys.argv[1], 'r') as f:
        linhas = [l.strip() for l in f.readlines() if l.strip()]

    lendo_arestas = False
    for linha in linhas:
        if linha.startswith('*vertices'):
            num_vertices = int(linha.split()[1])
            continue
        if linha.startswith('*edges') or linha.startswith('*arcs'):
            lendo_arestas = True
            continue
        
        partes = linha.split()
        if lendo_arestas and len(partes) >= 3:
            u, v, peso = int(partes[0]), int(partes[1]), float(partes[2])
            arestas.append((peso, u, v))

    arestas.sort(key=lambda x: x[0])
    dsu = DSU(num_vertices)
    
    peso_total = 0.0
    arestas_agm = []

    for peso, u, v in arestas:
        if dsu.union(u, v):
            peso_total += peso
            arestas_agm.append(f"{u}-{v}")

    print(peso_total)
    print(", ".join(arestas_agm))