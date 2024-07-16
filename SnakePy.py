import os
import pygame as pg
import time as tm
import random as rd
import sys

# Configuración del juego
snake_speed = 15
window_x = 1366
window_y = 768
black = pg.Color(0, 0, 18)
white = pg.Color(255, 255, 255)
red = pg.Color(255, 0, 0)
green = pg.Color(0, 255, 0)
blue = pg.Color(0, 0, 255)
yellow = pg.Color(255, 255, 0)

# Inicialización de Pygame
pg.init()
pg.display.set_caption('SnakePy')

# Ocultar el cursor del mouse
pg.mouse.set_visible(False)

# Directorio base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Cargar sonidos
menu_sound = pg.mixer.Sound(os.path.join(base_dir, 'music', 'menu_sound.mp3'))
game_sound = pg.mixer.Sound(os.path.join(base_dir, 'music', 'game_sound.mp3'))
game_over_sound = pg.mixer.Sound(os.path.join(base_dir, 'music', 'game_over_sound.mp3'))
eat_sound = pg.mixer.Sound(os.path.join(base_dir, 'music', 'eat_sound.mp3'))
score_sound = pg.mixer.Sound(os.path.join(base_dir, 'music', 'score_sound.mp3'))

# Cargar y establecer el icono
icon = pg.image.load(os.path.join(base_dir, 'images', 'Icon_SnakePy.png'))
pg.display.set_icon(icon)

game_window = pg.display.set_mode((window_x, window_y))
fps = pg.time.Clock()

# Variables del juego
max_score = 0
max_time = 0.0
start_time = 0
elapsed_time = 0

def show_score(color, font, size):
    score_font = pg.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect(topleft=(10, 10))
    game_window.blit(score_surface, score_rect)

def show_time(color, font, size, elapsed_time):
    time_font = pg.font.SysFont(font, size)
    time_surface = time_font.render(f'Time : {elapsed_time:.2f}', True, color)
    time_rect = time_surface.get_rect(topright=(window_x - 10, 10))
    game_window.blit(time_surface, time_rect)

def play_sound(sound, loop=False):
    if loop:
        sound.play(loops=-1)
    else:
        sound.play()

def stop_sound(sound):
    sound.stop()

def show_menu():
    global max_score, max_time
    play_sound(menu_sound, loop=True)  # Reproducir sonido de menú en bucle
    game_window.fill(black)
    title_font = pg.font.SysFont('times new roman', 80)
    score_font = pg.font.SysFont('times new roman', 30)
    time_font = pg.font.SysFont('times new roman', 30)
    instruction_font = pg.font.SysFont('times new roman', 25)
    
    title_surface = title_font.render('SnakePy', True, green)
    title_rect = title_surface.get_rect(center=(window_x / 2, window_y / 4))
    
    max_score_surface = score_font.render('Max Score : ' + str(max_score), True, blue)
    max_score_rect = max_score_surface.get_rect(center=(window_x / 2, window_y / 2))

    max_time_surface = time_font.render(f'Max Time : {max_time:.2f}', True, yellow)
    max_time_rect = max_time_surface.get_rect(center=(window_x / 2, window_y / 1.8))

    instruction_surface = instruction_font.render('Press Q to exit or C to play', True, white)
    instruction_rect = instruction_surface.get_rect(center=(window_x / 2, window_y / 1.5))

    version_font = pg.font.SysFont('times new roman', 20)
    version_surface = version_font.render('Version 1.1.2', True, white)
    version_rect = version_surface.get_rect(bottomleft=(10, window_y - 10))

    author_surface = version_font.render('by Hector Aliaga', True, white)
    author_rect = author_surface.get_rect(bottomright=(window_x - 10, window_y - 10))

    game_window.blit(title_surface, title_rect)
    game_window.blit(max_score_surface, max_score_rect)
    game_window.blit(max_time_surface, max_time_rect)
    game_window.blit(instruction_surface, instruction_rect)
    game_window.blit(version_surface, version_rect)
    game_window.blit(author_surface, author_rect)
    pg.display.flip()
    tm.sleep(1)

    wait_for_input()

def game_over():
    global max_score, max_time, elapsed_time
    stop_sound(game_sound)  # Detener música del juego
    play_sound(game_over_sound)  # Reproducir sonido de game over
    end_time = tm.time()
    elapsed_time = end_time - start_time
    game_window.fill(black)
    my_font_score = pg.font.SysFont('times new roman', 50)
    my_font_time = pg.font.SysFont('times new roman', 40)
    instruction_font = pg.font.SysFont('times new roman', 25)
    
    game_over_surface = my_font_score.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect(midtop=(window_x / 2, window_y / 4))

    time_surface = my_font_time.render(f'Your Time is: {elapsed_time:.2f}', True, yellow)
    time_rect = time_surface.get_rect(midtop=(window_x / 2, window_y / 3))

    instruction_surface = instruction_font.render('Press Q to exit or C to play again', True, white)
    instruction_rect = instruction_surface.get_rect(center=(window_x / 2, window_y / 1.5))

    game_window.blit(game_over_surface, game_over_rect)
    game_window.blit(time_surface, time_rect)
    game_window.blit(instruction_surface, instruction_rect)
    pg.display.flip()
    tm.sleep(1)

    if score > max_score:
        max_score = score
    if elapsed_time > max_time:
        max_time = elapsed_time

    stop_sound(game_over_sound)  # Detener sonido de game over
    play_sound(menu_sound, loop=True)  # Reproducir sonido de menú en bucle

    wait_for_input()

def wait_for_input():
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    stop_sound(menu_sound)  # Detener música del menú
                    waiting = False
                    game_window.fill(black)
                    pg.display.flip()
                elif event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

# Bucle principal del juego
def main():
    global snake_position, snake_body, fruit_position, fruit_spawn, direction, change_to, score, start_time, last_score_sound

    show_menu()

    # Inicialización de variables del juego
    snake_position = [100, 60]
    snake_body = [[100, 60], [80, 60], [60, 60], [40, 60]]
    fruit_position = [rd.randrange(1, (window_x // 20)) * 20, 
                      rd.randrange(1, (window_y // 20)) * 20]
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

    play_sound(game_sound, loop=True)  # Reproducir música del juego en bucle
    start_time = tm.time()
    run_over = False
    while not run_over:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run_over = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pg.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pg.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pg.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'
                elif event.key == pg.K_c:
                    stop_sound(menu_sound)  # Detener música del menú
                    stop_sound(game_sound)  # Detener música del juego
                    stop_sound(game_over_sound)  # Detener música de game over

        # Actualización de la dirección
        direction = change_to

        # Movimiento de la serpiente
        if direction == 'UP':
            snake_position[1] -= 20
        elif direction == 'DOWN':
            snake_position[1] += 20
        elif direction == 'LEFT':
            snake_position[0] -= 20
        elif direction == 'RIGHT':
            snake_position[0] += 20

        # Crecimiento de la serpiente
        snake_body.insert(0, list(snake_position))
        if snake_position == fruit_position:
            score += 10
            play_sound(eat_sound)  # Reproducir sonido de comer
            fruit_spawn = False
            last_score_sound = 0  # Reiniciar el estado del sonido de puntaje
        else:
            snake_body.pop()

        # Generación de nuevas frutas
        if not fruit_spawn:
            fruit_position = [rd.randrange(1, (window_x // 20)) * 20, 
                              rd.randrange(1, (window_y // 20)) * 20]
        fruit_spawn = True

        # Renderización de la ventana del juego
        game_window.fill(black)
        for pos in snake_body:
            pg.draw.rect(game_window, green, pg.Rect(pos[0], pos[1], 20, 20))
        pg.draw.rect(game_window, red, pg.Rect(fruit_position[0], fruit_position[1], 20, 20))

        # Comprobación de colisiones
        if (snake_position[0] < 0 or snake_position[0] > window_x - 20 or
            snake_position[1] < 0 or snake_position[1] > window_y - 20):
            game_over()
            main()
        
        for block in snake_body[1:]:
            if snake_position == block:
                game_over()
                main()

        # Mostrar puntuación y tiempo
        elapsed_time = tm.time() - start_time
        show_score(white, 'times new roman', 20)
        show_time(white, 'times new roman', 20, elapsed_time)

        # Reproducir sonido de puntaje cada 100 puntos una sola vez
        if score % 100 == 0 and score != 0 and score != last_score_sound:
            play_sound(score_sound)
            last_score_sound = score

        pg.display.update()
        fps.tick(snake_speed)

if __name__ == "__main__":
    main()
    pg.quit()
    sys.exit()