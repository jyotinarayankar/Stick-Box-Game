# without Asyncio

import pygame
from pygame.locals import *
import random
import time
import os
import sys

# Game constants
WIDTH = 1214
HEIGHT = 750
FPS = 60
GRAVITY = 0.5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# Initialize Pygame
pygame.init()
pygame.display.set_caption('Stick Box Game by Jyoti')

# Set up the screen size based on the device's display
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, int(HEIGHT / 25))
medium_font = pygame.font.Font(None, int(HEIGHT / 12))
large_font = pygame.font.Font(None, int(HEIGHT / 6))

# Load sound files
die_sound = pygame.mixer.Sound('Audio\\die.wav')
hit_sound = pygame.mixer.Sound('Audio\\hit.wav')
point_sound = pygame.mixer.Sound('Audio\\point.wav')
swoosh_sound = pygame.mixer.Sound('Audio\\swoosh.wav')
wing_sound = pygame.mixer.Sound('Audio\\wing.wav')


def draw_text(text, x, y, font, color=WHITE):
    surface = font.render(text, True, color)
    text_rect = surface.get_rect(center=(x, y))
    screen.blit(surface, text_rect)


def show_start_screen():
    screen.fill(BLACK)
    draw_text("Stick Box", WIDTH/2, HEIGHT/2 - int(HEIGHT / 25), large_font)
    draw_text("Tap to Play", WIDTH/2, HEIGHT/1.3 + int(HEIGHT / 25), font, RED)
    pygame.display.flip()
    pygame.time.wait(2000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                die_sound.play()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                point_sound.play()
                return


def show_input_screen(player_name):
    screen.fill(BLACK)
    draw_text("Stick Box", WIDTH/2, HEIGHT/6, large_font, RED)
    draw_text("Enter Player Name:", WIDTH/2, HEIGHT/2 - int(HEIGHT / 25), font)
    draw_text(player_name, WIDTH/2, HEIGHT/2 + int(HEIGHT/30), medium_font, RED)
    # draw_text("Press 'SPACE' or 'CLICK' to Jump", WIDTH/2, HEIGHT - int(HEIGHT / 3), font, WHITE)
    draw_text("Developed By: Jyotinarayan Kar", WIDTH/2, HEIGHT - int(HEIGHT / 30), font, WHITE)
    pygame.display.flip()



def show_game_over_screen(score, player_name, high_scores):
    screen.fill(BLACK)
    # die_sound.play() # Play sound when the game is over
    draw_text("Game Over", WIDTH/2, HEIGHT/6, large_font, RED)
    draw_text("Score: ", WIDTH/2 - int(WIDTH / 24), HEIGHT/2 - int(HEIGHT / 18), medium_font)
    draw_text(str(score - 1), WIDTH/2 + int(WIDTH / 24), HEIGHT/2 - int(HEIGHT / 18), medium_font, RED)
    draw_text("Player Name:", WIDTH/10, HEIGHT/2.5, font, YELLOW)
    draw_text(str(player_name), WIDTH/10, HEIGHT/2.5 + int(HEIGHT / 25), font)
    draw_text("High Scores:", WIDTH/1.11, HEIGHT/2.5, font, GREEN)
    for i, high_score in enumerate(high_scores):
        draw_text(f"{i+1}. {high_score[0]} - {high_score[1]}", WIDTH/1.11, HEIGHT/2.5 + int(HEIGHT / 25) + i*int(HEIGHT / 30), font)
    draw_text("Press 'SPACE' or 'Click' to Play Again as the Same Player", WIDTH/2, HEIGHT/2 + int(HEIGHT / 4), font)
    draw_text("Press 'R' to Change Player Name and Play Again", WIDTH/2, HEIGHT/2 + int(HEIGHT / 3.3), font)
    draw_text("Press 'Q' to Quit the Game", WIDTH/2, HEIGHT/2 + int(HEIGHT / 2.2), font,RED)  # Quit game option
    pygame.display.flip()
    pygame.time.wait(2000)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((int(HEIGHT / 15), int(HEIGHT / 15)))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 4, HEIGHT / 2)
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def flap(self):
        self.velocity = -int(HEIGHT / 75)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((int(HEIGHT / 15), height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= int(WIDTH / 120)


def reset_game():
    bird.rect.center = (WIDTH / 4, HEIGHT / 2)
    bird.velocity = 0
    score = 0
    pipes.empty()
    all_sprites.empty()
    all_sprites.add(bird)
    start_time = time.time()
    pipe_timer = 0
    return score, start_time, pipe_timer


all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()

bird = Bird()
all_sprites.add(bird)

score = 0
high_scores = []

running = True
buffer_time = 2
start_time = time.time()
pipe_interval = 2
pipe_timer = 0
game_over = False

show_start_screen()
player_name = ""

input_active = True

while input_active:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(player_name) > 0:
                input_active = False
                point_sound.play()
            if event.key == pygame.K_SPACE and len(player_name) > 0:
                input_active = False
                point_sound.play()
            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            else:
                if event.unicode.isalnum() and len(player_name) < 10:
                    player_name += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN and len(player_name) > 0:
            input_active = False
            point_sound.play()


    show_input_screen(player_name)
    pygame.display.flip()


def draw_game_screen(score, player_name):
    draw_text("Player: "+player_name, WIDTH/4, HEIGHT/21, font, WHITE)



while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    point_sound.play()
                    game_over = False
                    score, start_time, pipe_timer = reset_game()
                    show_input_screen(player_name)
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Added mouse button event
                    point_sound.play()
                    game_over = False
                    score, start_time, pipe_timer = reset_game()
                    show_input_screen(player_name)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    swoosh_sound.play()
                    game_over = False
                    score, start_time, pipe_timer = reset_game()
                    player_name = ""
                    input_active = True
                    while input_active:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN and len(player_name) > 0:
                                    input_active = False
                                    point_sound.play()
                                if event.key == pygame.K_SPACE and len(player_name) > 0:
                                    input_active = False
                                    point_sound.play()
                                elif event.key == pygame.K_BACKSPACE:
                                    player_name = player_name[:-1]
                                else:
                                    if event.unicode.isalnum() and len(player_name) < 10:
                                        player_name += event.unicode
                            elif event.type == pygame.MOUSEBUTTONDOWN and len(player_name) > 0:
                                input_active = False
                                point_sound.play()

                        show_input_screen(player_name)
                        pygame.display.flip()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # Quit game option
                    die_sound.play()
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Quit game option
                    die_sound.play()
                    running = False
            else:
                if event.type ==pygame.MOUSEBUTTONDOWN:  # Added mouse button event
                    bird.flap()
                  # Play sound when the bird flaps
                    wing_sound.play()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.flap()
                  # Play sound when the bird flaps
                    wing_sound.play()
        # Handle MOUSEBUTTONUP event
        elif event.type == pygame.MOUSEBUTTONUP:
            if not game_over:
                pass
                # bird.flap()

    all_sprites.update()

    if not game_over:

        if pygame.sprite.spritecollide(bird, pipes, False):
            game_over = True
          # Play sound when collision occurs
            # hit_sound.play()
            high_scores.append((player_name, score))
            high_scores.sort(key=lambda x: x[1], reverse=True)
            if len(high_scores) > 5:
                high_scores.pop()
          # Play sound when the game is over
            hit_sound.play()
            show_game_over_screen(score, player_name, high_scores)

        if bird.rect.bottom >= HEIGHT or bird.rect.top < 0:
            game_over = True
            high_scores.append((player_name, score))
            high_scores.sort(key=lambda x: x[1], reverse=True)
            if len(high_scores) > 5:
                high_scores.pop()
            hit_sound.play()
            show_game_over_screen(score, player_name, high_scores)


        current_time = time.time() - start_time
        if current_time > buffer_time:
            if current_time > pipe_timer:
                gap_height = random.randint(150, 300)
                pipe_height = random.randint(50, HEIGHT - gap_height - 50)
                top_pipe = Pipe(WIDTH, 0, pipe_height)
                bottom_pipe = Pipe(WIDTH, pipe_height + gap_height, HEIGHT - pipe_height - gap_height)
                pipes.add(top_pipe, bottom_pipe)
                all_sprites.add(top_pipe, bottom_pipe)
                pipe_timer = current_time + pipe_interval

        score += 1

    screen.fill(BLACK)
    draw_game_screen(score, player_name)
    all_sprites.draw(screen)

    if not game_over:
        draw_text("Score: " + str(score - 1), WIDTH/1.33, HEIGHT/20, font, YELLOW)
    if game_over:
        show_game_over_screen(score, player_name, high_scores)

    pygame.display.flip()

pygame.quit()