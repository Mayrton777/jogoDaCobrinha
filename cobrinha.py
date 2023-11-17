import pygame
from pygame.locals import *
from sys import exit
from random import randint

#inicia o pygame
pygame.init()

#musica de fundo
pygame.mixer.music.load('musica/fundo.mp3')
#volume da musica de fundo
pygame.mixer.music.set_volume(0.1)
#Faz um loop com a musica de fundo
pygame.mixer.music.play(-1)

#musica moeda
moeda = pygame.mixer.Sound('musica/coin.flac')
#volume da musica moeda
moeda.set_volume(0.02)

#largura e altura da tela
largura = 640
altura = 480
#cria uma tela com a largura e altura sendo respectivamente x e y
tela = pygame.display.set_mode((largura, altura))
#nomeia a tela com o nome jogo
pygame.display.set_caption('Jogo')

#posição em que a cobra surge na tela
x_cobra = largura / 2
y_cobra = altura / 2

#variavel com a velocidade do jogo
velocidade = 5
x_controle = velocidade
y_controle = 0

#variaveis para representam a posição sorteada da maça
x_maca = randint(40, 600)
y_maca = randint(50, 430)

# fonte do texto primeiro parâmetro e o nome da fonte, seguido pelo tamanho, negrito, itálico
fonte = pygame.font.SysFont('arial', 40, True, False)

#variavel para marcar os pontos
pontos = 0

#objeto para os FPS
relogio = pygame.time.Clock()

#adiciona a posição x y da cobra na lista
lista_cobra = []

#variavel com o comprimento inicial da cobra
comprimento_inicial = 5

#variavel que verifica os status da cobra
morreu = False


#função que aumenta o tamanho da cobra criando outros retângulos
def aumenta_cobra(crescer):
    for XeY in crescer:
        pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], 20, 20))


#Função que reinicia o jogo
def reiniciar_jogo():
    global pontos, comprimento_inicial, x_cobra, y_cobra, lista_cabeca, lista_cobra, x_maca, y_maca, morreu
    pontos = 0
    comprimento_inicial = 5
    x_cobra = largura / 2
    y_cobra = altura / 2
    lista_cabeca = []
    lista_cobra = []
    x_maca = randint(40, 600)
    y_maca = randint(50, 430)
    morreu = False


while True:
    #numero de FPS
    relogio.tick(60)

    #cor de fundo da tela
    tela.fill((150, 90, 80))

    #mensagem com os pontos
    mensagem = f'Pontos: {pontos}'
    texto_formatado = fonte.render(mensagem, True, (255, 255, 255))
    #posição do texto
    tela.blit(texto_formatado, (400, 40))

    #eventos
    for event in pygame.event.get():
        #fechamento da tela
        if event.type == QUIT:
            pygame.quit()
            exit()

        #movimento cobra
        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle -= velocidade
                    y_controle = 0
            if event.key == K_d:
                if x_controle == -velocidade:
                    pass
                else:
                    x_controle += velocidade
                    y_controle = 0
            if event.key == K_w:
                if y_controle == velocidade:
                    pass
                else:
                    y_controle -= velocidade
                    x_controle = 0
            if event.key == K_s:
                if y_controle == -velocidade:
                    pass
                else:
                    y_controle += velocidade
                    x_controle = 0

    x_cobra += x_controle
    y_cobra += y_controle

    #desenha a cobra na tela
    cobra = pygame.draw.rect(tela, (0, 255, 0), (x_cobra, y_cobra, 20, 20))
    #desenha a maça na tela
    maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, 20, 20))

    #colisão
    if cobra.colliderect(maca):
        x_maca = randint(40, 600)
        y_maca = randint(50, 430)
        pontos += 1
        moeda.play()
        comprimento_inicial += 2

    #adiciona a posição x e y da cobra a lista
    lista_cabeca = [x_cobra, y_cobra]
    #adiciona a posição da cabeça a lista cobra
    lista_cobra.append(lista_cabeca)

    #condição para caso a cobra se toque
    if lista_cobra.count(lista_cabeca) > 1:
        fonte2 = pygame.font.SysFont('arial', 20, True, False)
        mensagem = 'Game Over! Pressione a tecla R para jogar novamente'
        texto_formatado = fonte2.render(mensagem, True, (0, 0, 0))
        ret_texto = texto_formatado.get_rect()

        morreu = True
        while morreu:
            tela.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()

            ret_texto.center = (largura // 2, altura // 2)
            tela.blit(texto_formatado, ret_texto)
            pygame.display.update()

    #deleta o a ultima posição da cobra
    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    #chama a função aumenta cobra
    aumenta_cobra(lista_cobra)

    #faz com que quando a borda seja ultrapassada a cobra volte para a posição oposta do eixo y
    if y_cobra > 480:
        y_cobra = 0
    if y_cobra < 0:
        y_cobra = 480
    #faz com que quando a borda seja ultrapassada a cobra volte para a posição oposta do eixo x
    if x_cobra > 640:
        x_cobra = 0
    if x_cobra < 0:
        x_cobra = 640

    pygame.display.update()
