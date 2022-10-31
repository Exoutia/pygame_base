
import pygame
from sys import exit
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/animal/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/animal/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/animal/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(150, 300))
        self.gravity = 0

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity -= 20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()









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
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x> -100]
        return obstacle_list
    else: return []

def collision_check(player_rect, obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if player_rect.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    # Player animation walking if player is in ground
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_surf = player_walk[int(player_index)]
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

# Backgrounds
ground_surf = pygame.image.load('graphics/backgrounds/ground.png').convert()
sky_surf = pygame.image.load('graphics/backgrounds/wall.png').convert()
sky_surf = pygame.transform.scale(sky_surf, (800, 300))


# score_surf = text_font.render('Score: 00', False, (12,122,12))
# score_rect = score_surf.get_rect(center = (400, 50))

# Obstacle
ufo_surf = pygame.image.load('graphics/animal/enemy/ufo.png').convert_alpha()

snail_frame_1 = pygame.image.load('graphics/animal/enemy/snail.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/animal/enemy/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/animal/enemy/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/animal/enemy/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]



obstacle_rect_list = []


player_walk_1 = pygame.image.load('graphics/animal/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/animal/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/animal/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
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
pygame.time.set_timer(obstacle_timer, 1500)

snail_tiemr = pygame.USEREVENT + 2
pygame.time.set_timer(snail_tiemr, 500)
fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)

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
                    start_time = pygame.time.get_ticks()

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 1):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900, 1200), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900, 1100), 170)))

            if event.type == fly_timer:
                if fly_frame_index: fly_frame_index = 0
                else: fly_frame_index = 1
                fly_surf = fly_frames[fly_frame_index]

            if event.type == snail_tiemr:
                if snail_frame_index: snail_frame_index = 0
                else: snail_frame_index = 1
                snail_surf = snail_frames[snail_frame_index]





    if game_active:

        screen.blit(ground_surf, (0,300))
        screen.blit(sky_surf, (0,0))
        score = display_score()




        #  Player
        player_grav += 1
        player_rect.bottom += player_grav
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        player_animation()
        screen.blit(player_surf, player_rect)
        player.draw(screen)
        player.update()

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collisions
        game_active = collision_check(player_rect, obstacle_rect_list)

    else:
        # screen.blit(game_over_surf, (0,0))
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_grav = 0

        score_msg = text_font.render(f"Your Score: {score}", False, '#0A2559')
        score_msg_rect = score_msg.get_rect(center = (600, 200))
        screen.blit(score_msg, score_msg_rect)
        screen.blit(game_name, game_name_rect)
        screen.blit(inst_sur, inst_rect)


        # screen.blit()

    pygame.display.update()
    clock.tick(60)