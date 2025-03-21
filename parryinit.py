import pygame
from timer import Timer

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
        self.facing = 'right'

        self.dx = 0
        self.dy = 0
        self.prev_y = 0
        self.air = True
        self.is_dash = False
        self.dash_ready = True
        self.frametime = 0
        self.jumptime = 0
        self.dashtime = 0
        self.readytime = 0
        
        self.jump = 0
        self.down = 0
        self.attack = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
               
        if keys[pygame.K_RIGHT]:
            self.move_right = 1
            self.facing = 'right'
        if not keys[pygame.K_RIGHT]:
            self.move_right = 0
            
        if keys[pygame.K_LEFT]:
            self.move_left = 1
            self.facing = 'left'
        if not keys[pygame.K_LEFT]:
            self.move_left = 0
        
        if keys[pygame.K_p]:
            self.rect.x = 800
            self.rect.y = 500
            self.dy = 0
            self.dx = 0

        if self.move_right or self.move_left:
            self.is_pressed = True
        else:
            self.is_pressed = False


        if keys[pygame.K_UP]:
            self.jump = 1
        if not keys[pygame.K_UP]:
            self.jump = 0

        if self.jump == 1:
            self.jumptime +=1
        else:
            self.jumptime = 0

    def player_movement(self):
        
        # dash checks and timer
        if self.dash_ready and self.is_pressed and not self.air:
            self.is_dash = True
            self.dash_ready = False
        else:
            self.readytime += 1
            if self.readytime >= 30 and not self.is_pressed: # dash cooldown
                self.dash_ready = True
                self.readytime = 0
            
        if self.is_dash:
            self.dashtime += 1
            if self.dashtime >= 15: # how many frames you dash for
                    self.is_dash = False
                    self.dashtime = 0

        print('dash = ' + str(self.is_dash))
        print('press = ' + str(self.is_pressed))

        movespeed = 0
        speed_cap = 10

        if self.is_pressed:
            movespeed = 2
            if self.is_dash:
                movespeed = movespeed * 2
                speed_cap = int(speed_cap * 1.5)
            if self.air:
                movespeed = 1

        if self.air:
            speed_cap = 50
            if self.frametime in (1, 3):
                if self.facing == 'right':
                    self.dx += movespeed
                else:
                    self.dx -= movespeed

        else:                       
            if self.facing == 'right':
                self.dx += movespeed
            else:
                self.dx -= movespeed
            
        if self.dx >= speed_cap + 1:
            self.dx = speed_cap
        if self.dx <= speed_cap - (speed_cap * 2) - 1:
            self.dx = speed_cap - (speed_cap * 2)

        if self.jump and not self.air:
            self.gravity = 0
            self.dy -= 18

        # movespeed cap = 10
        # acceleration = 2
        # dash cap = 15
        # dash acceleration = 5
        # air speed = 1
        # no air speed cap
    
    def placeholder_sprite_changes(self):
        if self.is_dash:
            self.player_idle.fill('blue')
        else:
            self.player_idle.fill('cyan')

        if self.facing == 'right':
            pygame.draw.line(screen, 'pink', self.rect.topleft, self.rect.midright, 3)
            pygame.draw.line(screen, 'pink', self.rect.bottomleft, self.rect.midright, 3)
        if self.facing == 'left':
            pygame.draw.line(screen, 'pink', self.rect.topright, self.rect.midleft, 3)
            pygame.draw.line(screen, 'pink', self.rect.bottomright, self.rect.midleft, 3)

    def apply_friction(self):
        if self.frametime in (0, 2):
            self.friction = 1.5
            
            if self.dx > 0 and not self.air:
                self.dx = int(self.dx // self.friction)
                if self.dx < 0:
                    self.dx = 0
                    
            if self.dx < 0 and not self.air:
                self.dx = int(self.dx // self.friction) +1
                if self.dx > 0:
                    self.dx = 0
        
    def apply_gravity(self):
        if self.frametime == 4:
            self.gravity += 1
            self.dy += self.gravity
            if self.dy >=31:
                self.dy = 30
            self.frametime = 0
        self.frametime +=1

    def airborne(self):
        self.difference = self.rect.y - self.prev_y
        print((self.rect.y, self.prev_y))
        print('difference = ' + str(self.difference))
        if self.difference == 0:
            pass
        else:
            pass

    def collision(self, rect_list):
        for rect in rect_list:
            
            if rect.colliderect(self.rect.x + self.dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                if self.dx > 0:
                    self.dx = rect.left - self.rect.right
                if self.dx <0:
                    self.dx = rect.right - self.rect.left
                    
            if rect.colliderect(self.rect.x, self.rect.y + self.dy, self.image.get_width(), self.image.get_height()):
                if self.dy < 0 and self.rect.top >= rect.bottom:
                    self.dy = rect.bottom - self.rect.top
                    self.gravity = 0
                if self.dy >= 0 and self.rect.bottom <= rect.top:
                    self.dy = rect.top - self.rect.bottom
                    self.gravity = 0
                    # self.air = False

    def update(self):
        self.apply_gravity()
        self.player_input()
        self.airborne()
        self.player_movement()
        self.apply_friction()
        self.collision(arena_rect_list)
        self.placeholder_sprite_changes()
        self.prev_y = self.rect.y
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.dy == 0:
            self.air = False
        else:
            self.air = True
        print(self.dx)
        print(self.dy)
        print('air = ' + str(self.air))

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
floor_surf_thin = pygame.Surface((400, 50))
floor_rect = floor_surf.get_rect(midbottom = (800, 800))
floor_rect_left = floor_surf_thin.get_rect(midright = (500, 550))
floor_rect_right = floor_surf_thin.get_rect(midleft = (1100, 550))
arena_rect_list = [floor_rect, floor_rect_left, floor_rect_right]

# timer
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
    # pygame.draw.line(screen, 'pink', player.sprite.rect.topleft, player.sprite.rect.midright, 10)
    
    player.draw(screen)
    player.update()

    # final updates
    pygame.display.update()
    clock.tick(60)
