import pygame

# class
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.player_idle = pygame.Surface((50, 75))
        self.player_idle.fill('cyan')

        self.image = self.player_idle
        self.rect = self.image.get_rect(midbottom = (800, 500))
        self.gravity = 0
        self.friction = 0
        self.floor = 1000

        self.dx = 0
        self.dy = 0
        self.prev_y = 0
        self.air = True
        self.can_dash = True
        self.timer = 15
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

        if keys[pygame.K_UP]:
            self.jump = 1
        if not keys[pygame.K_UP]:
            self.jump = 0

    def player_movement(self):
        
        if self.move_right:
            self.dx += 2
            if self.dx >= 10:
                self.dx = 11

        if self.move_left:
            self.dx += -2
            if self.dx <= -10:
                self.dx = -11
                

        if self.jump and not self.air:
            self.gravity = 0
            self.dy = -50
    
    def apply_friction(self):
        self.friction = 1
        if self.dx > 0:
            self.dx -= self.friction
        if self.dx < 0:
            self.dx += self.friction
        

    def apply_gravity(self):
        self.gravity += 1
        if self.gravity >=101:
            self.gravity = 100
        self.dy += self.gravity

    def airborne(self):
        self.difference = self.rect.y - self.prev_y
        print((self.rect.y, self.prev_y))
        print('difference = ' + str(self.difference))
        if self.difference == 0:
            print('on ground')
            self.air = False
        else:
            print('in air')
            self.air = True

    def collision(self, rect_list):
        for rect in rect_list:
            if rect.colliderect(self.rect.x + self.dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                if self.dx > 0:
                    self.dx = rect.left - self.rect.right
                if self.dx <0:
                    self.dx = rect.right - self.rect.left
            if rect.colliderect(self.rect.x, self.rect.y + self.dy, self.image.get_width(), self.image.get_height()):
                if self.gravity < 0 and self.rect.top >= rect.bottom:
                    self.dy = rect.bottom - self.rect.top
                    self.gravity = 0
                elif self.gravity >= 0 and self.rect.bottom <= rect.top:
                    self.dy = rect.top - self.rect.bottom
                    self.gravity = 0


    def update(self):
        self.apply_gravity()
        self.player_input()
        self.airborne()
        self.player_movement()
        self.apply_friction()
        self.collision(arena_rect_list)
        self.prev_y = self.rect.y
        self.rect.x += self.dx
        self.rect.y += self.dy
        print(self.dx)

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

    # final updates
    pygame.display.update()
    clock.tick(60)
