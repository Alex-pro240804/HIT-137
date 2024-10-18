import pygame
from pygame import mixer
import os
import random
import csv
import buttons

mixer.init()
pygame.init()

# Set up screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# Create the display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('hit137.ass3')

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
TILE_SIZE = 40
ROWS = 13
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21


bg_scroll = 0
screen_scroll = 0
level = 0
start_game = False
moving_left = False
moving_right = False
shoot = False
grenade_thrown = False
level_complete = 0

#music
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('jump.wav')
jump_fx.set_volume(0.5)
shot_fx = pygame.mixer.Sound('gun.ogg')
shot_fx.set_volume(0.5)
grenade_fx = pygame.mixer.Sound('grenade.ogg')
grenade_fx.set_volume(0.5)


# Load images
#button images
start_img = pygame.image.load('png files/start_btn.png').convert_alpha()
exit_img = pygame.image.load('png files/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('png files/restart_btn.png').convert_alpha()

sky_img = pygame.image.load('png files/layers/sky.png').convert_alpha()
# Adjust the background size to match the screen width and a smaller height to "zoom out" the background
background_width = SCREEN_WIDTH  # Keep the width same as the screen width
background_height = SCREEN_HEIGHT  # Scale the height to zoom out

# Scale the background image
sky_img = pygame.transform.scale(sky_img, (background_width, background_height))



#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'png files/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

bullet_img = pygame.image.load('png files/icons/bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (int(bullet_img.get_width() * 0.5), int(bullet_img.get_height() * 0.5)))

grenade_img = pygame.image.load('png files/icons/grenade.png').convert_alpha()
grenade_img = pygame.transform.scale(grenade_img, (int(grenade_img.get_width() * 0.5), int(grenade_img.get_height() * 0.5)))

health_box_img = pygame.image.load('png files/icons/health_box.png').convert_alpha()
health_box_img = pygame.transform.scale(health_box_img, (int(health_box_img.get_width() * 0.5), int(health_box_img.get_height() * 0.5)))

ammo_box_img = pygame.image.load('png files/icons/ammo_box.png').convert_alpha()
ammo_box_img = pygame.transform.scale(ammo_box_img, (int(ammo_box_img.get_width() * 0.5), int(ammo_box_img.get_height() * 0.5)))

grenade_box_img = pygame.image.load('png files/icons/grenade_box.png').convert_alpha()
grenade_box_img = pygame.transform.scale(grenade_box_img, (int(grenade_box_img.get_width() * 0.5), int(grenade_box_img.get_height() * 0.5)))

item_boxes = {
    'Health': health_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img
}

# Define colors
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Define font
font = pygame.font.SysFont('Futura', 15)

# Function to draw text on the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function to draw the background
def draw_bg(bg_scroll):
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(4):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))  # Ground line
    screen.blit(sky_img, (0, 0))

#function to reset level
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    #create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data        
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.grenades = grenades
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.moving_left = False
        self.moving_right = False
        self.shoot = False
        self.grenade_thrown = False
        self.min_scroll = 0

        # Load all images for the player's animations
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            temp_list = []
            animation_folder = os.path.join('png files', self.char_type, animation)
            num_of_frames = len(os.listdir(animation_folder))
            for i in range(num_of_frames):
                img_path = os.path.join(animation_folder, f'{i}.png')
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def throw_grenade(self):
        if self.grenades > 0:
            grenade = Grenade(self.rect.centerx, self.rect.centery, self.direction)
            grenade_group.add(grenade)
            self.grenades -= 1

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        screen_scroll = 0
        dx = 0
        dy = 0
        if moving_left and self.rect.left > 0:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        #check for collisions
        for tile in world.obstacle_list:
            #check collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #if ai has hit the wall then make it turn around
                if self.char_type == 'enemy':
                    self.direction += -1
                    self.move_counter = 0
            #check collison in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy,self.width, self.height):
                 #check if below the ground, i.e jumping
                 if self.vel_y < 0:
                     self.vel_y = 0
                     dy = tile[1].bottom - self.rect.top
                  #check if above the ground, i.e. falling
                 elif self.vel_y >= 0:
                     self.vel_y = 0
                     self.in_air = False
                     dy = tile[1].top - self.rect.bottom   
        #check for collison with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0 

        #check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0


        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player position
        if self.char_type =='player':
            if self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and moving_right:
                screen_scroll = -dx
                self.rect.x -= dx
            if self.rect.left < SCROLL_THRESH and moving_left and bg_scroll > 0:
                screen_scroll -= dx

        # Backward scrolling: Only allow if the player has moved far enough right
            if self.rect.left < SCROLL_THRESH and moving_left:
                # Prevent scrolling back if we are still at the minimum scroll position
                if bg_scroll > self.min_scroll:
                    screen_scroll = -dx  # Scroll left
                    self.rect.x -= dx  # Keep player in place relative to the screen
        
                
                 
        return screen_scroll        

    def fire_bullet(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet_owner = 'player' if self.char_type == 'player' else 'enemy'
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, bullet_owner)
            bullet_group.add(bullet)
            self.ammo -= 1
            
            shot_fx.play()

    def ai(self):
        if self.alive and player.alive:
            # Check if the player is within shooting range
            distance_to_player = abs(player.rect.centerx - self.rect.centerx)
            if distance_to_player < TILE_SIZE * 5 and self.ammo > 0:
                # Face the player
                if player.rect.centerx < self.rect.centerx:
                    self.direction = -1
                    self.flip = True
                else:
                    self.direction = 1
                    self.flip = False

                # Fire a bullet if cooldown allows
                if self.shoot_cooldown == 0:
                    self.fire_bullet()

            # Check if the enemy should idle or move
            if self.idling:
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False
            else:
                if random.randint(1, 200) == 1:
                    self.idling = True
                    self.idling_counter = 50
                else:
                    ai_moving_right = self.direction == 1
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    if self.move_counter > TILE_SIZE or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                        self.direction *= -1
                        self.move_counter = 0
        #scroll
        self.rect.x += screen_scroll                   

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
            if self.frame_index >= len(self.animation_list[self.action]) - 1:
                self.kill()

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        player = None
        health_bar = None

        # Iterate through each value in the level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decorations(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                        self.obstacle_list.append((img, decoration.rect))
                    elif tile == 15:  # create player
                        player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, scale=1.65, speed=5, ammo=20, grenades=5)
                        health_bar = HealthBar(10, 10, player.health, player.health)

                    elif tile == 16:  # create enemies
                        enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, scale=1.65, speed=2, ammo=20, grenades=0)
                        enemy_group.add(enemy)
                    elif tile == 17:  # create ammo box
                        item_box = Itembox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18:  # create grenade box
                        item_box = Itembox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:  # create health box
                        item_box = Itembox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:  # create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
        print(f"Player created: {player is not None}")
        # Return player and health bar for use in the game
        return player, health_bar

    def draw(self, screen_scroll):
        # Loop through all the obstacles and draw them with the screen scroll offset
        for tile in self.obstacle_list:
            tile[1].x += screen_scroll  # Adjust tile position based on scroll
            screen.blit(tile[0], tile[1])


    


class Decorations(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()  
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))                            
    def update(self, screen_scroll):
        pass
               
            
class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()  
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))                            
           
    def update(self, screen_scroll):
        self.rect.x += screen_scroll         

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()  
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))                            
           
    def update(self):
        self.rect.x += screen_scroll             

class Itembox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        #scroll
        self.rect.x += screen_scroll 
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 15
            elif self.item_type == 'Grenade':
                player.grenades += 3
            self.kill()

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, owner):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.owner = owner

    def update(self):
        self.rect.x += (self.direction * self.speed)
        # Remove the bullet if it goes off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        #check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
             self.kill()


            # Handle bullet collisions with enemies
        if self.owner == 'player':
            for enemy in enemy_group:
                if enemy.rect.colliderect(self.rect) and enemy.alive:
                    enemy.health -= 30  # Subtract health from enemy
                    print(f"Enemy hit! Remaining health: {enemy.health}")
                    self.kill()  # Bullet should disappear on impact
                    break

        # Handle bullet collisions with the player
        elif self.owner == 'enemy':
            if player.rect.colliderect(self.rect) and player.alive:
                player.health -= 30  # Subtract health from player
                print(f"Player hit! Remaining health: {player.health}")
                self.kill()  # Bullet should disappear on impact
                if player.health <= 0:
                    player.alive = False  # Mark player as dead


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.direction = direction
        

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        #check for collision with level
        for tile in world.obstacle_list:
            #check collisions with walls
            if tile[1].colliderect(self.rect.x +dx, self.rect.y, self.width, self.height):
             self.direction *= -1
             dx = self.direction * self.speed
         #check collison in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy,self.width, self.height):
                 self.speed = 0
                 #check if below the ground, i.e thrown up
                 if self.vel_y < 0:
                     self.vel_y = 0
                     dy = tile[1].bottom - self.rect.top
                  #check if above the ground, i.e. thrown down
                 elif self.vel_y >= 0:
                     self.vel_y = 0
                     dy = tile[1].top - self.rect.bottom 
                       
     

        
        self.rect.x += dx
        self.rect.y += dy
        self.timer -= 1
        self.rect.x += screen_scroll
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 0.5)
            explosion_group.add(explosion)
            if player.alive and abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemy_group:
                if enemy.alive and abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'png files/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        EXPLOSION_SPEED = 4
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]
#creat buttons
start_button = buttons.Button(SCREEN_WIDTH // 2-130, SCREEN_HEIGHT // 2 -150, start_img,1)
exit_button = buttons.Button(SCREEN_WIDTH // 2-110, SCREEN_HEIGHT // 2 + 150, exit_img,1)
restart_button = buttons.Button(SCREEN_WIDTH // 2-100, SCREEN_HEIGHT // 2 - 150, restart_img,2)
# Create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()







#create emoty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
player, health_bar = world. process_data(world_data)             


# Game loop
run = True
while run:
    clock.tick(FPS)

    if start_game == False:
        #draw menu
        screen.fill(BG)
       #add buttons
        if start_button.draw(screen):
           start_game = True
           
        if exit_button.draw(screen):
            run = False
    else:
        
            # Update background scroll based on player movement
            bg_scroll += screen_scroll

            # Draw background with scrolling
            draw_bg(bg_scroll)

            # Draw world map with scrolling
            world.draw(screen_scroll)

            # Show health bar, ammo, and grenades
            health_bar.draw(player.health)
            draw_text('AMMO: ', font, RED, 10, 35)
            for x in range(player.ammo):
              screen.blit(bullet_img, (62 + (x * 10), 38))
            draw_text('GRENADES: ', font, RED, 10, 60)
            for x in range(player.grenades):
                 screen.blit(grenade_img, (95 + (x * 10), 68))

            

            # Update player and handle movement/scroll
            screen_scroll = player.move(moving_left, moving_right)
            bg_scroll += screen_scroll

            # Update player animation and state
            player.update()


            # AI and draw for each enemy
            for enemy in enemy_group:
                enemy.ai()
                enemy.update() 
                enemy.draw(screen)

            # Update decorations (and other objects)
            for decoration in decoration_group:
                decoration.update(screen_scroll)
            decoration_group.draw(screen)

            # Update water group objects
            for water in water_group:
                water.update(screen_scroll)  # Update water elements with screen_scroll
            water_group.draw(screen) 

            
            # Detect Collision with Exit
            if pygame.sprite.spritecollide(player, exit_group, False):
                level_complete = True

            # Handle level progression if the player has completed the level
            if level_complete:
                # Increment the level and load the new one
                level += 1
                if level > 2:  # Assuming there are 3 levels (0, 1, 2)
                    level = 0  # Reset to the first level or end the game
                bg_scroll = 0
                screen_scroll = 0
                world_data = reset_level()

                # Load the new level
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)

                # Reinitialize the world and player with the new level data
                world = World()
                player, health_bar = world.process_data(world_data)

                # Reset the level_complete flag
                level_complete = False   

            # Handle user inputs
            keys = pygame.key.get_pressed()
            moving_left = keys[pygame.K_a]
            moving_right = keys[pygame.K_d]
            shoot = keys[pygame.K_SPACE]

            if shoot and player.alive and player.shoot_cooldown == 0:
                player.fire_bullet()

            player.draw(screen)


            # Update other game elements
            bullet_group.update()
            grenade_group.update()
            explosion_group.update()
            item_box_group.update()
            exit_group.update()

            bullet_group.draw(screen)
            grenade_group.draw(screen)
            explosion_group.draw(screen)
            item_box_group.draw(screen)
            decoration_group.draw(screen)
            water_group.draw(screen)
            exit_group.draw(screen)

            # Player actions and animations
            if player.alive:
                if player.in_air:
                    player.update_action(2)
                elif moving_left or moving_right:
                    player.update_action(1)
                else:
                    player.update_action(0)
                    
            else:
                screen_scroll = 0
                if restart_button.draw(screen):
                    bg_scroll = 0
                    screen_scroll = 0
                    world_data = reset_level()
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world. process_data(world_data) 

                    player.alive = True
                                    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and not player.in_air:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_k and not grenade_thrown and player.grenades > 0:
                player.throw_grenade()
                grenade_thrown = True
            if event.key == pygame.K_ESCAPE:
                run = False

    if not pygame.key.get_pressed()[pygame.K_k]:
        grenade_thrown = False

    pygame.display.update()

pygame.quit()
