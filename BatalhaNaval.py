import random
import os
import time

# Configurações do Jogo
LARGURA_TABULEIRO = 10
ALTURA_TABULEIRO = 10
NUMERO_DE_NAVIOS = 5

# Símbolos do Tabuleiro
AGUA = "~"
NAVIO = "N"
ACERTO = "X"
ERRO = "O"


def criar_tabuleiro():
    return [[AGUA for _ in range(LARGURA_TABULEIRO)] for _ in range(ALTURA_TABULEIRO)]


def imprimir_tabuleiro(tabuleiro, nome_jogador, ocultar_navios=False):
    print(f"--- Tabuleiro de {nome_jogador} ---")
    # Desenha numeros das colunas
    print("   " + " ".join([str(i) for i in range(LARGURA_TABULEIRO)]))
    # Desenha topo do tabuleiro
    print("  " + "-" * (LARGURA_TABULEIRO * 2 + 1))

    #Desenha pipe para esquerda e direita do tabuleiro,numero da linha, agua
    for i, linha in enumerate(tabuleiro):
        print(f"{i}| ", end="")
        for celula in linha:
            if ocultar_navios and celula == NAVIO:
                print(f"{AGUA} ", end="")
            else:
                print(f"{celula} ", end="")
        print("|")
    # Desenha parte de baixo do tabuleiro
    print("  " + "-" * (LARGURA_TABULEIRO * 2 + 1))
    print()


def posicionar_navios_aleatoriamente(tabuleiro, numero_navios):
    navios_posicionados = 0
    # Faz verificação de quantidade de navios posicionados, e para quando atinge o valor configurado
    while navios_posicionados < numero_navios:
        x = random.randint(0, LARGURA_TABULEIRO - 1)
        y = random.randint(0, ALTURA_TABULEIRO - 1)
        if tabuleiro[y][x] == AGUA:
            tabuleiro[y][x] = NAVIO
            navios_posicionados += 1


def posicionar_navios_jogador(tabuleiro, numero_navios, nome_jogador):
    for i in range(numero_navios):
        while True:
            limpar_tela()
            imprimir_tabuleiro(tabuleiro, nome_jogador)
            print(f"Posicione seu navio Nº {i + 1} de {numero_navios}.")

            # Maneira de fazer o programa verificar se dado inserido pelo usuario é um numero
            # sem utilizar tratamento de excessão e evitar que o programa termine
            while True:
                input_x = input(f"Digite a coordenada X (coluna 0-{LARGURA_TABULEIRO - 1}): ")
                if input_x.isdigit():
                    x = int(input_x)
                    break
                else:
                    print("Entrada inválida. Por favor, digite um número.")

            while True:
                input_y = input(f"Digite a coordenada Y (linha 0-{ALTURA_TABULEIRO - 1}): ")
                if input_y.isdigit():
                    y = int(input_y)
                    break
                else:
                    print("Entrada inválida. Por favor, digite um número.")

            # Verifica se coordenadas estão dentro das medidas da matriz
            if not (0 <= x < LARGURA_TABULEIRO and 0 <= y < ALTURA_TABULEIRO):
                print("\nCoordenada fora do tabuleiro! Tente novamente.")
                time.sleep(2)
                continue

            # Verifica se ja possui navio dentro dessa coordenada
            if tabuleiro[y][x] != AGUA:
                print("\nLocal já ocupado por outro navio! Tente novamente.")
                time.sleep(2)
                continue

            # Seta posição do navio caso não haja nenhum erro
            tabuleiro[y][x] = NAVIO
            break


def ataque_do_jogador(tabuleiro_oponente, nome_jogador):
    while True:
        print(f"\nSua vez de atacar, {nome_jogador}!")

        # Novamente verifica se o dado inserido é um numero
        while True:
            input_x = input(f"Digite a coordenada X do seu alvo (coluna 0-{LARGURA_TABULEIRO - 1}): ")
            if input_x.isdigit():
                x = int(input_x)
                break
            else:
                print("Entrada inválida. Por favor, digite um número.")

        # Novamente verifica se o dado inserido é um numero
        while True:
            input_y = input(f"Digite a coordenada Y do seu alvo (linha 0-{ALTURA_TABULEIRO - 1}): ")
            if input_y.isdigit():
                y = int(input_y)
                break
            else:
                print("Entrada inválida. Por favor, digite um número.")

        # Novamente verifica se coordenadas estão dentro da medida do tabuleiro
        if not (0 <= x < LARGURA_TABULEIRO and 0 <= y < ALTURA_TABULEIRO):
            print("Coordenada fora do tabuleiro! Tente novamente.")
            continue

        # Verifica se ja foi realizado um disparo na posição digitada
        if tabuleiro_oponente[y][x] in [ACERTO, ERRO]:
            print("Você já atirou aí! Escolha outra coordenada.")
            continue

        return x, y


# Função para realizar um disparo aleatorio dentro das coordenadas do tabuleiro
# Continua sorteando infinitamente até que os valores não sejam ja utilizados anteriormente
def ataque_da_maquina(tabuleiro_oponente):
    while True:
        x = random.randint(0, LARGURA_TABULEIRO - 1)
        y = random.randint(0, ALTURA_TABULEIRO - 1)
        if tabuleiro_oponente[y][x] not in [ACERTO, ERRO]:
            return x, y


def verificar_vitoria(tabuleiro):
    # Faz uma verificação do tabuleiro para verificar a existencia de navios
    for linha in tabuleiro:
        if NAVIO in linha:
            return False
    return True

# Função para limpar a tela do console deixando a experiencia mais facil de entender e "limpa"
def limpar_tela():
    os.system('cls')


def main():
    limpar_tela()
    print("------ ⚓ BATALHA NAVAL ⚓ ------")

    nome_jogador = input("Qual é o seu nome? ")

    tabuleiro_jogador = criar_tabuleiro()
    tabuleiro_maquina = criar_tabuleiro()

    posicionar_navios_aleatoriamente(tabuleiro_maquina, NUMERO_DE_NAVIOS)
    posicionar_navios_jogador(tabuleiro_jogador, NUMERO_DE_NAVIOS, nome_jogador)

    limpar_tela()
    print("Todos os navios estão posicionados. Que comece a batalha!")
    # Faz que o programa tenha uma contagem de 3 segundos para rodar a próxima linha.
    time.sleep(3)

    while True:
        limpar_tela()
        imprimir_tabuleiro(tabuleiro_maquina, "Máquina", ocultar_navios=True)
        imprimir_tabuleiro(tabuleiro_jogador, nome_jogador)

        x, y = ataque_do_jogador(tabuleiro_maquina, nome_jogador)

        if tabuleiro_maquina[y][x] == NAVIO:
            print("\n>>> ACERTOU! Você atingiu um navio inimigo! <<<")
            tabuleiro_maquina[y][x] = ACERTO
            if verificar_vitoria(tabuleiro_maquina):
                print(f"\n🎉 PARABÉNS, {nome_jogador}! VOCÊ VENCEU A BATALHA! 🎉")
                imprimir_tabuleiro(tabuleiro_maquina, "Máquina")
                print("Agradecemos por jogar! Trabalho feito por:")
                print("- Carlos Eduardo Wille Martins")
                print("- Raul Castelnou")
                print("- Wlademir Alves de Souza")

                break
        else:
            print("\n>>> ÁGUA! Você errou o alvo. <<<")
            tabuleiro_maquina[y][x] = ERRO

        time.sleep(2)

        print("\nAgora é a vez da Máquina...")
        time.sleep(2)

        x_maq, y_maq = ataque_da_maquina(tabuleiro_jogador)
        print(f"Máquina atirou na coordenada {x_maq},{y_maq}!")
        time.sleep(1)

        if tabuleiro_jogador[y_maq][x_maq] == NAVIO:
            print("\n>>> A máquina acertou um de seus navios! <<<")
            tabuleiro_jogador[y_maq][x_maq] = ACERTO
            if verificar_vitoria(tabuleiro_jogador):
                limpar_tela()
                imprimir_tabuleiro(tabuleiro_maquina, "Máquina")
                imprimir_tabuleiro(tabuleiro_jogador, nome_jogador)
                print(f"\n☠️ FIM DE JOGO, {nome_jogador}! A MÁQUINA AFUNDOU SUA FROTA. ☠️")
                print("Agradecemos por jogar! Trabalho feito por:")
                print("- Carlos Eduardo Wille Martins")
                print("- Raul Castelnou")
                print("- Wlademir Alves de Souza")
                break
        else:
            print("\n>>> A máquina errou! <<<")
            tabuleiro_jogador[y_maq][x_maq] = ERRO

        time.sleep(3)

# Executa o programa
if __name__ == "__main__":
    main()