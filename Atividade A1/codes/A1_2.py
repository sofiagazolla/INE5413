import sys
import grafo

def busca_em_largura(g, s):
    n = grafo.qtd_vertices(g)
    visitados = [False] * (n + 1)
    distancia = [float('inf')] * (n + 1)
    
    fila = []
    niveis = {} 
    
    fila.append(s)
    visitados[s] = True
    distancia[s] = 0
    niveis[0] = [s]
    
    while len(fila) > 0:
        u = fila.pop(0) 
        
        vizinhos_de_u = grafo.vizinhos(g, u)
        
        for v in vizinhos_de_u:
            if visitados[v] == False:
                visitados[v] = True
                distancia[v] = distancia[u] + 1
                
                d = distancia[v]
                if d not in niveis:
                    niveis[d] = []
                niveis[d].append(v)
                
                fila.append(v)
                
    return niveis

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Faltam parametros")
        sys.exit(1)
        
    arquivo_net = sys.argv[1]
    vertice_s = int(sys.argv[2])
    
    # Criamos o dicionário e passamos para a função ler
    meu_grafo = grafo.criar_grafo()
    grafo.ler_arquivo(meu_grafo, arquivo_net)
    
    resultado = busca_em_largura(meu_grafo, vertice_s)
    
    # Imprimindo níveis
    chaves = list(resultado.keys())
    chaves.sort()
    
    for nivel in chaves:
        lista_str = []
        for v in resultado[nivel]:
            lista_str.append(str(v))
        vertices_formatados = ",".join(lista_str)
        print(str(nivel) + ": " + vertices_formatados)
