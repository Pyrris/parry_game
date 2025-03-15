import pygame

# class
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.player_idle = pygame.Surface((100, 150))
        self.player_idle.fill('cyan')

        self.image = self.player_idle
        self.rect = self.image.get_rect(midbottom = (800, 500))
        self.gravity = 0
        self.floor = 1000
        self.prev_y = self.rect.y

        self.move_right = 0
        self.move_left = 0
        self.jump = 0
        self.down = 0
        self.attack = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
               
        if keys[pygame.K_RIGHT]:
            self.move_right = 1
        if not keys[pygame.K_RIGHT]:
            self.move_right = 0
            
        if keys[pygame.K_LEFT]:
            self.move_left = 1
        if not keys[pygame.K_LEFT]:
            self.move_left = 0

    def player_movement(self):

        if self.move_right:
            self.rect.x += 10
        if self.move_left:
            self.rect.x -=10

    def apply_gravity(self):
        self.prev_y = self.rect.y
        self.gravity += 1
        self.rect.y += self.gravity
        if self.gravity >=101:
            self.gravity = 100

    def airborne(self):
        difference = self.rect.y - self.prev_y
        print('difference = ' + str(difference))
        if difference == 0:
            print('on ground')
            return False
        else:
            print('in air')
            return True

    def collision(self, rect_list):
        for rect in rect_list:
            if self.rect.colliderect(rect):
                self.gravity = 0












                
                # rel_xpos = 'right'
                # rel_ypos = 'down'
                #
                # rel_x = rect.centerx - self.rect.centerx
                # rel_y = rect.centery - self.rect.centery
                # if rel_x >= 0: rel_xpos = 'right'
                # else: rel_xpos = 'left'
                # if rel_y >= 0: rel_ypos = 'down'
                # else: rel_ypos = 'up'
                #
                # if rel_ypos == 'down':
                #     if rel_xpos == 'right':
                #         if rect.collidepoint(self.rect.bottomright):
                #             self.rect.bottom = rect.top
                #     if rel_xpos == 'left':
                #         if rect.collidepoint(self.rect.bottomleft):
                #             self.rect.bottom = rect.top
                # if rel_xpos == 'right':
                #     if rect.clipline((self.rect.right + 1, self.rect.bottom - 1), (self.rect.right + 1, self.rect.top + 1)):
                #         self.rect.right = rect.left - 1
                # if rel_xpos == 'left':
                #     if rect.clipline((self.rect.left -1, self.rect.bottom -1), (self.rect.left -1, self.rect.top +1)):
                #         self.rect.left = rect.right - 1



    def update(self):
        self.apply_gravity()
        self.player_input()
        self.player_movement()
        self.collision(arena_rect_list)
        self.airborne()

# funcs


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
floor_rect = floor_surf.get_rect(midbottom = (800, 800))
arena_rect_list = [floor_rect]

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
    
    player.draw(screen)
    player.update()
    print(player.sprite.move_left, player.sprite.move_right)

    # final updates
    pygame.display.update()
    clock.tick(60)
