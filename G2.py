#modulo para randomizar 
import random
import os

def iniciar_jogo():
    global memoria, descoberto, score, nome
    nome = input("Informe o nome do jogador: ")  # Coleta o nome do usuário

    score = 1000
    valores = random.sample([0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7], 16)
    memoria = [valores[0:4], valores[4:8], valores[8:12], valores[12:16]]
    descoberto = [[False, False, False, False],[False, False, False, False],[False, False, False, False],[False, False, False, False]]
    return

def exibir_jogo():
    icons = ['😍', '🤨', '🤯', '💻', '👌', '🎓', '🤡', '💩']
    for i in range(0, 4):
        for j in range(0, 4):
            if descoberto[i][j] != False:
                print(icons[(memoria[i][j])], end='  ')
            else:
                print('⭕', end='  ')
        print()
    
def revelar_posicao(l1, c1):
    if descoberto[l1][c1] == False:
        descoberto[l1][c1] = True
        return True
    return False

def checar_posicoes(l1, c1, l2, c2):
    global score
    if memoria[l1][c1] == memoria[l2][c2]:
        print('\nParabéns! Você acertou!')
        return True
    else:
        print('\nVocê errou. Tente novamente.')
        esconder_posicoes(l1, c1, l2, c2)
        score = score - 50
        return False
    
def esconder_posicoes(l1, c1, l2, c2):
    descoberto[l1][c1] = False
    descoberto[l2][c2] = False
    return

def checar_vitoria():
    if score == 0:
        print('\nFim de jogo',nome,'! Infelizmente seus pontos de score acabaram.')
        return True

    for i in range(0, 4):
        if False in descoberto[i]:
            return False
        
    print('\nParabéns',nome,'! Você conseguiu descobrir todas as cartas, seu score final é', score, '.')
    
    with open('pontuacoes.txt', 'a') as arquivo:
        arquivo.write(f'{nome}: {score}\n')
    return True

def apresentar_ranking():
    with open('pontuacoes.txt', 'r') as arquivo:
        linhas = arquivo.readlines()

    pontuacoes = {}
    for linha in linhas:
        nome, pontuacao = linha.strip().split(': ')
        pontuacao = int(pontuacao)
        pontuacoes[nome] = pontuacoes.get(nome, 0) + pontuacao

    pontuacoes_ordenadas = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)

    print("Ranking de Pontuações:")
    for i, (nome, pontuacao) in enumerate(pontuacoes_ordenadas, start=1):
        print(f"{i}. {nome}: {pontuacao}")
    print("\n\n\n")

def main():
    while True:
        print("Menu:")
        print("1. Apresentar ranking dos jogadores")
        print("2. Iniciar novo jogo")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            apresentar_ranking()
        elif opcao == "2":
            while True:
                iniciar_jogo()
                r = list(range(0, 4))
                while True:
                    os.system('cls || clear')
                    exibir_jogo()
                    while True:
                        pos1 = list(input('\nEscolha a primeira posição x,y: '))
                        l1 = int(pos1[0])
                        c1 = int(pos1[2])
                        print()
                        if l1 not in r or c1 not in r:
                            input('Posição inválida. Pressione ENTER para tentar novamente...')
                        elif not revelar_posicao(l1, c1):
                            input('Posição inválida. Pressione ENTER para tentar novamente...')
                        else:
                            break

                    exibir_jogo()

                    while True:
                        pos2 = list(input('\nEscolha a segunda posição x,y: '))
                        print()
                        l2 = int(pos2[0])
                        c2 = int(pos2[2])
                        if l2 not in r or c2 not in r:
                            input('Posição inválida. Pressione ENTER para tentar novamente...')
                        elif not revelar_posicao(l2, c2):
                            input('Posição inválida ou já escolhida. Pressione ENTER para tentar novamente...')
                        else:
                            break

                    exibir_jogo()
                    checar_posicoes(l1, c1, l2, c2)
                    if checar_vitoria():
                        break
                    input('\nPressione ENTER para continuar...')

                opcao_jogar_novamente = input("Deseja jogar novamente? (S/N): ")
                
                if opcao_jogar_novamente.upper() != "S":
                    break
        else:
            print("Opção inválida. Tente novamente.")

main()