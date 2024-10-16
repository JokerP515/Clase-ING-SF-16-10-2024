import pygame
import random
import time

# Inicializar pygame
pygame.init()

# Cargar música de fondo
pygame.mixer.music.load(r'C:\Users\Kirlian Herrera\Desktop\SONIDOSPROGRAMA\me estas tentando.mp3')
pygame.mixer.music.set_volume(0.5)  # Ajustar el volumen de la música (0.0 a 1.0)
pygame.mixer.music.play(-1)  # -1 significa que se repetirá en bucle

# Configurar pantalla
ANCHO, ALTO = 800, 600  # Tamaño de pantalla
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Memoria")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Cargar sonido del clic
sonido_click = pygame.mixer.Sound(r'C:\Users\Kirlian Herrera\Desktop\SONIDOSPROGRAMA\450612__breviceps__reverse-blip.wav')

# Cargar imagen de la carta oculta
IMAGEN_CARTA_OCULTA = pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\no cambiada.png')

# Cargar imágenes de cartas descubiertas
IMAGENES_CARTAS = [
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(53).png'),  # PNG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(54).png'),  # PNG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(55).jpg'),  # JPG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(56).jpg'),  # JPG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(57).jpg'),  # JPG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(58).jpg'),  # JPG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(59).jpg'),  # JPG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(60).jpg'),  # JPG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(61).png'),  # PNG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(62).jpg'),  # JPG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(63).jpg'),  # JPG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(64).jpg'),  # JPG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(65).jpg'),  # JPG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(66).jpg'),  # JPG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(67).jpg'),  # JPG
    pygame.image.load(r'C:\Users\Kirlian Herrera\Desktop\imagenes\(68).jpg')   # JPG
]

# Ajustar tamaño de las imágenes
IMAGEN_CARTA_OCULTA = pygame.transform.scale(IMAGEN_CARTA_OCULTA, (90, 140))
IMAGENES_CARTAS = [pygame.transform.scale(imagen, (90, 140)) for imagen in IMAGENES_CARTAS]

# Número de pares
pares = len(IMAGENES_CARTAS) // 2

# Crear el tablero de juego con pares de cartas
def crear_tablero(pares):
    valores = list(range(1, pares + 1)) * 2
    random.shuffle(valores)
    tablero = [valores[i:i + 8] for i in range(0, len(valores), 8)]
    return tablero

# Dibujar el tablero visualmente con pygame
def dibujar_tablero(tablero, descubiertas, puntos, tiempo):
    VENTANA.fill(BLANCO)

    # Mostrar cronómetro y puntaje
    font = pygame.font.SysFont(None, 36)
    texto_tiempo = font.render(f'Tiempo: {int(tiempo)} s', True, NEGRO)
    texto_puntos = font.render(f'Score: {puntos}', True, NEGRO)
    
    # Colocar el cronómetro y el puntaje
    VENTANA.blit(texto_tiempo, (ANCHO - 200, 10))  # Posicionar en la esquina superior derecha
    VENTANA.blit(texto_puntos, (ANCHO - 200, 50))  # Justo debajo del tiempo

    # Dibujar cartas
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            x = j * 100  # Posición horizontal
            y = i * 150 + 100  # Posición vertical, desplazado para dar espacio al marcador
            pygame.draw.rect(VENTANA, NEGRO, (x, y, 90, 140), 2)  # Dibujar cuadro para la carta
            if descubiertas[i][j]:
                # Mostrar imagen de la carta descubierta
                VENTANA.blit(IMAGENES_CARTAS[tablero[i][j] - 1], (x + 2, y + 2))
            else:
                # Mostrar la carta oculta
                VENTANA.blit(IMAGEN_CARTA_OCULTA, (x + 2, y + 2))

    dibujar_firma()
    pygame.display.update()

# Dibujar la firma del creador
def dibujar_firma():
    font = pygame.font.SysFont(None, 48)
    firma_texto = "Creado por Kirlian Herrera"
    ancho_firma = font.size(firma_texto)[0]

    for i, letra in enumerate(firma_texto):
        color = (i * 20 % 255, 255 - (i * 10 % 255), i * 40 % 255)
        texto = font.render(letra, True, color)
        VENTANA.blit(texto, (ANCHO // 2 - ancho_firma // 2 + (i * 20), ALTO - 50))

# Función para manejar la selección de cartas con el mouse
def seleccionar_carta_mouse(pos, descubiertas):
    fila = (pos[1] - 100) // 150  # Ajustar para la nueva posición del tablero
    columna = pos[0] // 100
    if 0 <= fila < len(descubiertas) and 0 <= columna < len(descubiertas[fila]) and not descubiertas[fila][columna]:
        return fila, columna
    return None, None

# Función principal del juego
def jugar_memoria():
    puntos = 0
    tablero = crear_tablero(pares)
    descubiertas = [[False] * 8 for _ in range(4)]
    seleccionada = []
    tiempo_inicio = time.time()

    corriendo = True
    reloj = pygame.time.Clock()

    while corriendo:
        tiempo = time.time() - tiempo_inicio
        dibujar_tablero(tablero, descubiertas, puntos, tiempo)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                fila, columna = seleccionar_carta_mouse(pos, descubiertas)

                if fila is not None and columna is not None:
                    seleccionada.append((fila, columna))
                    descubiertas[fila][columna] = True
                    sonido_click.play()

                    if len(seleccionada) == 2:
                        fila1, col1 = seleccionada[0]
                        fila2, col2 = seleccionada[1]
                        
                        # Verificar que las cartas estén dentro del rango
                        if fila1 < len(tablero) and fila2 < len(tablero) and tablero[fila1][col1] == tablero[fila2][col2]:
                            print("¡Par encontrado!")
                            puntos += 10
                        else:
                            time.sleep(0.5)
                            descubiertas[fila1][col1] = False
                            descubiertas[fila2][col2] = False
                            puntos -= 5

                        seleccionada.clear()

        if puntos == pares * 10:
            print("¡Felicidades! Has encontrado todos los pares.")
            corriendo = False

        reloj.tick(30)

    pygame.quit()

# Iniciar el juego
jugar_memoria()
