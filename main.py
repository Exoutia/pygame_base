
import pygame
from sys import exit
from random import randint


def display_score():
    curr_time = pygame.time.get_ticks()//1000 - start_time//1000
    score_surf = text_font.render(f"score: {curr_time}", False, (12, 122, 12))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return curr_time

def obstacle_movement(obstacle_list: list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            screen.blit(ufo_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x> -100]
        return obstacle_list
    else: return []

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True
start_time = 0
score = 0


ground_surf = pygame.image.load('graphics/ground.png').convert()
sky_surf = pygame.image.load('graphics/wall.png').convert()
sky_surf = pygame.transform.scale(sky_surf, (800, 300))


# score_surf = text_font.render('Score: 00', False, (12,122,12))
# score_rect = score_surf.get_rect(center = (400, 50))

# Obstacle
ufo_surf = pygame.image.load('graphics/animal/ufo.png').convert_alpha()

obstacle_rect_list = []


player_surf = pygame.image.load('graphics/animal/player/player_stand.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_grav = 0

# intro screen
player_stand = pygame.image.load('graphics/animal/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = text_font.render('Pixel Runner', False, '#0A2559')
game_name_rect = game_name.get_rect(center = (400, 80))
inst_sur = text_font.render("Press 'SPACE' to restart", False, '#0A2559')
inst_rect = inst_sur.get_rect(midbottom = (400, 350))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 800)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_grav = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    # print('jump')
                    player_grav = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    obstacle_rect_list = [] 
                    start_time = pygame.time.get_ticks()

        if event.type == obstacle_timer and game_active:
            enemy_rect = ufo_surf.get_rect(midright = (randint(900, 1000), 170))
            obstacle_rect_list.append(enemy_rect)


    if game_active:

        screen.blit(ground_surf, (0,300))
        screen.blit(sky_surf, (0,0))
        score = display_score()




        #  Player
        player_grav += 1
        player_rect.bottom += player_grav
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        enemy_rect = None
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        if obstacle_rect_list:
            enemy_rect = obstacle_rect_list[0]

        # Collisions
        if enemy_rect and enemy_rect.colliderect(player_rect):
            game_active = False

    else:
        # screen.blit(game_over_surf, (0,0))
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)

        score_msg = text_font.render(f"Your Score: {score}", False, '#0A2559')
        score_msg_rect = score_msg.get_rect(center = (600, 200))
        screen.blit(score_msg, score_msg_rect)
        screen.blit(game_name, game_name_rect)
        screen.blit(inst_sur, inst_rect)


        # screen.blit()

    pygame.display.update()
    clock.tick(60)