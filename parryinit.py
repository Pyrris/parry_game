import pygame
from timer import Timer
from EntityClasses import Player

# funcs

def placeholder_visuals(entity):
    if entity.is_dash:
        entity.player_idle.fill('blue')
    else:
        entity.player_idle.fill('cyan')

    if entity.facing == 'right':
            pygame.draw.line(screen, 'pink', entity.rect.topleft, entity.rect.midright, 3)
            pygame.draw.line(screen, 'pink', entity.rect.bottomleft, entity.rect.midright, 3)
    if entity.facing == 'left':
            pygame.draw.line(screen, 'pink', entity.rect.topright, entity.rect.midleft, 3)
            pygame.draw.line(screen, 'pink', entity.rect.bottomright, entity.rect.midleft, 3)

    if entity.attack == 1:
        pygame.draw.rect(screen, 'red', entity.atkrect)

        
def collision(entity, rect_list):
    for rect in rect_list:

        if rect.colliderect(entity.rect.x + entity.dx, entity.rect.y, entity.image.get_width(), entity.image.get_height()):
            if entity.dx > 0:
                entity.dx = rect.left - entity.rect.right
            if entity.dx < 0:
                entity.dx = rect.right - entity.rect.left

        if rect.colliderect(entity.rect.x, entity.rect.y + entity.dy, entity.image.get_width(), entity.image.get_height()):
            if entity.dy < 0 and entity.rect.top >= rect.bottom:
                entity.dy = rect.bottom - entity.rect.top
                entity.gravity = 0
            if entity.dy >= 0 and entity.rect.bottom <= rect.top:
                entity.dy = rect.top - entity.rect.bottom
                entity.gravity = 0

# inits
pygame.init()
screen = pygame.display.set_mode((1600, 900), display=0)
pygame.display.set_caption('Parry')
clock = pygame.time.Clock()
is_running = True

# groups
player = pygame.sprite.GroupSingle()
player.add(Player())

# surf/rects
floor_surf = pygame.Surface((1000, 100))
floor_surf_thin = pygame.Surface((400, 50))
floor_rect = floor_surf.get_rect(midbottom=(800, 800))
floor_rect_left = floor_surf_thin.get_rect(midright=(500, 550))
floor_rect_right = floor_surf_thin.get_rect(midleft=(1100, 550))
arena_rect_list = [floor_rect, floor_rect_left, floor_rect_right]

# timer
# NOTE: unused
simple_timer = Timer(1000)

# game loop
while is_running:

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # draw and update sprites and rects
    screen.fill('white')

    pygame.draw.rect(screen, 'black', floor_rect)
    pygame.draw.rect(screen, 'black', floor_rect_left)
    pygame.draw.rect(screen, 'black', floor_rect_right)

    player.draw(screen)
    player.update()
    placeholder_visuals(player.sprite)
    collision(player.sprite, arena_rect_list)
    player.sprite.update_pos()

    # final updates
    pygame.display.update()
    clock.tick(60)
