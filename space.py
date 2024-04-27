import pygame
import random
import math

# Inicializa o Pygame
pygame.init()

# Configura a tela
tela_largura = 800
tela_altura = 600
tela = pygame.display.set_mode((tela_largura, tela_altura))
done = False

# Título e Ícone
pygame.display.set_caption("Space Invaders")
icone = pygame.image.load('icone.png')  # Adicione o caminho para o seu ícone de jogo aqui
pygame.display.set_icon(icone)

# Jogador
jogador_img = pygame.image.load('706026.png')  # Adicione o caminho para sua imagem de jogador
jogador_x = 370
jogador_y = 480
jogador_x_change = 0

# Inimigo
inimigo_img = []
inimigo_x = []
inimigo_y = []
inimigo_x_change = []
inimigo_y_change = []
num_inimigos = 6

for i in range(num_inimigos):
    inimigo_img.append(pygame.image.load('inimigo.png'))  # Adicione o caminho para sua imagem de inimigo
    inimigo_x.append(random.randint(0, 735))
    inimigo_y.append(random.randint(50, 150))
    inimigo_x_change.append(4)
    inimigo_y_change.append(40)

# Tiro
# 'ready' - Você não pode ver o tiro na tela
# 'fire' - O tiro está se movendo
tiro_img = pygame.image.load('99396.png')  # Adicione o caminho para sua imagem de tiro
tiro_x = 0
tiro_y = 480
tiro_x_change = 0
tiro_y_change = 10
tiro_estado = 'ready'

# Pontuação
pontuacao = 0
fonte = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

def mostrar_pontuacao(x, y):
    score = fonte.render("Pontuação : " + str(pontuacao), True, (0, 0, 0))  # Altera a cor do texto para preto
    tela.blit(score, (x, y))


def e_colisao(inimigo_x, inimigo_y, tiro_x, tiro_y):
    distancia = math.sqrt(math.pow(inimigo_x - tiro_x, 2) + math.pow(inimigo_y - tiro_y, 2))
    if distancia < 27:
        return True
    else:
        return False


def jogador(x, y):
    tela.blit(jogador_img, (x, y))

def inimigo(x, y, i):
    tela.blit(inimigo_img[i], (x, y))

def disparar_tiro(x, y):
    global tiro_estado
    tiro_estado = 'fire'
    tela.blit(tiro_img, (x + 16, y + 10))

# Relógio para controlar a taxa de FPS
relogio = pygame.time.Clock()

# Game Loop
executando = True
while executando:
    tela.fill((255, 255, 255))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

        # Se uma tecla for pressionada, verifica se é esquerda ou direita
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jogador_x_change = -5
            if evento.key == pygame.K_RIGHT:
                jogador_x_change = 5
            if evento.key == pygame.K_SPACE:
                if tiro_estado == 'ready':
                    tiro_x = jogador_x
                    disparar_tiro(tiro_x, tiro_y)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jogador_x_change = 0

    jogador_x += jogador_x_change

    # Mantém o jogador dentro da tela
    if jogador_x <= 0:
        jogador_x = 0
    elif jogador_x >= 736:
        jogador_x = 736

  # Movimento do Inimigo e Detecção de Colisão
    for i in range(num_inimigos):
        inimigo_x[i] += inimigo_x_change[i]
        if inimigo_x[i] <= 0:
            inimigo_x_change[i] = 4
            inimigo_y[i] += inimigo_y_change[i]
        elif inimigo_x[i] >= 736:
            inimigo_x_change[i] = -4
            inimigo_y[i] += inimigo_y_change[i]

        # Detecção de colisão
        colisao = e_colisao(inimigo_x[i], inimigo_y[i], tiro_x, tiro_y)
        if colisao:
            tiro_y = 480
            tiro_estado = 'ready'
            pontuacao += 1  # Atualiza a pontuação
            inimigo_x[i] = random.randint(0, 735)  # Reposiciona o inimigo para um novo local aleatório
            inimigo_y[i] = random.randint(50, 150)

        inimigo(inimigo_x[i], inimigo_y[i], i)

    # Movimento do tiro
    if tiro_y <= 0:
        tiro_y = 480
        tiro_estado = 'ready'

    if tiro_estado == 'fire':
        disparar_tiro(tiro_x, tiro_y)
        tiro_y -= tiro_y_change

    jogador(jogador_x, jogador_y)
    mostrar_pontuacao(texto_x, texto_y)  # Mostra a pontuação na tela
    pygame.display.update()

     # Define a taxa de FPS
    relogio.tick(30)  # Reduzindo para 30 FPS para tornar o jogo mais lento
