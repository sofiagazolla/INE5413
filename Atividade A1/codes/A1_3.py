import sys
import grafo

# só possui um ciclo Euleriano se e somente se todos os seus vértices possuem grau par
def verificar_grau_par(g):
    n = grafo.qtd_vertices(g)
    for i in range(1, n + 1):
        vizinhos = grafo.vizinhos(g, i)
        if len(vizinhos) % 2 != 0: # pega qntd de vizinhos e faz %2, se != 2 -> impar
            return False
    return True

def ciclo_euleriano(g):
    # se tiver algum grau ímpar, já sabemos que não tem ciclo
    if verificar_grau_par(g) == False:
        return 0, []

    n = grafo.qtd_vertices(g)
    
    # fazemos uma cópia das adjacências porque o algoritmo de Hierholzer "destrói" as arestas por onde passa.
    adj_copia = {}
    total_arestas = 0
    for i in range(1, n + 1):
        adj_copia[i] = grafo.vizinhos(g, i)
        total_arestas += len(adj_copia[i])
    # como o grafo é não-dirigido, cada aresta foi contada duas vezes
    total_arestas = total_arestas // 2

    # se não tem arestas, não tem ciclo
    if total_arestas == 0:
        return 0, []

    # acha o primeiro vértice que tenha arestas para começar
    inicio = 1
    for i in range(1, n + 1):
        if len(adj_copia[i]) > 0:
            inicio = i
            break

    pilha = [inicio] # incia pilha de exploração com vértice de inicio 
    ciclo = [] # vai guardar resposta final

    # algoritmo de Hierholzer iterativo
    while len(pilha) > 0: # enquanto pilha nao esta vazia
        u = pilha[-1] # pega o elemento no topo da pilha
        
        # se o vértice ainda tem vizinhos para visitar
        if len(adj_copia[u]) > 0:
            v = adj_copia[u][0] # Pega o primeiro vizinho
            
            # remove a aresta de ida (u -> v)
            adj_copia[u].pop(0)
            
            # remove a aresta de volta (v -> u)
            for i in range(len(adj_copia[v])):
                if adj_copia[v][i] == u:
                    adj_copia[v].pop(i)
                    break
                    
            pilha.append(v) # adicionamos v no topo da pilha
        else:
            # se não tem mais para onde ir, remove da pilha e põe no ciclo
            ciclo.append(pilha.pop())

    # o ciclo é montado de trás pra frente, então invertemos
    ciclo.reverse()

    # verificação de grafo desconexo
    # se o tamanho do ciclo (menos 1) for diferente do total de arestas, 
    # significa que o grafo era desconexo e sobraram arestas para trás.
    if len(ciclo) - 1 != total_arestas:
        return 0, []

    return 1, ciclo

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Faltam parametros")
        sys.exit(1)
        
    arquivo_net = sys.argv[1]
    
    meu_grafo = grafo.criar_grafo()
    grafo.ler_arquivo(meu_grafo, arquivo_net)
    
    tem_ciclo, caminho = ciclo_euleriano(meu_grafo)
    
    # Imprime a primeira linha (1 ou 0)
    print(str(tem_ciclo))
    
    # Se tem ciclo (1), imprime o caminho na segunda linha
    if tem_ciclo == 1:
        lista_str = []
        for no in caminho:
            lista_str.append(str(no))
        caminho_formatado = ",".join(lista_str)
        print(caminho_formatado)
