import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # define the character box, colour it cyan
        self.player_idle = pygame.Surface((50, 75))
        self.player_idle.fill('cyan')

        # Sets the player sprite
        self.image = self.player_idle
        # add a rect that is the same as the current image
        self.rect = self.image.get_rect(midbottom=(800, 500))
        self.atkrect = None
        # Initial Orientation
        self.move_right = 0
        self.move_left = 0
        self.facing = 'right'
        # Deprecated
        self.floor = 1000
        
        # Define some physics bits
        self.gravity = 0
        self.friction = 0
        self.dx = 0
        self.dy = 0
        self.prev_y = 0

        # player state data
        self.air = True
        self.is_dash = False
        self.dash_ready = True

        # player action timers, value is frames
        self.timerDict = {}
        self.timerDict['Phys'] = 0
        self.timerDict['jump'] = 0
        self.timerDict['DashLen'] = 15
        self.timerDict['DashCD'] = 30
        # TODO: Implement
        self.timerDict['Atk'] = 0

        # TODO: Implement
        self.down = 0

    def reset_pos(self):
        self.rect.x = 800
        self.rect.y = 500
        self.dy = 0
        self.dx = 0

    def player_input(self):
        keys = pygame.key.get_pressed()

        self.move_right = int(keys[pygame.K_RIGHT])
        self.move_left = int(keys[pygame.K_LEFT])
        self.facing = 'right' if self.move_right == 1 else 'left' if self.move_left == 1 else self.facing

        self.attack = keys[pygame.K_x]

        if keys[pygame.K_p]:
            self.reset_pos()

        self.is_pressed = (self.move_right or self.move_left)

        self.jump = keys[pygame.K_UP]

        # TODO: Finish fast-fall
        if self.jump == 1:
            self.jumptime += 1
        else:
            self.jumptime = 0

    def player_movement(self):
        if self.dash_ready:
            if self.is_pressed and not self.air:
                self.is_dash = True
                self.dash_ready = False
        else:
            self.timerDict['DashCD'] -= 1
            if self.timerDict['DashCD'] <= 0 and not self.is_pressed:
                self.dash_ready = True
                self.timerDict['DashCD'] = 30

        if self.is_dash:
            self.timerDict['DashLen'] -= 1
            if self.timerDict['DashLen'] <= -1:
                self.is_dash = False
                self.timerDict['DashLen'] = 15

        print('dash = ' + str(self.is_dash))
        print('press = ' + str(self.is_pressed))

        MOVESPEED = 0
        SPEED_CAP = 10

        if self.is_pressed:
            MOVESPEED = 2
            if self.is_dash:
                MOVESPEED = MOVESPEED * 2
                SPEED_CAP = int(SPEED_CAP * 1.5)
            if self.air:
                MOVESPEED = 1

        if self.air:
            SPEED_CAP = 50
            if self.timerDict['Phys'] in (1, 3):
                if self.facing == 'right':
                    self.dx += MOVESPEED
                else:
                    self.dx -= MOVESPEED

        else:
            if self.facing == 'right':
                self.dx += MOVESPEED
            else:
                self.dx -= MOVESPEED

        if self.dx >= SPEED_CAP + 1:
            self.dx = SPEED_CAP
        if self.dx <= SPEED_CAP - (SPEED_CAP * 2) - 1:
            self.dx = SPEED_CAP - (SPEED_CAP * 2)

        if self.jump and not self.air:
            self.gravity = 0
            self.dy -= 18

    # TODO: Finish implementing
    def player_attack(self):
        if self.attack == 1:
            if self.facing == 'right':
                self.atkrect = pygame.Rect(self.rect.right - 25, self.rect.top + 10, 50, 50)
            else:
                self.atkrect = pygame.Rect(self.rect.left - 25, self.rect.top + 10, 50, 50)
        else:
            self.atkrect = None
            print('attack')

    def apply_friction(self):
        if self.timerDict['Phys'] in (0, 2):
            self.friction = 1.5

            if self.dx > 0 and not self.air:
                self.dx = int(self.dx // self.friction)
                if self.dx < 0:
                    self.dx = 0

            if self.dx < 0 and not self.air:
                self.dx = int(self.dx // self.friction) + 1
                if self.dx > 0:
                    self.dx = 0

    def apply_gravity(self):
        if self.timerDict['Phys'] == 4:
            self.gravity += 1
            self.dy += self.gravity
            if self.dy >= 31:
                self.dy = 30
            self.timerDict['Phys'] = 0
        self.timerDict['Phys'] += 1

    def update(self):
        self.player_input()
        self.player_attack()
        self.player_movement()
        self.apply_gravity()
        self.apply_friction()

    def update_pos(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.dy == 0:
            self.air = False
        else:
            self.air = True
        print(self.dx)
        print(self.dy)
        print('air = ' + str(self.air))


