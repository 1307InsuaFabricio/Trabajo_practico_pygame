import pygame
import random
import json
import os
# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Cargar colores desde un archivo JSON
with open("colores.json", "r") as file:
    carga = json.load(file)
COLORES = [tuple(color) for color in carga["colores"]]

# Clase del juego
class juego_tenis:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Trabajo Practico -Game-Pong-")
        self.clock = pygame.time.Clock()

        # Configuración inicial
        self.jugador_1_name = ""
        self.jugador_2_name = ""

        # Configuración de la pelota
        self.pelota_size = 20
        self.reiniciar_pelota()

        # Configuración de las paletas
        self.paleta_width = 20
        self.paleta_height = 100
        self.paleta_speed = 10
        self.reiniciar_paletas()

        # Puntajes
        self.score1 = 0
        self.score2 = 0

        # Multiplicador de velocidad
        self.multiplicar_velocidad = 0.3

        # Sonidos
        self.bounce_sound = pygame.mixer.Sound("sonidos\\bounce_sound.mp3")
        self.score_sound = pygame.mixer.Sound("sonidos\\score_sound.mp3")
        self.menu_sound = pygame.mixer.Sound("sonidos\\menu.mp3")
        

        # Fuentes
        self.letra_grande = pygame.font.Font(None, 75)  
        self.letra_pequeña = pygame.font.Font(None, 50)  

    def reiniciar_pelota(self):
        self.pelota_x = WIDTH // 2
        self.pelota_y = HEIGHT // 2
        self.pelota_speed_x = random.choice([-4, 4])
        self.pelota_speed_y = random.choice([-4, 4])
        self.pelota_color = random.choice(COLORES)

    def reiniciar_paletas(self):
        self.paleta1_y = HEIGHT // 2 - self.paleta_height // 2
        self.paleta2_y = HEIGHT // 2 - self.paleta_height // 2

    def guardar_resultados(self, winner, winner_score, loser, loser_score):
        resultado = {
            "ganador": {"nombre": winner, "puntos": winner_score},
            "perdedor": {"nombre": loser, "puntos": loser_score},
        }
        if os.path.exists("resultados_pong.json"):
            with open("resultados_pong.json", "r") as file:
                try:
                    datos = json.load(file)
                except json.JSONDecodeError:
                    datos = []
        else:
            datos = []
        datos.append(resultado)
        with open("resultados_pong.json", "w") as file:
            json.dump(datos, file, indent=4)

    def pedir_nombres(self):
        input_active = [False, False]
        input_boxes = [
            pygame.Rect(WIDTH // 4 - 100, HEIGHT // 2, 200, 50),
            pygame.Rect(3 * WIDTH // 4 - 100, HEIGHT // 2, 200, 50),
        ]
        input_texts = ["", ""]
        font_input = pygame.font.Font(None, 50)
        jugar_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 100, 150, 50)
        running = True

        # Reproducir el sonido del menú en bucle al entrar en esta pantalla
        self.menu_sound.play(loops=-1)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, box in enumerate(input_boxes):
                        if box.collidepoint(event.pos):
                            input_active[i] = True
                        else:
                            input_active[i] = False
                    # Comprobar si se presionó el botón "JUGAR"
                    if jugar_button.collidepoint(event.pos) and all(input_texts):
                        self.jugador_1_name, self.jugador_2_name = input_texts
                        running = False
                if event.type == pygame.KEYDOWN:
                    for i, active in enumerate(input_active):
                        if active:
                            if event.key == pygame.K_BACKSPACE:
                                input_texts[i] = input_texts[i][:-1]
                            elif len(input_texts[i]) < 11:
                                input_texts[i] += event.unicode

            self.screen.fill(BLACK)
            self.dibujar_texto("Ingrese los nombres:", WHITE, WIDTH // 2, HEIGHT // 3, center=True)
            for i, box in enumerate(input_boxes):
                pygame.draw.rect(self.screen, WHITE if input_active[i] else (100, 100, 100), box, 2)
                text_surface = font_input.render(input_texts[i], True, WHITE)
                self.screen.blit(text_surface, (box.x + 10, box.y + 10))

            # Dibujar el botón "JUGAR"
            pygame.draw.rect(self.screen, WHITE, jugar_button)
            self.dibujar_texto("JUGAR", BLACK, jugar_button.centerx, jugar_button.centery, center=True, font=self.letra_pequeña)

            pygame.display.flip()
            self.clock.tick(30)

        # Detener el sonido del menú una vez que los nombres hayan sido ingresados
        self.menu_sound.stop()

    def dibujar_texto(self, text, color, x, y, center=False, font=None):
        font = font or self.letra_grande
        render = font.render(text, True, color)
        if center:
            rect = render.get_rect(center=(x, y))
            self.screen.blit(render, rect.topleft)
        else:
            self.screen.blit(render, (x, y))

    def mover_bola(self):
        self.pelota_x += self.pelota_speed_x * self.multiplicar_velocidad
        self.pelota_y += self.pelota_speed_y * self.multiplicar_velocidad

        if self.pelota_y < 0 or self.pelota_y > HEIGHT - self.pelota_size:
            self.pelota_speed_y *= -1
            self.pelota_color = random.choice(COLORES)
            self.bounce_sound.play()

        if (20 < self.pelota_x < 20 + self.paleta_width and
            self.paleta1_y < self.pelota_y + self.pelota_size < self.paleta1_y + self.paleta_height) or \
           (WIDTH - 20 - self.paleta_width < self.pelota_x + self.pelota_size < WIDTH - 20 and
            self.paleta2_y < self.pelota_y + self.pelota_size < self.paleta2_y + self.paleta_height):
            self.pelota_speed_x *= -1
            self.pelota_color = random.choice(COLORES)
            self.bounce_sound.play()
            self.multiplicar_velocidad += 0.03

        if self.pelota_x <= 0:
            self.score2 += 1
            self.score_sound.play()
            self.reiniciar_pelota()
        if self.pelota_x >= WIDTH:
            self.score1 += 1
            self.score_sound.play()
            self.reiniciar_pelota()

    def run(self):
        self.pedir_nombres()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Reiniciar puntajes y juego
                        self.score1 = 0
                        self.score2 = 0
                        self.multiplicar_velocidad = 1
                        self.reiniciar_pelota()
                        self.reiniciar_paletas()
                    if event.key == pygame.K_m:  # Regresar a ventana de pedir nombres
                        self.pedir_nombres()
                        self.score1 = 0
                        self.score2 = 0
                        self.reiniciar_pelota()
                        self.reiniciar_paletas()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and self.paleta1_y > 0:
                self.paleta1_y -= self.paleta_speed
            if keys[pygame.K_s] and self.paleta1_y < HEIGHT - self.paleta_height:
                self.paleta1_y += self.paleta_speed
            if keys[pygame.K_UP] and self.paleta2_y > 0:
                self.paleta2_y -= self.paleta_speed
            if keys[pygame.K_DOWN] and self.paleta2_y < HEIGHT - self.paleta_height:
                self.paleta2_y += self.paleta_speed

            self.mover_bola()

            if self.score1 == 10 or self.score2 == 10:
                winner = self.jugador_1_name if self.score1 == 10 else self.jugador_2_name
                loser = self.jugador_2_name if winner == self.jugador_1_name else self.jugador_1_name
                winner_score = self.score1 if self.score1 == 10 else self.score2
                loser_score = self.score2 if winner == self.jugador_1_name else self.score1

                print(f"{winner} gana!")
                self.guardar_resultados(winner, winner_score, loser, loser_score)
                pygame.time.wait(3000)
                self.score1 = 0
                self.score2 = 0
                self.reiniciar_pelota()
                self.reiniciar_paletas()
                self.pedir_nombres()

            self.screen.fill(BLACK)
            pygame.draw.rect(self.screen, WHITE, (20, self.paleta1_y, self.paleta_width, self.paleta_height))
            pygame.draw.rect(self.screen, WHITE, (WIDTH - 20 - self.paleta_width, self.paleta2_y, self.paleta_width, self.paleta_height))
            pygame.draw.ellipse(self.screen, self.pelota_color, (self.pelota_x, self.pelota_y, self.pelota_size, self.pelota_size))
            pygame.draw.aaline(self.screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

            # Dibujar nombres y puntajes
            self.dibujar_texto(f"{self.jugador_1_name}: {self.score1}", WHITE, WIDTH // 6, 20, font=self.letra_pequeña)
            self.dibujar_texto(f"{self.jugador_2_name}: {self.score2}", WHITE, 3 * WIDTH // 5, 20, font=self.letra_pequeña)

            pygame.display.flip()
            self.clock.tick(60)

# Ejecutar el juego
if __name__ == "__main__":
    game = juego_tenis()
    game.run()
