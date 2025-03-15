import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def anim_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index +=0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.anim_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png')
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png')
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png')
            snail_2 = pygame.image.load('graphics/snail/snail2.png')
            self.frames = [snail_1, snail_2]
            y_pos = 300
            
        self.anim_index = 0
        self.image = self.frames[self.anim_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def anim_state(self):
        self.anim_index += 0.1
        if self.anim_index >= len(self.frames):
            self.anim_index = 0
        self.image = self.frames[int(self.anim_index)]


    def update(self):
        self.anim_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
            # .kill() kills the object

# sprite class is a neater wya to handle managing sprites


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return(obstacle_list)
    else: return []

def collisions(player, obstacle):
    if obstacle:
        for obstacle_rect in obstacle:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

def player_anim():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
# pygame.init is essential to initialise pygame library
screen = pygame.display.set_mode((800, 400), display=0)
# sets a variable that will display the window.
pygame.display.set_caption('Runner')
# names the game window.
clock = pygame.time.Clock()
# this creates a clock object
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
# This sets a font for generated text.
game_active = False
# This sets the game loop state
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.5)
bg_music.play(loops = -1)

# groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# test_surface = pygame.Surface((100, 200))
##this generates a rectangular 'surface'
# test_surface.fill('cyan')
##.fill changes the colour of the surface.

sky_surface = pygame.image.load('graphics/Sky.png').convert()

ground_surface = pygame.image.load('graphics/ground.png').convert()

# score_surf = test_font.render('My Game', False, (64,64,64))
# score_rect = score_surf.get_rect(center = (400, 50))

# obstacles
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))
# making a rect of an object and using that as our position will be better
# than manually placing them because of positional points on the rect.
player_grav = 0

#intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale_by(player_stand, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

title_surf = test_font.render('Runner', False, (111, 196, 169))
title_rect = title_surf.get_rect(center = (400, 50))

start_surf = test_font.render('Press SPACE to run', False, (111, 196, 169))
start_rect = start_surf.get_rect(center = (400, 350))

# Timer
obstacle_timer = pygame.USEREVENT + 1
# Add +1 when making a custom event so you don't overlap with pygame's events
pygame.time.set_timer(obstacle_timer, 1500)

snail_anim_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_anim_timer, 500)

fly_anim_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_anim_timer, 200)

while True:
    # game loop!
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # This checks if the player has pushed the window X.
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_grav = -20
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_grav = -20
                # print(event.pos)
                # prints the mouse pos when the mouse moves.
                # checks if the mouse button is pushed down
                # MOUSEBUTTONUP is also a valid for negative edge
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                # if randint(0,2):
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100), 300)))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100), 210)))
                    
            if event.type == snail_anim_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

                
    # draw all our elements
    # update everything
    
    if game_active:
            
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # screen.blit(score_surf, score_rect)
        score = display_score()

        # enemies
        # snail_rect.x -= 5
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surf, snail_rect)

        # player
        # player_grav += 1
        # if player_grav >= 300:
        #     player_grav = 300
        # player_rect.y += player_grav
        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300
        # player_anim()
        # screen.blit(player_surf, player_rect)
        
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()
        # need to both draw and update the sprite class

        # Obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print('jump')

        # collision
        game_active = collision_sprite()
        # if player_rect.colliderect(snail_rect):
        #     game_active = False
        # game_active = collisions(player_rect, obstacle_rect_list)

        # mouse_pos = pygame.mouse.get_pos()
        # if player_rect.collidepoint(mouse_pos):
        #     pygame.mouse.get_pressed()
        #     print('Collision')
            # example of collision with mouse pos
        
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_grav = 0

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(title_surf, title_rect)

        if score == 0: screen.blit(start_surf, start_rect)
        else: screen.blit(score_message, score_message_rect)
    pygame.display.update()
    # this updates the window every loop.
    clock.tick(60)
    # this sets the framerate.
    
