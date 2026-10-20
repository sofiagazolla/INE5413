import sys
import grafo

def dijkstra(g, s): # recebe grafo e vértice de origem 
    n = grafo.qtd_vertices(g)
    dist = [float('inf')] * (n + 1) # cria lista para guardar menores distâncias 
    ant = [None] * (n + 1) # cria lista de antecessores 
    visitados = [False] * (n + 1) # cria lista de visitados para marcar quem já teve vizinhos visitados
    
    dist[s] = 0 # a distância da origem para ela mesmo é zero
    
    for _ in range(n): # passa por todos os vértices
        u = None # vértice da vez 
        menor_distancia = float('inf')
        
        # busca o menor vértice não visitado
        for i in range(1, n + 1): # passa por todos os vértices 
            if visitados[i] == False and dist[i] < menor_distancia: # procurando os que não foram visitados,
                # e tem menor distância acumulada até o momento
                menor_distancia = dist[i]
                u = i 
                
        if u == None: # se ao final da busca o u continuar none -> vértices restantes são inatingíveis
            break
            
        visitados[u] = True # marca vértice escolhido como visitado
        vizinhos_de_u = grafo.vizinhos(g, u) # pega lista dos vizinhos 
        
        for v in vizinhos_de_u: # para cada vizinho v de u
            peso_uv = grafo.peso_aresta(g, u, v) # verifica o peso da aresta entre u e v
            if dist[v] > dist[u] + peso_uv: # se a distância atual p/ chegar em v for maior que passando por u
                dist[v] = dist[u] + peso_uv # atualiza v com valor menor  
                ant[v] = u # registra que para chegar em v com essa distância mínima o passo anterior foi u
                
    return dist, ant

def recuperar_caminho(ant, destino):
    caminho = [] # cria lista vazia para recosntruir caminho
    atual = destino # define ponto atual como destino
    while atual != None:
        caminho.append(atual) # refaz caminho de "ré"
        atual = ant[atual]
        
    caminho.reverse() # invertemos a lista para rota ficar certa
    return caminho

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Faltam parametros")
        sys.exit(1)
        
    arquivo_net = sys.argv[1]
    vertice_s = int(sys.argv[2])
    
    meu_grafo = grafo.criar_grafo()
    grafo.ler_arquivo(meu_grafo, arquivo_net)
    
    distancias, predecessores = dijkstra(meu_grafo, vertice_s)
    
    n = grafo.qtd_vertices(meu_grafo)
    for v in range(1, n + 1):
        caminho = recuperar_caminho(predecessores, v)
        lista_str = []
        for no in caminho:
            lista_str.append(str(no))
            
        caminho_formatado = ",".join(lista_str)
        
        # verifica se a distância não é infinita antes de converter para inteiro
        if distancias[v] != float('inf'):
            dist_formatada = str(int(distancias[v]))
        else:
            dist_formatada = "inf"
            
        print(str(v) + ": " + caminho_formatado + "; d=" + dist_formatada)