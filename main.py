import pygame
import random
import json
import os

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600  # Ancho y alto de la ventana del juego

# Colores básicos
BLACK = (0, 0, 0)  # Negro (fondo)
WHITE = (255, 255, 255)  # Blanco (elementos visibles)

# Cargar colores desde un archivo JSON
with open("colores.json", "r") as file: # yo
    carga = json.load(file)  # Cargar los colores desde un archivo JSON
COLORES = [tuple(color) for color in carga["colores"]]  # Convierte los colores a tuplas

# Clase principal del juego
class juego_tenis:# ambos
    def __init__(self):
        # Configuración de la ventana
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Trabajo Practico -Game-Pong-")
        self.clock = pygame.time.Clock()  # Controla el tiempo del juego

        # Configuración inicial de nombres de jugadores
        self.jugador_1_name = ""
        self.jugador_2_name = ""

        # Configuración inicial de la pelota
        self.pelota_size = 20
        self.reiniciar_pelota()  # Coloca la pelota en su posición inicial

        # Configuración inicial de las paletas
        self.paleta_width = 20
        self.paleta_height = 100
        self.paleta_speed = 10  # Velocidad de movimiento de las paletas
        self.reiniciar_paletas()  # Coloca las paletas en su posición inicial

        # Inicialización de puntajes
        self.score1 = 0
        self.score2 = 0

        # Multiplicador de velocidad para la pelota
        self.multiplicar_velocidad = 0.4

        # Cargar sonidos del juego
        self.bounce_sound = pygame.mixer.Sound("sonidos\\bounce_sound.mp3")  # Sonido al rebotar
        self.score_sound = pygame.mixer.Sound("sonidos\\score_sound.mp3")  # Sonido al anotar
        self.menu_sound = pygame.mixer.Sound("sonidos\\menu.mp3")  # Sonido del menú inicial

        # Fuentes para los textos en pantalla
        self.letra_grande = pygame.font.Font(None, 75)  # Fuente para textos grandes
        self.letra_pequeña = pygame.font.Font(None, 50)  # Fuente para textos pequeños

    # Reinicia la posición de la pelota y su velocidad
    def reiniciar_pelota(self):# yo
        # Coloca la pelota en el centro de la pantalla
        self.pelota_x = WIDTH // 2
        self.pelota_y = HEIGHT // 2
        # Asigna una velocidad inicial aleatoria en el eje X (izquierda o derecha)
        self.pelota_speed_x = random.choice([-4, 4])
        # Asigna una velocidad inicial aleatoria en el eje Y (arriba o abajo)
        self.pelota_speed_y = random.choice([-4, 4])
        # Cambia el color de la pelota a uno aleatorio de la lista de colores
        self.pelota_color = random.choice(COLORES)

    # Reinicia la posición de las paletas
    def reiniciar_paletas(self): # yo
        # Posiciona la paleta izquierda al centro vertical de la pantalla
        self.paleta1_y = HEIGHT // 2 - self.paleta_height // 2
        # Posiciona la paleta derecha al centro vertical de la pantalla
        self.paleta2_y = HEIGHT // 2 - self.paleta_height // 2

    # Guarda los resultados del juego en un archivo JSON
    def guardar_resultados(self, winner, winner_score, loser, loser_score):# fran
        # Crea un diccionario para almacenar el resultado de la partida
        resultado = {
            "ganador": {"nombre": winner, "puntos": winner_score},  # Datos del jugador ganador
            "perdedor": {"nombre": loser, "puntos": loser_score},  # Datos del jugador perdedor
        }

        # Verifica si ya existe el archivo de resultados
        if os.path.exists("resultados_pong.json"):
            # Si el archivo existe, intenta cargar los datos existentes
            with open("resultados_pong.json", "r") as file:
                try:
                    datos = json.load(file)  # Carga los datos del archivo
                except json.JSONDecodeError:
                    datos = []  # Si hay un error, inicia con una lista vacía
        else:
            # Si el archivo no existe, inicia con una lista vacía
            datos = []

        # Añade el nuevo resultado a la lista de datos
        datos.append(resultado)

        # Escribe la lista actualizada de resultados en el archivo
        with open("resultados_pong.json", "w") as file:
            json.dump(datos, file, indent=4)  # Guarda en formato JSON con sangría para legibilidad

        # Método para pedir los nombres de los jugadores antes de iniciar el juego
    def pedir_nombres(self): # ambos
        # Variables para rastrear si los cuadros de texto están activos (seleccionados)
        input_active = [False, False]  # Estado de los cuadros de texto
        input_boxes = [  # Coordenadas y dimensiones de los cuadros de entrada
            pygame.Rect(WIDTH // 4 - 100, HEIGHT // 2, 200, 50),  # Cuadro para el jugador 1
            pygame.Rect(3 * WIDTH // 4 - 100, HEIGHT // 2, 200, 50),  # Cuadro para el jugador 2
        ]
        input_texts = ["", ""]  # Lista para almacenar los textos que introducen los jugadores
        font_input = pygame.font.Font(None, 50)  # Fuente para el texto que aparece en los cuadros
        jugar_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 100, 150, 50)  # Botón "JUGAR"
        running = True  # Controla el bucle principal del menú

        # Reproduce el sonido del menú en bucle continuo
        self.menu_sound.play(loops=-1)

        while running:
            # Captura los eventos generados en la ventana
            for event in pygame.event.get():
                # Si se cierra la ventana, termina el programa
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Evento: clic del ratón
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Verifica si se hizo clic en uno de los cuadros de entrada
                    for i, box in enumerate(input_boxes):
                        if box.collidepoint(event.pos):  # Si el clic está dentro del cuadro
                            input_active[i] = True  # Activa el cuadro correspondiente
                        else:
                            input_active[i] = False  # Desactiva los demás cuadros

                    # Verifica si se hizo clic en el botón "JUGAR"
                    if jugar_button.collidepoint(event.pos) and all(input_texts):  # Requiere que ambos nombres estén completos
                        # Guarda los nombres introducidos y termina el bucle
                        self.jugador_1_name, self.jugador_2_name = input_texts
                        running = False

                # Evento: pulsación de una tecla
                if event.type == pygame.KEYDOWN:
                    # Verifica cuál cuadro está activo
                    for i, active in enumerate(input_active):
                        if active:
                            if event.key == pygame.K_BACKSPACE:  # Si se presiona la tecla "Backspace"
                                input_texts[i] = input_texts[i][:-1]  # Borra el último carácter del texto
                            elif len(input_texts[i]) < 11:  # Limita el texto a 11 caracteres
                                input_texts[i] += event.unicode  # Agrega el carácter presionado su respectiva tecla

            # Renderiza la pantalla de entrada de nombres
            self.screen.fill(BLACK)  # Limpia la pantalla con un fondo negro
            self.dibujar_texto("Ingrese los nombres:", WHITE, WIDTH // 2, HEIGHT // 3, center=True)  # Título del menú

            # Renderiza los cuadros de texto y el texto introducido en ellos
            for i, box in enumerate(input_boxes):
                # Cambia el color del cuadro si está activo (blanco) o inactivo (gris)
                pygame.draw.rect(self.screen, WHITE if input_active[i] else (100, 100, 100), box, 2)
                # Renderiza el texto introducido dentro del cuadro
                text_surface = font_input.render(input_texts[i], True, WHITE)
                self.screen.blit(text_surface, (box.x + 10, box.y + 10))

            # Renderiza el botón "JUGAR"
            pygame.draw.rect(self.screen, WHITE, jugar_button)  # Dibuja el rectángulo del botón
            self.dibujar_texto("JUGAR", BLACK, jugar_button.centerx, jugar_button.centery, center=True, font=self.letra_pequeña)  # Texto del botón

            # Actualiza la pantalla
            pygame.display.flip()
            self.clock.tick(30)  # Controla la velocidad del bucle (30 FPS)

        # Detiene el sonido del menú una vez que los nombres han sido ingresados
        self.menu_sound.stop()

    # Dibuja texto en pantalla #fran
    def dibujar_texto(self, text, color, x, y, center=False, font=None):
        font = font or self.letra_grande
        render = font.render(text, True, color)
        if center:
            rect = render.get_rect(center=(x, y))
            self.screen.blit(render, rect.topleft)
        else:
            self.screen.blit(render, (x, y))

    # Mueve la pelota y maneja las colisiones
    def mover_bola(self):# ambos
        # Actualiza la posición de la pelota sumando la velocidad a sus coordenadas
        self.pelota_x += self.pelota_speed_x * self.multiplicar_velocidad
        self.pelota_y += self.pelota_speed_y * self.multiplicar_velocidad

        # Verifica si la pelota toca los bordes superior o inferior de la ventana
        if self.pelota_y < 0 or self.pelota_y > HEIGHT - self.pelota_size:
            self.pelota_speed_y *= -1  # Invierte la dirección de la velocidad en el eje Y (rebote vertical)
            self.pelota_color = random.choice(COLORES)  # Cambia el color de la pelota al rebotar
            self.bounce_sound.play()  # Reproduce un sonido para indicar el rebote

        # Verifica colisiones con las paletas:

        # Lado izquierdo: entre el borde y la primera paleta
        if (20 < self.pelota_x < 20 + self.paleta_width and  # La pelota está dentro del rango de la paleta en X
            self.paleta1_y < self.pelota_y + self.pelota_size < self.paleta1_y + self.paleta_height):  # La pelota está dentro del rango de la paleta en Y
            self.pelota_speed_x *= -1  # Invierte la dirección de la velocidad en el eje X (rebote horizontal)
            self.pelota_color = random.choice(COLORES)  # Cambia el color de la pelota
            self.bounce_sound.play()  # Reproduce el sonido del rebote
            self.multiplicar_velocidad += 0.04  # Incrementa gradualmente la velocidad de la pelota

        # Lado derecho: entre el borde y la segunda paleta
        if (WIDTH - 20 - self.paleta_width < self.pelota_x + self.pelota_size < WIDTH - 20 and  # Verifica el rango en X
            self.paleta2_y < self.pelota_y + self.pelota_size < self.paleta2_y + self.paleta_height):  # Verifica el rango en Y
            self.pelota_speed_x *= -1  # Rebote horizontal
            self.pelota_color = random.choice(COLORES)  # Cambia el color de la pelota
            self.bounce_sound.play()  # Reproduce el sonido del rebote
            self.multiplicar_velocidad += 0.04  # Incrementa la velocidad gradualmente

        # Verifica si la pelota sale del lado izquierdo de la pantalla
        if self.pelota_x <= 0:  
            self.score2 += 1  # Aumenta el puntaje del jugador 2
            self.score_sound.play()  # Reproduce el sonido de anotación
            self.reiniciar_pelota()  # Reinicia la posición y la velocidad de la pelota

        # Verifica si la pelota sale del lado derecho de la pantalla
        if self.pelota_x >= WIDTH:  
            self.score1 += 1  # Aumenta el puntaje del jugador 1
            self.score_sound.play()  # Reproduce el sonido de anotación
            self.reiniciar_pelota()  # Reinicia la posición y la velocidad de la pelota

    # Lógica principal del juego
    def run(self):# ambos
        # Inicia el juego pidiendo los nombres de los jugadores
        self.pedir_nombres()
        running = True  # Variable para controlar el bucle principal

        while running:  # Bucle principal del juego
            # Procesar eventos de Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si se cierra la ventana
                    running = False  # Salir del bucle principal
                if event.type == pygame.KEYDOWN:  # Detectar teclas presionadas
                    if event.key == pygame.K_r:  # Si se presiona 'R', reiniciar el juego
                        self.score1 = 0  # Reinicia el puntaje del jugador 1
                        self.score2 = 0  # Reinicia el puntaje del jugador 2
                        self.multiplicar_velocidad = 1  # Restablece la velocidad inicial
                        self.reiniciar_pelota()  # Reinicia la posición de la pelota
                        self.reiniciar_paletas()  # Reinicia las posiciones de las paletas
                    if event.key == pygame.K_m:  # Si se presiona 'M', regresar al menú inicial
                        self.pedir_nombres()  # Pide los nombres de nuevo
                        self.score1 = 0  # Reinicia el puntaje del jugador 1
                        self.score2 = 0  # Reinicia el puntaje del jugador 2
                        self.reiniciar_pelota()  # Reinicia la posición de la pelota
                        self.reiniciar_paletas()  # Reinicia las posiciones de las paletas

            # Manejo del movimiento de las paletas con las teclas correspondientes
            keys = pygame.key.get_pressed()  # Verifica las teclas presionadas
            if keys[pygame.K_w] and self.paleta1_y > 0:  # Mueve la paleta izquierda hacia arriba
                self.paleta1_y -= self.paleta_speed
            if keys[pygame.K_s] and self.paleta1_y < HEIGHT - self.paleta_height:  # Mueve la paleta izquierda hacia abajo
                self.paleta1_y += self.paleta_speed
            if keys[pygame.K_UP] and self.paleta2_y > 0:  # Mueve la paleta derecha hacia arriba
                self.paleta2_y -= self.paleta_speed
            if keys[pygame.K_DOWN] and self.paleta2_y < HEIGHT - self.paleta_height:  # Mueve la paleta derecha hacia abajo
                self.paleta2_y += self.paleta_speed

            # Llama al método que actualiza la posición de la pelota y maneja las colisiones
            self.mover_bola()

            # Verifica si algún jugador ha alcanzado 10 puntos (condición para ganar)
            if self.score1 == 11 or self.score2 == 11:
                # Determina el ganador y el perdedor
                winner = self.jugador_1_name if self.score1 == 10 else self.jugador_2_name
                loser = self.jugador_2_name if winner == self.jugador_1_name else self.jugador_1_name
                winner_score = self.score1 if self.score1 == 10 else self.score2
                loser_score = self.score2 if winner == self.jugador_1_name else self.score1

                print(f"{winner} gana!")  # Imprime el ganador en la consola
                self.guardar_resultados(winner, winner_score, loser, loser_score)  # Guarda los resultados en un archivo
                pygame.time.wait(3000)  # Pausa de 3 segundos antes de reiniciar
                self.score1 = 0  # Reinicia el puntaje del jugador 1
                self.score2 = 0  # Reinicia el puntaje del jugador 2
                self.reiniciar_pelota()  # Reinicia la posición de la pelota
                self.reiniciar_paletas()  # Reinicia las posiciones de las paletas
                self.pedir_nombres()  # Regresa al menú inicial para ingresar los nombres nuevamente

            # Dibuja todos los elementos del juego en la pantalla
            self.screen.fill(BLACK)  # Limpia la pantalla con un color negro
            pygame.draw.rect(self.screen, WHITE, (20, self.paleta1_y, self.paleta_width, self.paleta_height))  # Dibuja la paleta izquierda
            pygame.draw.rect(self.screen, WHITE, (WIDTH - 20 - self.paleta_width, self.paleta2_y, self.paleta_width, self.paleta_height))  # Dibuja la paleta derecha
            pygame.draw.ellipse(self.screen, self.pelota_color, (self.pelota_x, self.pelota_y, self.pelota_size, self.pelota_size))  # Dibuja la pelota
            pygame.draw.aaline(self.screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))  # Dibuja la línea central de la cancha

            # Dibuja los nombres de los jugadores y sus puntajes en pantalla
            self.dibujar_texto(f"{self.jugador_1_name}: {self.score1}", WHITE, WIDTH // 6, 20, font=self.letra_pequeña)
            self.dibujar_texto(f"{self.jugador_2_name}: {self.score2}", WHITE, 3 * WIDTH // 5, 20, font=self.letra_pequeña)

            pygame.display.flip()  # Actualiza la pantalla para reflejar los cambios
            self.clock.tick(30)  # Controla la tasa de cuadros por segundo (30 FPS)

# Ejecutar el juego
if __name__ == "__main__":
    game = juego_tenis()
    game.run()
