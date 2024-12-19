import pygame, random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")


# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Nave heroe
HEIGHT_NAVE_HEROE = 50
WIDTH_NAVE_HEROE = 50
POSITION_X_NAVE = WIDTH / 2
POSITION_Y_NAVE = HEIGHT - HEIGHT_NAVE_HEROE - 20
vida = 100
imagen_nave_heroe = pygame.image.load("./img/hero.png")
imagen_nave_heroe = pygame.transform.scale(
    imagen_nave_heroe, (WIDTH_NAVE_HEROE, HEIGHT_NAVE_HEROE)
)

rec_nave = imagen_nave_heroe.get_rect()
rec_nave.center = (POSITION_X_NAVE, POSITION_Y_NAVE)

rec_vida_heroe = pygame.Rect(0, HEIGHT - 15, 100, 10)

# Velocidad nave
velocidad = 5

# balas
WIDTH_BALAS = 50
HEIGHT_BALAS = 40
imagen_balas_heroe = pygame.image.load("./img/hero_bullets_2.png")
imagen_balas_heroe = pygame.transform.scale(
    imagen_balas_heroe, (WIDTH_BALAS, HEIGHT_BALAS)
)
rec_balas = imagen_balas_heroe.get_rect()
balas = []

# Enemigo
HEIGHT_NAVE_ENEMIGO = 150
WIDTH_NAVE_ENEMIGO = 150
POSITION_X_NAVE_ENEMIGO = WIDTH / 2
POSITION_Y_NAVE_ENEMIGO = 70
PARPADEO_DURACION = 5
jefe_1_vivo = True
tiempo_parpadeo = 0
vida_enemigo = 100
color_enemigo = RED
movimiento_enemigo = 4

imagen_nave_enemigo_grande_parpadeo = pygame.image.load(
    "./img/enemy_big_colition.png"
).convert_alpha()
imagen_nave_enemigo_grande = pygame.image.load("./img/enemy_big.png").convert_alpha()
imagen_nave_enemigo_grande_parpadeo = pygame.transform.scale(
    imagen_nave_enemigo_grande_parpadeo, (WIDTH_NAVE_ENEMIGO, HEIGHT_NAVE_ENEMIGO)
)
imagen_nave_enemigo_grande = pygame.transform.scale(
    imagen_nave_enemigo_grande, (WIDTH_NAVE_ENEMIGO, HEIGHT_NAVE_ENEMIGO)
)
imagen_nave_enemigo_actual = imagen_nave_enemigo_grande

rec_nave_enemigo = imagen_nave_enemigo_actual.get_rect()
rec_nave_enemigo.center = (POSITION_X_NAVE_ENEMIGO, POSITION_Y_NAVE_ENEMIGO)

# balas ENEMIGAS
WIDTH_BALAS = 80
HEIGHT_BALAS = 70
frecuencia_disparo = 1
tiempo_ultimo_disparo = pygame.time.get_ticks() / 1000
imagen_balas_enemigas = pygame.image.load("./img/enemy_big_bullets.png")
imagen_balas_enemigas = pygame.transform.scale(
    imagen_balas_enemigas, (WIDTH_BALAS, HEIGHT_BALAS)
)
balas_enemigas = []

# Cargar imágenes de la explosión
imagenes_explosion = [
    pygame.image.load("./img/explosion_2.png").convert_alpha(),
    pygame.image.load("./img/explosion_3.png").convert_alpha(),
    pygame.image.load("./img/explosion_4.png").convert_alpha(),
    pygame.image.load("./img/explosion_5.png").convert_alpha(),
    pygame.image.load("./img/explosion_6.png").convert_alpha(),
    pygame.image.load("./img/explosion_7.png").convert_alpha(),
    pygame.image.load("./img/explosion_8.png").convert_alpha(),
]
imagenes_explosion = [
    pygame.transform.scale(imagen, (WIDTH_NAVE_ENEMIGO, HEIGHT_NAVE_ENEMIGO))
    for imagen in imagenes_explosion
]
explosion_animada_activa = False

# inicio del juego
iniciar = False
# Fin del juego
winner = False
game_over = False


def animar_explosion(screen, x, y):
    for imagen in imagenes_explosion:
        screen.blit(imagen, (x - imagen.get_width() // 2, y - imagen.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(100)


def dibujar_nave_jugador():
    screen.blit(imagen_nave_heroe, rec_nave)


def vida_jugador():
    pygame.draw.rect(screen, GREEN, (5, HEIGHT - 15, vida, 10))


def crear_balas(x):
    nueva_bala = {}
    nueva_bala["rect"] = imagen_balas_heroe.get_rect()
    nueva_bala["rect"].center = (x, POSITION_Y_NAVE - 40)
    nueva_bala["velocidad"] = 10
    balas.append(nueva_bala)


def dibujar_balas():
    for bala in balas:
        screen.blit(imagen_balas_heroe, bala["rect"])


def dibujar_enemigo():
    screen.blit(imagen_nave_enemigo_actual, rec_nave_enemigo)


def crear_balas_enemigas():
    nueva_bala = {}
    nueva_bala["rect"] = imagen_balas_enemigas.get_rect()
    nueva_bala["rect"].center = rec_nave_enemigo.center
    nueva_bala["velocidad"] = 8
    balas_enemigas.append(nueva_bala)


def dibujar_balas_enemigas():
    for bala in balas_enemigas:
        screen.blit(imagen_balas_enemigas, bala["rect"])


def cambiar_vida_enemigo():
    pygame.draw.rect(screen, RED, (WIDTH - 110, HEIGHT - 15, vida_enemigo, 10))


running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)
    # pygame.draw.rect(screen, color_enemigo, rec_nave_enemigo)
    if not iniciar:
        font = pygame.font.SysFont(None, 50)
        title = font.render("Space Invaders", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
        start_text = font.render("Presiona cualquier tecla para empezar", True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # Si se presiona cualquier tecla
                iniciar = True
    else:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if keys[pygame.K_SPACE]:
                crear_balas(rec_nave.x + 25)
        if not game_over:

            if keys[pygame.K_LEFT] and rec_nave.left >= (WIDTH - (WIDTH - 5)):
                rec_nave.left -= velocidad
            if keys[pygame.K_RIGHT] and rec_nave.right <= (WIDTH - 5):
                rec_nave.right += velocidad

            # Balas
            for bala in balas[:]:
                bala["rect"].y -= bala["velocidad"]
                if bala["rect"].colliderect(rec_nave_enemigo):
                    balas.remove(bala)
                    vida_enemigo = vida_enemigo - 10
                    tiempo_parpadeo = PARPADEO_DURACION
                    color_enemigo = WHITE
                    if frecuencia_disparo > 0.7:
                        frecuencia_disparo -= 0.1
                    if movimiento_enemigo > 0:
                        movimiento_enemigo += 2
                    else:
                        movimiento_enemigo -= 2
                    if vida_enemigo <= 0:
                        game_over = True
                        winner = True
                    imagen_nave_enemigo_actual = imagen_nave_enemigo_grande_parpadeo
                if bala["rect"].y < 0:
                    balas.remove(bala)

            # Vida enemigo
            if not winner:

                # Balas enemigas JEFE1
                for bala in balas_enemigas[:]:
                    bala["rect"].y += bala["velocidad"]
                    if bala["rect"].colliderect(rec_nave):
                        balas_enemigas.remove(bala)
                        vida -= 25
                        if vida <= 0:
                            game_over = True
                            winner = False
                    if bala["rect"].y > HEIGHT:
                        balas_enemigas.remove(bala)

                tiempo_actual = pygame.time.get_ticks() / 1000
                if tiempo_actual - tiempo_ultimo_disparo >= frecuencia_disparo:
                    crear_balas_enemigas()
                    tiempo_ultimo_disparo = tiempo_actual

                # Parpadeo
                if tiempo_parpadeo > 0:
                    tiempo_parpadeo -= 1
                    if tiempo_parpadeo == 0:
                        imagen_nave_enemigo_actual = imagen_nave_enemigo_grande
                        color_enemigo = RED

                # Movimiento enemigo
                if movimiento_enemigo == 0:
                    movimiento_enemigo = random.choice([-4, 4])
                if movimiento_enemigo >= 10:
                    movimiento_enemigo = 10
                if movimiento_enemigo <= -10:
                    movimiento_enemigo = -10
                rec_nave_enemigo.x += movimiento_enemigo

                if rec_nave_enemigo.left <= 5:
                    movimiento_enemigo *= -1
                elif rec_nave_enemigo.right >= WIDTH - 5:
                    movimiento_enemigo *= -1

                dibujar_enemigo()
            else:
                jefe_1_vivo = False
                balas_enemigas = []
            if (explosion_animada_activa == False) and jefe_1_vivo == False:
                explosion_animada_activa = True
                animar_explosion(
                    screen, rec_nave_enemigo.centerx, rec_nave_enemigo.centery
                )

            dibujar_nave_jugador()
            dibujar_balas()
            dibujar_balas_enemigas()
            vida_jugador()
            cambiar_vida_enemigo()

        else:
            if winner:
                game_over_text = font.render("¡GANASTE!", True, GREEN)
            else:
                game_over_text = font.render("¡PERDISTE!", True, RED)
            screen.blit(
                game_over_text,
                (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2),
            )

    pygame.display.flip()
    clock.tick(60)
