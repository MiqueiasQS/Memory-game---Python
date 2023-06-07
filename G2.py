import random
import os

def start_game():
    global memory, uncovered, score, name
    name = input("Informe o nome do jogador: ")

    score = 1000
    values = random.sample([0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7], 16)
    memory = [values[0:4], values[4:8], values[8:12], values[12:16]]
    uncovered = [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]]

def display_game():
    icons = ['😍', '🤨', '🤯', '💻', '👌', '🎓', '🤡', '💩']
    for i in range(0, 4):
        for j in range(0, 4):
            if uncovered[i][j] != False:
                print(icons[memory[i][j]], end='  ')
            else:
                print('⭕', end='  ')
        print()

def reveal_position(row, col):
    if uncovered[row][col] == False:
        uncovered[row][col] = True
        return True
    return False

def check_positions(row1, col1, row2, col2):
    global score
    if memory[row1][col1] == memory[row2][col2]:
        print('\nParabéns! Você acertou!')
        return True
    else:
        print('\nVocê errou. Tente novamente.')
        hide_positions(row1, col1, row2, col2)
        score -= 50
        return False

def hide_positions(row1, col1, row2, col2):
    uncovered[row1][col1] = False
    uncovered[row2][col2] = False

def check_victory():
    if score == 0:
        print('\nFim de jogo', name, '! Infelizmente seus pontos acabaram.')
        return True

    for i in range(0, 4):
        if False in uncovered[i]:
            return False

    print('\nParabéns', name, '! Você conseguiu descobrir todas as cartas, sua pontuação final é', score, '.')

    try:
        with open('pontuacoes.txt', 'a') as arquivo:
            arquivo.write(f'{name}: {score}\n')
    except IOError:
        print("Erro ao salvar pontuação: Ocorreu um erro ao acessar o arquivo.")
    
    return True

def display_ranking():
    try:
        with open('pontuacoes.txt', 'r') as arquivo:
            lines = arquivo.readlines()

        scores = {}
        for line in lines:
            name, score = line.strip().split(': ')
            score = int(score)
            scores[name] = scores.get(name, 0) + score

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        print("Ranking de Pontuações:")
        for i, (name, score) in enumerate(sorted_scores, start=1):
            print(f"{i}. {name}: {score}")
        print("\n\n\n")

    except FileNotFoundError:
        print("Arquivo de pontuações não encontrado.")
        print("\n\n\n")

def main():
    while True:
        print("Menu:")
        print("1. Apresentar ranking dos jogadores")
        print("2. Iniciar novo jogo")
        option = input("Escolha uma opção: ")

        if option == "1":
            display_ranking()
        elif option == "2":
            while True:
                try:
                    start_game()
                    r = list(range(0, 4))
                    while True:
                        os.system('cls || clear')
                        display_game()
                        while True:
                            try:
                                pos1 = list(input('\nEscolha a primeira posição x,y: '))
                                row1 = int(pos1[0])
                                col1 = int(pos1[2])
                                print()
                                if row1 not in r or col1 not in r:
                                    print("Posição inválida.")
                                    continue
                                if not reveal_position(row1, col1):
                                    print("Posição inválida.")
                                    continue
                                break
                            except ValueError:
                                print("Entrada inválida.")
                                continue

                        display_game()

                        while True:
                            try:
                                pos2 = list(input('\nEscolha a segunda posição x,y: '))
                                print()
                                row2 = int(pos2[0])
                                col2 = int(pos2[2])
                                if row2 not in r or col2 not in r:
                                    print("Posição inválida.")
                                    continue
                                if not reveal_position(row2, col2):
                                    print("Posição inválida ou já escolhida.")
                                    continue
                                break
                            except ValueError:
                                print("Entrada inválida.")
                                continue

                        display_game()
                        check_positions(row1, col1, row2, col2)
                        if check_victory():
                            break
                        input('\nPressione ENTER para continuar...')

                    optionPlayAgain = input("Deseja jogar novamente? (S/N): ")

                    if optionPlayAgain.upper() != "S":
                        break
                except BaseException as error:
                    print(f"Erro inesperado: {error}")
        else:
            print("Opção inválida. Tente novamente.")

main()
