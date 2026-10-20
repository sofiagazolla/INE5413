# grafo.py - Biblioteca Base UFSC
def criar_grafo():
    return {
        'n': 0, # qtd vértices 
        'm': 0, # qtd arestas 
        'rotulos': {}, # rótulos 
        'adj': {} # lista de adjacência (Dicionário de Dicionários)
    }

def ler_arquivo(grafo, nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = f.readlines()
    
    lendo_arestas = False
    for linha in linhas:
        linha = linha.strip()
        if not linha: continue
        
        if linha.startswith("*vertices"):
            grafo['n'] = int(linha.split()[1])
            for i in range(1, grafo['n'] + 1):
                grafo['adj'][i] = {}
        elif linha.startswith("*edges"):
            lendo_arestas = True
        elif not lendo_arestas:
            partes = linha.split(" ", 1)
            u = int(partes[0])
            grafo['rotulos'][u] = partes[1] if len(partes) > 1 else ""
        else:
            u, v, peso = linha.split()
            u, v, peso = int(u), int(v), float(peso)
            grafo['adj'][u][v] = peso
            grafo['adj'][v][u] = peso
            grafo['m'] += 1

# --- MÉTODOS OBRIGATÓRIOS (Questão 1) --- 

def qtdVertices(grafo):
    return grafo['n']

def qtdArestas(grafo):
    return grafo['m']

def grau(grafo, v):
    return len(grafo['adj'][v])

def rotulo(grafo, v):
    return grafo['rotulos'].get(v, str(v))

def vizinhos(grafo, v):
    return list(grafo['adj'][v].keys())

def haAresta(grafo, u, v):
    return v in grafo['adj'][u]

def peso(grafo, u, v):
    if v in grafo['adj'][u]:
        return grafo['adj'][u][v]
    return float('inf') # valor infinito conforme nota 

def qtd_vertices(g): return qtdVertices(g)
def peso_aresta(g, u, v): return peso(g, u, v)