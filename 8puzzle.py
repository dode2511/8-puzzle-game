from heapq import heappop, heappush

# heuristica: contar as pessas na posicao errada

# calcula quantas peças estão na posicao errada
def contador_pecas_erradas(posicao, estado_final):
    erradas = 0
    for i in range(3):
        for j in range(3):
            if posicao[i][j] != estado_final[i][j]:
                erradas += 1
    return erradas

# obtem as jogadas possiveis
def movimentos_possieis(posicao):
    movimentos = []            #procura aonde esta o 0 
    linha_vazia, coluna_vazia = next((i, j) for i, linha in enumerate(posicao) for j, val in enumerate(linha) if val == 0)
    
    # movimentos possiveis para o 0 (direita,esquerda,cima,baixo)
    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]  
    for dl, dc in deltas:
        nova_linha, nova_coluna = linha_vazia + dl, coluna_vazia + dc
        if 0 <= nova_linha < 3 and 0 <= nova_coluna < 3:
            nova_posicao = [row[:] for row in posicao]
            nova_posicao[linha_vazia][coluna_vazia], nova_posicao[nova_linha][nova_coluna] = nova_posicao[nova_linha][nova_coluna], nova_posicao[linha_vazia][coluna_vazia]
            movimentos.append(nova_posicao)
    return movimentos

# comeca o jogo
def jogo_8puzzle(estado_inicial, estado_final):
    # inicializa a lista aberta (estados nao vizitados)
    lista_aberta = [(contador_pecas_erradas(estado_inicial, estado_final), estado_inicial)]
    # guarda o caminho de cada no
    caminho_do_no = {}
    # armazena o custo do caminho (distancia do estado inical)
    custo_caminho = {tuple(map(tuple, estado_inicial)): 0}
    
    while lista_aberta:
        _, estado_atual = heappop(lista_aberta)
        
        # verifica se o estado atual é o estado final caso seja , reconstroi o caminho 
        if estado_atual == estado_final:
            caminho = []
            while estado_atual != estado_inicial:
                caminho.append(estado_atual)
                estado_atual = caminho_do_no[tuple(map(tuple, estado_atual))]
            caminho.append(estado_inicial)
            return caminho[::-1]
        
        for proximo_estado in movimentos_possieis(estado_atual):
            
            custo_caminho_atual = custo_caminho[tuple(map(tuple, estado_atual))] + 1
            
            if (tuple(map(tuple, proximo_estado)) not in custo_caminho) or (custo_caminho_atual < custo_caminho[tuple(map(tuple, proximo_estado))]):
                
                caminho_do_no[tuple(map(tuple, proximo_estado))] = estado_atual
                custo_caminho[tuple(map(tuple, proximo_estado))] = custo_caminho_atual
                
                # calcula o custo total (custo do caminho + heuristica) para o proximo estado (vizinho)
                custo_total = custo_caminho_atual + contador_pecas_erradas(proximo_estado, estado_final)
                # adiciona o proximo estado  na lista aberta 
                heappush(lista_aberta, (custo_total, proximo_estado))

# inicio do jogo
estado_inicial = [[1, 0, 3],
                  [4, 2, 5],
                  [7, 8, 6]]

# final do jogo
estado_final = [[1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]]

caminho = jogo_8puzzle(estado_inicial, estado_final)

if caminho:
    print("Caminho:")
    for estado in caminho:
        for linha in estado:
            print(*linha)
        print()
else:
    print("Erro: Não foi possível encontrar uma solução.")

