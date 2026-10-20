import sys

def carregar_grafo(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = [l.strip() for l in f.readlines() if l.strip()]
    n = int(linhas[0].split()[1])
    adj = {i: set() for i in range(1, n + 1)}
    for linha in linhas:
        if linha.startswith('*') or not linha: continue
        u, v = map(int, linha.split()[:2])
        adj[u].add(v)
        adj[v].add(u)
    return n, adj

def conjuntos_independentes_maximais(subconjunto, adj_bits):
    resultado = []

    def bk(escolhidos, candidatos, descartados):
        if candidatos == 0 and descartados == 0:
            resultado.append(escolhidos)
            return

        restantes = candidatos
        while restantes:
            bit_vertice = restantes & (-restantes)   # pega o proximo candidato -> bit menos significativo
            vertice = bit_vertice.bit_length() - 1     # indice do vertice correspondente a esse bit

            nao_vizinhos = subconjunto & ~adj_bits[vertice] & ~bit_vertice  # quem nao conflita com esse vertice

            bk(escolhidos | bit_vertice,
               candidatos & nao_vizinhos,
               descartados & nao_vizinhos)

            candidatos &= ~bit_vertice   # vertice ja foi testado, tira dos candidatos
            descartados |= bit_vertice   # marca para nao testar dnv
            restantes &= ~bit_vertice    # avanca pro proximo candidato do while

    bk(escolhidos=0, candidatos=subconjunto, descartados=0)
    return resultado

def lawler(n, adj):
    adj_bits = [0] * n
    for i in range(n):
        for viz in adj[i + 1]:
            adj_bits[i] |= (1 << (viz - 1))

    numero_cromatico = {0: 0}  # numero_cromatico[subconjunto] = qtd minima de cores pra colorir esse subconjunto
    conjunto_escolhido = {}     # conjunto_escolhido[subconjunto] = qual independente maximal gerou o valor otimo

    def resolver(subconjunto):
        # testa remover cada independente maximal e fica com a opcao que gastar menos cores
        if subconjunto in numero_cromatico:
            return numero_cromatico[subconjunto]

        melhor_valor, melhor_conjunto = float('inf'), None
        for independente in conjuntos_independentes_maximais(subconjunto, adj_bits):
            valor = 1 + resolver(subconjunto ^ independente)
            if valor < melhor_valor:
                melhor_valor, melhor_conjunto = valor, independente

        numero_cromatico[subconjunto] = melhor_valor
        conjunto_escolhido[subconjunto] = melhor_conjunto
        return melhor_valor

    todos_vertices = (1 << n) - 1
    total_cores = resolver(todos_vertices)

    # reconstroi a coloracao seguindo as escolhas guardadas
    cores = [0] * (n + 1)
    subconjunto = todos_vertices
    cor_atual = 1
    while subconjunto > 0:
        independente = conjunto_escolhido[subconjunto]
        for i in range(n):
            if independente & (1 << i):
                cores[i + 1] = cor_atual
        subconjunto ^= independente
        cor_atual += 1

    return total_cores, cores

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)
    n, adj = carregar_grafo(sys.argv[1])
    min_cores, atribuicao = lawler(n, adj)
    print(min_cores)
    print(", ".join(map(str, atribuicao[1:])))