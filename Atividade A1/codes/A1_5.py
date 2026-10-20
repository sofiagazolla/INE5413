import sys
import grafo

def floyd_warshall(g):
    n = grafo.qtd_vertices(g) # recebe grafo g
    
    # cria a matriz de distâncias (D) e preenche com infinito
    dist = []
    for i in range(n + 1):
        linha = [float('inf')] * (n + 1)
        dist.append(linha)
        
    # distância de um vértice para ele mesmo é 0, e para os vizinhos é o peso
    for i in range(1, n + 1):
        dist[i][i] = 0
        vizinhos = grafo.vizinhos(g, i)
        for v in vizinhos:
            dist[i][v] = grafo.peso_aresta(g, i, v)
            
    # os 3 laços de repetição do Floyd-Warshall
    for k in range(1, n + 1): # k atual como vértice intermediário que estamos testando
        for i in range(1, n + 1): # origem
            for j in range(1, n + 1): # destino
                soma = dist[i][k] + dist[k][j] # novo caminho passando por k 
                if soma < dist[i][j]: # verefica se novo caminho é mais curto 
                    dist[i][j] = soma # se sim atualiza
                    
    return dist

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Faltam parametros")
        sys.exit(1)
        
    arquivo_net = sys.argv[1]
    
    meu_grafo = grafo.criar_grafo()
    grafo.ler_arquivo(meu_grafo, arquivo_net)
    
    matriz_dist = floyd_warshall(meu_grafo)
    n = grafo.qtd_vertices(meu_grafo)
    
    # impressão no formato: "1:0,10,3,5"
    for i in range(1, n + 1):
        lista_str = []
        for j in range(1, n + 1):
            # transforma em int 
            # se a distância for infinita, tratamos apenas para não dar erro
            if matriz_dist[i][j] != float('inf'):
                valor = int(matriz_dist[i][j])
                lista_str.append(str(valor))
            else:
                lista_str.append("inf")
                
        linha_formatada = ",".join(lista_str)
        print(str(i) + ":" + linha_formatada)
