#Esta version del juego lo ejecuta con imagenes que tienen
#El nombre imagen#.png donde # corresponde a un numero del 1 al 8
#Si desea, puede colocar otras imagenes con los mismos nombres
#pero por defecto dejo esas
import os
import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Juego de Memoria")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Obtener el directorio de este archivo para usar rutas relativas
base_path = os.path.dirname(__file__)

# Cargar imágenes
def load_images():
    images = []
    for i in range(1, 9):  # Supongamos que tienes 8 imágenes diferentes
        image_path = os.path.join(base_path, "imagenes", f"imagen{i}.png")  # Subdirectorio "imagenes"
        image = pygame.image.load(image_path)  # Carga la imagen
        image = pygame.transform.scale(image, (100, 100))  # Redimensionar imágenes
        images.append(image)
    return images * 2  # Dos de cada imagen para formar las parejas

# Función para dibujar la pantalla de victoria
def draw_victory_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    victory_text = font.render("¡Ganaste!", True, BLACK)
    restart_text = font.render("Presiona R para reiniciar", True, BLACK)
    quit_text = font.render("Presiona Q para salir", True, BLACK)

    screen.blit(victory_text, (width // 2 - victory_text.get_width() // 2, height // 3))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2))
    screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 1.5))
    pygame.display.flip()

# Función para dibujar las cartas
def draw_board(revealed, images, score):
    screen.fill(WHITE)
    for i in range(len(images)):
        x = (i % 4) * 150 + 50
        y = (i // 4) * 150 + 50
        if revealed[i]:
            # Dibuja el contorno negro
            pygame.draw.rect(screen, BLACK, (x, y, 100, 100), 2)  # Contorno de 2 píxeles
            pygame.draw.rect(screen, WHITE, (x + 2, y + 2, 96, 96))  # Fondo de la carta
            screen.blit(images[i], (x, y))  # Dibuja la imagen
        else:
            pygame.draw.rect(screen, GRAY, (x, y, 100, 100))  # Carta oculta
    
    # Mostrar puntuación
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Puntuación: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()

# Bucle principal del juego
def main():
    images = load_images()
    random.shuffle(images)  # Mezclar las imágenes
    revealed = [False] * len(images)
    first_selection = None
    second_selection = None
    score = 0
    pause = False
    pause_start_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                mouse_x, mouse_y = event.pos
                card_index = (mouse_x // 150) + (mouse_y // 150) * 4

                if not revealed[card_index]:
                    revealed[card_index] = True

                    if first_selection is None:
                        first_selection = card_index
                    elif second_selection is None:
                        second_selection = card_index

                        # Verificar si hay pareja
                        if images[first_selection] == images[second_selection]:
                            score += 1
                            # Mantener las cartas descubiertas
                            first_selection = None
                            second_selection = None
                        else:
                            pause = True
                            pause_start_time = pygame.time.get_ticks()

            # Manejo de la pausa
            if pause:
                current_time = pygame.time.get_ticks()
                if current_time - pause_start_time >= 1000:  # 1000 ms = 1 segundo
                    # Ocultar las cartas si no son una pareja
                    if first_selection is not None and second_selection is not None:
                        revealed[first_selection] = False
                        revealed[second_selection] = False
                    
                    # Reiniciar selecciones
                    first_selection = None
                    second_selection = None
                    # Reiniciar la pausa
                    pause = False

        # Comprobar si se ha ganado
        if score >= 8:
            draw_victory_screen()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:  # Reiniciar juego
                            main()  # Reiniciar la función principal
                        elif event.key == pygame.K_q:  # Salir
                            pygame.quit()
                            sys.exit()
            continue

        draw_board(revealed, images, score)

# Iniciar el juego
main()
