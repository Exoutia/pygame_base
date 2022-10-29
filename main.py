
import pygame
from sys import exit


def display_score():
    curr_time = pygame.time.get_ticks()//1000 - start_time//1000
    score_surf = text_font.render(f"score: {curr_time}", False, (12, 122, 12))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    # print(curr_time)


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True
start_time = 0

# Game interface
game_name = text_font.render('Pixel Runner', False, '#0A2559')
game_name_rect = game_name.get_rect(center = (400, 80))
inst_sur = text_font.render("Press 'SPACE' to restart", False, '#0A2559')
inst_rect = inst_sur.get_rect(midbottom = (400, 350))


ground_surf = pygame.image.load('graphics/ground.png').convert()
sky_surf = pygame.image.load('graphics/wall.png').convert()
sky_surf = pygame.transform.scale(sky_surf, (800, 300))


# score_surf = text_font.render('Score: 00', False, (12,122,12))
# score_rect = score_surf.get_rect(center = (400, 50))

ufo_surf = pygame.image.load('graphics/animal/ufo.png').convert_alpha()
ufo_rect = ufo_surf.get_rect(center = (700, 250))

player_surf = pygame.image.load('graphics/animal/player/player_stand.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_grav = 0

# intro screen
player_stand = pygame.image.load('graphics/animal/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center=(400, 200))


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
                    ufo_rect.left = 800
                    start_time = pygame.time.get_ticks()

    if game_active:

        screen.blit(ground_surf, (0,300))
        screen.blit(sky_surf, (0,0))
        # pygame.draw.rect(screen, '#B4DEE4', score_rect, border_radius=20)
        # pygame.draw.rect(screen, '#B4DEE4', score_rect, 10, 20)
        # screen.blit(score_surf, score_rect)
        display_score()

        ufo_rect.right -= 5
        if ufo_rect.right < 0:
            ufo_rect.left = 800
        screen.blit(ufo_surf, ufo_rect)


        #  Player
        player_grav += 1
        player_rect.bottom += player_grav
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        # Collisions
        if ufo_rect.colliderect(player_rect):
            game_active = False

    else:
        # screen.blit(game_over_surf, (0,0))
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        screen.blit(inst_sur, inst_rect)


        # screen.blit()

    pygame.display.update()
    clock.tick(60)