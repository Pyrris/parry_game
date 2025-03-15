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

    def apply_gravity(self):
        self.prev_y = self.rect.y
        self.gravity += 1
        self.rect.y += self.gravity
        if self.gravity >=101:
            self.gravity = 100

    def airborne(self):
        global airborne
        difference = self.rect.y - self.prev_y
        if difference == 0:
            return False
        else:
            return True

    def player_floor(self, y_pos):
        self.floor = y_pos
        if self.rect.bottom > self.floor:
            self.rect.bottom = self.floor

    def collision(self, rect_list):
        if self.airborne():
            for rect in rect_list:
                if self.rect.colliderect(rect):
                    self.player_floor(rect.top)
                    self.gravity = 0                  

    def update(self):
        self.apply_gravity()

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
floor_surf = pygame.Surface((1400, 100))
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
    player.sprite.collision(arena_rect_list)

    # final updates
    pygame.display.update()
    clock.tick(60)
