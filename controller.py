import pygame
import random
import time

from start import *
from player import *
from block import *


################################################################################
#This part is menu
pygame.init()


# screen constants
display_width = 780
display_height = 780


# colors
black = (0, 0, 0)
white = (255, 255, 255)

Orange_Red = (255, 69, 0)
Tomato = (255, 96, 71)

Yellow_Green = (154, 205, 50)
Lime_Green = (50, 205, 50)


Orange = (255, 165, 0)
Dark_Orange = (255, 140, 0)

Slate_Gray = (119, 136, 153)
Dim_Gray = (105, 105, 105)

Medium_Purple = (147, 112, 219)
Violet = (238, 130, 238)

# prepare cursors
#the default cursor
DEFAULT_CURSOR = pygame.mouse.get_cursor()

#the hand cursor
HAND_CURSOR = (
"        XX      ",
"       X..X     ",
"       X..X     ",
"       X..X     ",
"    XXXX..XXX   ",
"    X..X..X.XX  ",
" XX X..X..X.X.X ",
"X..XX.........X ",
"X...X.........X ",
" X.....X.X.X..X ",
"  X....X.X.X..X ",
"  X....X.X.X.X  ",
"   X...X.X.X.X  ",
"    X.......X   ",
"     X....X.X   ",
"     XXXXX XX   ")
_HCURS, _HMASK = pygame.cursors.compile(HAND_CURSOR, ".", "X")
HAND_CURSOR = ((16, 16), (5, 1), _HCURS, _HMASK)

gameDisplay = pygame.display.set_mode((display_width, display_height)) #create screen
pygame.display.set_caption('Pygaming With Fire')#title
clock = pygame.time.Clock()

pause = False

# image constants
titleImg = pygame.image.load('title_images//title.png')
titleCharImg1 = pygame.image.load('title_images//char_title_1.png')
titleCharImg2 = pygame.image.load('title_images//char_title_2.png')
titleCharImg3 = pygame.image.load('title_images//char_title_3.png')
bgImg = pygame.image.load('title_images//Adventurer_Manager_Background_The_Pillaged_Town1.png')


#functions
def bg(n,m):
    gameDisplay.blit(bgImg, (n, m))

n = (display_width * 0.0001)
m = (display_width * 0.0001)
    
def title(x, y): #title image
    gameDisplay.blit(titleImg, (x, y))

x = (display_width * 0.3)
y = (display_width * 0.1)


def titleChar_1(z, q): #title image
    gameDisplay.blit(titleCharImg1, (z, q))
    
z = (display_width * 0.25) #z = x
q = (display_width * 0.1) #q = y

def titleChar_2(a, b): #title image
    gameDisplay.blit(titleCharImg2, (a, b))
    
a = (display_width * 0.35) #a = x
b = (display_width * 0.2) #b = y

def titleChar_3(k, l): #title image
    gameDisplay.blit(titleCharImg3, (k, l))
    
k = (display_width * 0.45) #k = x
l = (display_width * 0.3) #l = y

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()
text = "A game where you can kill whoever you want!"

def button(msg,x,y,w,h,ic,ac,action=None): #ic=insideColor

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y: #when cursor in the button
        #pygame.mouse.set_cursor(*HAND_CURSOR) #change cursor to hand
        pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
        if click[0] == 1 and action != None:
            if action() == "play":
                c.main_loop()
            elif action == "quit":
                pygame.quit()
                quit()

    else:
        #pygame.mouse.set_cursor(*DEFAULT_CURSOR)
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))        
    smallText = pygame.font.SysFont('Silom', 20) #botton font
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), y+(h/2))
    gameDisplay.blit(textSurf, textRect)


def quitgame():
    pygame.quit()
    quit()

def unpause():
    global pause
    pause = False

def paused():
    
    #gameDisplay.fill(black)
    largeText = pygame.font.SysFont('Silom', 50)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width * 0.5), (display_height * 0.45))
    gameDisplay.blit(TextSurf, TextRect)
    while pause:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        if 350+100 > mouse[0] > 350 and 600+50 > mouse[1] > 600: 
                pygame.mouse.set_cursor(*HAND_CURSOR) 
        elif 350+100 > mouse[0] > 350 and 700+50 > mouse[1] > 700: 
                pygame.mouse.set_cursor(*HAND_CURSOR) 
        else:
                pygame.mouse.set_cursor(*DEFAULT_CURSOR)
                
        button("Continue",350,600,100,50, Medium_Purple, Violet, unpause)
        button("Quit",350,700,100,50, Slate_Gray, Dim_Gray, quitgame)

        pygame.display.update()
        clock.tick(15)
        
#I made the gameover screen function, but I don't know how to call it.
def gameover():
    
    #gameover = True
    largeText = pygame.font.SysFont('Silom', 20)
    TextSurf, TextRect = text_objects("Game Over", largeText)
    TextRect.center = ((display_width * 0.5), (display_height * 0.45))
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT():
                pygame.quit()
                quit()
                
        if 350+100 > mouse[0] > 350 and 600+50 > mouse[1] > 600: 
                pygame.mouse.set_cursor(*HAND_CURSOR) 
        elif 350+100 > mouse[0] > 350 and 700+50 > mouse[1] > 700: 
                pygame.mouse.set_cursor(*HAND_CURSOR) 
        else:
                pygame.mouse.set_cursor(*DEFAULT_CURSOR)
                
        button("Play Again",350,600,100,50, Orange, Dark_Orange, c.main_loop)
        button("Quit",350,700,100,50, Slate_Gray, Dim_Gray, quitgame)
                       
        pygame.display.update()
        clock.tick(15)


def game_intro():


        intro = False

        while intro == False:
                mouse = pygame.mouse.get_pos()
                #click = pygame.mouse.get_pressed()
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                pygame.mouse.set_cursor(*HAND_CURSOR) 
                        else:
                                pygame.mouse.set_cursor(*DEFAULT_CURSOR)
                # change cursor to hand if it is on the button
                if 350+100 > mouse[0] > 350 and 400+50 > mouse[1] > 400: 
                        pygame.mouse.set_cursor(*HAND_CURSOR) 
                elif 350+100 > mouse[0] > 350 and 500+50 > mouse[1] > 500: 
                        pygame.mouse.set_cursor(*HAND_CURSOR) 
                elif 350+100 > mouse[0] > 350 and 600+50 > mouse[1] > 600: 
                        pygame.mouse.set_cursor(*HAND_CURSOR) 
                elif 350+100 > mouse[0] > 350 and 700+50 > mouse[1] > 700: 
                        pygame.mouse.set_cursor(*HAND_CURSOR) 
                else:
                        pygame.mouse.set_cursor(*DEFAULT_CURSOR)

                bg(n, m)
                title(x, y)
                titleChar_1(z, q)
                titleChar_2(a, b)
                titleChar_3(k, l)

                message = pygame.font.SysFont('Silom', 20)
                TextSurf, TextRect = text_objects(text, message)
                TextRect.center = ((display_width * 0.5), (display_height * 0.45))
                gameDisplay.blit(TextSurf, TextRect)


                button("2 Player",350,400,100,50, Orange_Red, Tomato, c.main_loop)
                button("3 Player",350,500,100,50, Lime_Green, Yellow_Green, c.main_loop)
                button("4 Player",350,600,100,50, Orange, Dark_Orange, c.main_loop)
                button("Quit",350,700,100,50, Slate_Gray, Dim_Gray, quitgame)

        

                pygame.display.update()
                clock.tick(15)
                
#################################################################################
'''
#This part is the Game Over screen
medText = pygame.font.SysFont('Silom', 50) #botton font
text_object("Enter your initials", medText)
'''
#################################################################################
class Controller:

    def __init__(self):
        
        # SETTINGS  
        self.WIDTH = 780
        self.HEIGHT = 780
        self.BLOCK = 60
        self.SPEED = 5
        self.NUM_BOMBS = 3
        self.FRAMERATE = 80
        self.ARENA_UPPER = 11
        self.ARENA_LOWER = 1
        self.WHITE = (255, 255, 255)
        self.TURN_ASSIST = .7
        self.STICK_DEG = 3
        self.TICK_TIME = 2500
        self.FIRE_TIME = 400
    
        # CONTROL DICTIONARY {pygame.event.type.key:(player ID, command)}
        self.CONTROLS = {pygame.K_w:(0, 'UP'), pygame.K_d:(0, 'RIGHT'), pygame.K_s:(0, 'DOWN'), pygame.K_a:(0, 'LEFT'), pygame.K_LSHIFT:(0, 'BOMB'),
                         pygame.K_i:(1, 'UP'), pygame.K_l:(1, 'RIGHT'), pygame.K_k:(1, 'DOWN'), pygame.K_j:(1, 'LEFT'), pygame.K_n: (1, 'BOMB'),
                         pygame.K_UP:(2, 'UP'), pygame.K_RIGHT:(2, 'RIGHT'), pygame.K_DOWN:(2, 'DOWN'), pygame.K_LEFT:(2, 'LEFT'), pygame.K_KP0: (2, 'BOMB'),
                         pygame.K_KP8:(3, 'UP'), pygame.K_KP6:(3, 'RIGHT'), pygame.K_KP5:(3, 'DOWN'), pygame.K_KP4:(3, 'LEFT'), pygame.K_KP_PLUS: (3, 'BOMB')}

        # INITIALIZE DISPLAY OBJECT
        pygame.display.init()
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Pygaming With Fire')
        
        # CLOCK
        self.clock = pygame.time.Clock()

        # CONVERT BLOCK IMAGES
        Block.ROCK_IMG.convert()
        Block.BARR_IMG.convert()
        Block.WALK_IMG.convert()
        Block.BOMB_1_IMG.convert()
        Block.BOMB_2_IMG.convert()
        Block.BOMB_3_IMG.convert()
        Block.FIRE_IMG.convert()

        # CREATE PLAYERS BLOCKS, BARRELS, BOMBS, ENDS AND FIRES GROUPS
        self.players = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.barrels = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.ends = pygame.sprite.Group()
        self.fires = pygame.sprite.Group()
        self.powers = pygame.sprite.Group()

        # INSTANTIATE BLOCKS        
        for x, y, form in gen_blocks():
            
            block = Block((x, y), self.BLOCK, form)
            
            self.blocks.add(block)

            if form == 'BARR':

                self.barrels.add(block)

            if form == 'BARR' or form == 'ROCK':

                self.ends.add(block)

        # INSTATNTIATE PLAYERS
        for x, y, ID in gen_players():

            player = Player((x, y), self.BLOCK, ID)

            player.speed = self.SPEED

            player.num_bombs = self.NUM_BOMBS
            
            self.players.add(player)

        self.player_list = self.players.sprites() # Save list of player objects, ousted players are removed from pygame group
        self.player_list.sort(key=lambda player: player.ID) # Sort list by player ID for indexing (controls dictionary matches key to an ID and a command)

        # CONVERT PLAYER IMAGES
        for player in self.players.sprites():

            player.image.convert()
            player.reg_img.convert()
            player.dead_img.convert()
            player.invi_img.convert()

#####################################################################################################################################

    def check_legal(self, future_x, future_y):

        # CHECK BARREL COLLISION (using pixels)
        future_rect = pygame.Rect(future_x, future_y, self.BLOCK, self.BLOCK)

        collision = False

        for barrel in self.barrels.sprites():

            if barrel.rect.colliderect(future_rect):

                collision = True

        # CHECK MOVING TO RAIL (using coords)
        future_x, future_y = pixels_coords((future_x, future_y))
        legal_x = (self.ARENA_LOWER <= future_x <= self.ARENA_UPPER)
        legal_y = (self.ARENA_LOWER <= future_y <= self.ARENA_UPPER)
        
        in_bounds = legal_x and legal_y

        on_vertical_rail = False
        on_horizont_rail = False
        
        for i in gen_rail():
            
            if (future_y == i):
                
                on_horizont_rail = True
                
            if (future_x == i):
                
                on_vertical_rail = True
                
        legal = (on_horizont_rail or on_vertical_rail) and in_bounds and (not collision)

        return legal

#####################################################################################################################################

    def drop_bomb(self, bomber):

        # CHECK IF ANOTHER PLAY IS BLOCKING BOMB SPACE
        future_x, future_y = stick_pixels((bomber.x, bomber.y))
        
        future_rect = pygame.Rect(future_x, future_y, self.BLOCK, self.BLOCK)

        if bomber.num_bombs:
            
            can_bomb = True # Initialized to true and set to false if colliding with another player

        else:

            can_bomb = False

        for player in self.players.sprites(): # Does not include removed players

            if player.rect.colliderect(future_rect) and (player.ID != bomber.ID):

                can_bomb = False

        for bomb in self.bombs.sprites():

            if bomb.rect.colliderect(future_rect):

                can_bomb = False

        if can_bomb:

            bomber.num_bombs -= 1

            bomber.stick_player(1) # Stick bomber to nearest legal block space
            
            bomb = pygame.sprite.spritecollide(bomber, self.blocks, False)[0] # Find block that player intersects (only one due to stick)

            bomb.update('BOMB')

            bomb.fire_len = bomber.fire_len # Pass bomber fire length to bomb for calculation

            self.barrels.add(bomb) # Bombs are counted as barrels (players can't move through them)

            self.bombs.add(bomb)

            bomber.on_bomb = True

#####################################################################################################################################
            
    def gen_fire(self, bomb):


        closest_up = bomb.fire_len
        closest_right = bomb.fire_len
        closest_down = bomb.fire_len
        closest_left = bomb.fire_len

        bomb_x_coord, bomb_y_coord = pixels_coords((bomb.x, bomb.y))
        bomb_x_coord = int(bomb_x_coord)
        bomb_y_coord = int(bomb_y_coord)

        for end in self.ends.sprites():

            y_diff = int(end.y_coord - bomb_y_coord)
            x_diff = int(end.x_coord - bomb_x_coord)

            up = -bomb.fire_len < y_diff < 0
            right = 0 < x_diff < bomb.fire_len
            down = 0 < y_diff < bomb.fire_len
            left = -bomb.fire_len < x_diff < 0

            same_x = end.x_coord == bomb_x_coord
            same_y = end.y_coord == bomb_y_coord

            if up and same_x:

                closest_up = min(closest_up, abs(y_diff))
 
            elif right and same_y:

                closest_right = min(closest_right, abs(x_diff))

            elif down and same_x:

                closest_down = min(closest_down, abs(y_diff))

            elif left and same_y:

                closest_left = min(closest_left, abs(x_diff))

        for y_adj in range(1, closest_up + 1):

            yield bomb_x_coord, bomb_y_coord - y_adj

        for x_adj in range(1, closest_right + 1):

            yield bomb_x_coord + x_adj, bomb_y_coord

        for y_adj in range(1, closest_down + 1):

            yield bomb_x_coord, bomb_y_coord + y_adj

        for x_adj in range(1, closest_left + 1):

            yield bomb_x_coord - x_adj, bomb_y_coord
       
#####################################################################################################################################
    
    def main_loop(self):
        #pasue
        global pause
        
        crash = False

        while crash == False:

            # PARSE THROUGH EVENTS
            for event in pygame.event.get():

                # HANDLE QUIT EVENT (EXIT LOOP)                
                if event.type == pygame.QUIT:
                    
                    crash = True

                # HANDLE KEY DOWN EVENT
                if event.type == pygame.KEYDOWN:
                    #pause function
                    if event.key == pygame.K_p:
                        pause = True
                        paused()

                    event_action = self.CONTROLS.get(event.key) # Grab (player, command) based on pygame.event.type.key

                    if event_action == None: # "If event not in control dictionary, continue to next event."

                        continue

                    else:
                    
                        player_ID = event_action[0]
                        command = event_action[1]

                    player = self.player_list[player_ID]


                    if player.dead_time:

                        continue
                    
                    # TURN ASSIST
                    near_vertical_rail = False
                    near_horizont_rail = False

                    x_coord, y_coord = pixels_coords((player.x, player.y))
                    
                    for rail in gen_rail():

                        if abs(rail - x_coord) < self.TURN_ASSIST:

                            near_vertical_rail = rail #True (rail coord used for pixel location)

                        if abs(rail - y_coord) < self.TURN_ASSIST:

                            near_horizont_rail = rail                           
                    

                    if command == 'UP' and near_vertical_rail: # "If command is up and near a vertical rail: queue movement, shift to get on rail, and shift off bombs (instant and manual)

                        # QUEUE MOVEMENT           
                        player.move_x = 0 # Cancel perpendicular movement (prevents stuttering around turns)

                        player.move_y = -player.speed

                        # TURN ASSIST SHIFT
                        rail_pixel = coords_pixels(near_vertical_rail) # Perpendicular pixel to slide to to make this command legal

                        player.x = rail_pixel 

                        # OFF BOMB SHIFT
                        player.up_pressed = True # Store pressed state to instantly shift off dropped bombs (if not set to unpressed with key-up)
    
                        if player.on_bomb: # "If on a bomb, manually shift off of it if the future rectangle is legal"
                        
                            future_y = player.y - self.BLOCK 

                            if self.check_legal(player.x, future_y) : 

                                player.y -= (self.BLOCK - player.speed)

                    elif command == 'RIGHT' and near_horizont_rail:
          
                        player.move_y = 0
                        
                        player.move_x = player.speed
                        
                        rail_pixel = coords_pixels(near_horizont_rail)
                        
                        player.y = rail_pixel
                        
                        player.right_pressed = True 
    
                        if player.on_bomb: 
                        
                            future_x = player.x + self.BLOCK 

                            if self.check_legal(future_x, player.y): 

                                player.x += (self.BLOCK - player.speed)

                    elif command == 'DOWN' and near_vertical_rail:
          
                        player.move_x = 0 

                        player.move_y = player.speed

                        rail_pixel = coords_pixels(near_vertical_rail)
                        
                        player.x = rail_pixel 

                        player.down_pressed = True 
    
                        if player.on_bomb: 
                        
                            future_y = player.y + self.BLOCK

                            if self.check_legal(player.x, future_y): 

                                player.y += (self.BLOCK - player.speed)

                    elif command == 'LEFT' and near_horizont_rail:
         
                        player.move_y = 0 

                        player.move_x = -player.speed
                        
                        rail_pixel = coords_pixels(near_horizont_rail) 

                        player.y = rail_pixel 

                        player.left_pressed = True 
    
                        if player.on_bomb: 
                        
                            future_x = player.x - self.BLOCK 

                            if self.check_legal(future_x, player.y): 

                                player.x -= (self.BLOCK - player.speed)
                            
                    elif command == 'BOMB':
                        
                        self.drop_bomb(player)

                        # SLIDE OFF BOMB IMMEDIATELY IF DIRECTIONAL KEY WAS PRESSED
                        up_future_y = player.y - self.BLOCK
                        right_future_x = player.x + self.BLOCK
                        down_future_y = player.y + self.BLOCK
                        left_future_x = player.x - self.BLOCK

                        if player.up_pressed and self.check_legal(player.x, up_future_y):

                            player.y -= (self.BLOCK - player.speed)
                            
                        elif player.right_pressed and self.check_legal(right_future_x, player.y):

                            player.x += (self.BLOCK - player.speed)

                        elif player.down_pressed and self.check_legal(player.x, down_future_y):
                       
                            player.y += (self.BLOCK - player.speed)

                        elif player.left_pressed and self.check_legal(left_future_x, player.y):

                            player.x -= (self.BLOCK - player.speed)
                            
                # HANDLE KEY UP EVENT
                if event.type == pygame.KEYUP:

                    event_action = self.CONTROLS.get(event.key)

                    if event_action == None:

                        continue

                    else:
                    
                        player_ID = event_action[0]
                        command = event_action[1]
                                                          
                    player = self.player_list[player_ID]

                    if player.dead_time:

                        continue

                    if command == 'UP':

                        player.up_pressed = False

                        player.stick_player(self.STICK_DEG)

                        if player.move_y < 0: # Only cancel previous movement in this direction (prevents stuttering in opposite directions)

                            player.move_y = 0

                    elif command == 'RIGHT':

                        player.right_pressed = False

                        player.stick_player(3)

                        if player.move_x > 0:

                            player.move_x = 0

                    elif command == 'DOWN':

                        player.down_pressed = False

                        player.stick_player(self.STICK_DEG)

                        if player.move_y > 0:

                            player.move_y = 0

                    elif command == 'LEFT':

                        player.stick_player(self.STICK_DEG)
                        
                        player.left_pressed = False

                        if player.move_x < 0:

                            player.move_x = 0

#####################################################################################################################################

            # UPDATE BOMB
            for bomb in self.bombs.sprites():
                
                current_time = pygame.time.get_ticks()

                if self.TICK_TIME - 1000 > current_time - bomb.drop_time > self.TICK_TIME - 2000:

                    bomb.image = Block.BOMB_2_IMG

                elif self.TICK_TIME > current_time - bomb.drop_time > self.TICK_TIME - 1000:

                    bomb.image = Block.BOMB_3_IMG
                
                elif current_time - bomb.drop_time > self.TICK_TIME:

                    bomb.update('FIRE')
                    
                    self.fires.add(bomb)
                    self.bombs.remove(bomb)
                    self.barrels.remove(bomb)
                    
                    for x_coord, y_coord in self.gen_fire(bomb): 

                        bomb.fires.add((x_coord, y_coord)) # Generate fire coords and add them to a set

                    for block in self.blocks.sprites():

                        if (block.x_coord, block.y_coord) in bomb.fires and block.form != 'ROCK': # Check if a block is in fire set and is not a block

                            if block.form == 'BOMB':

                                block.drop_time = bomb.drop_time

                            block.update('FIRE')
                            
                            self.fires.add(block)
                            self.ends.remove(block)
                            self.barrels.remove(block)

                    bomb.drop_time = None # Reset drop time       
                    bomb.fires = set() # Reset set of fire coords
                    bomb.fire_len = None # Reset fire length
                    # None of this would have to be done if bomb was a separate class :^)
                    
#####################################################################################################################################

            # UPDATE FIRES
            for fire in self.fires.sprites():

                current_time = pygame.time.get_ticks()

                if current_time - fire.fire_time > self.FIRE_TIME:

                    fire.update('WALK')

                    if fire.form[:3] == 'PWR':

                        self.powers.add(fire)

                    self.fires.remove(fire)

#####################################################################################################################################
                
            # UPDATE PLAYERS
            for player in self.player_list:

                current_time = pygame.time.get_ticks()
                
                future_x = player.x + player.move_x
                future_y = player.y + player.move_y

                if self.check_legal(future_x, future_y):

                    player.on_bomb = False # Reset on bomb, legal moves never land on a bomb
                
                    player.update()

                power_collision = pygame.sprite.spritecollide(player, self.powers, False)

                for power in power_collision: # Give player power up and manually change block to walk space (update handles 'WALK' for other block changes)

                    if power.form[4:] == 'BOMB':
                        
                        player.num_bombs += 1

                    elif power.form[4:] == 'FAST':

                        player.speed = min(self.SPEED + 5, player.speed + 2) # Allows stacking, with all stacks gone 15 seconds after the last

                        player.fast_time = pygame.time.get_ticks()

                    elif power.form[4:] == 'INVI':

                        player.invi_player()

                        player.invi_time += 8000 # Power invincibility lasts 6 seconds longer

                    elif power.form[4:] == 'LONG':

                        player.fire_len = min(5, player.fire_len + 1)

                    power.contents = None
                    power.form = 'WALK'
                    power.image = Block.WALK_IMG

                    self.powers.remove(power)

                dead_collision = pygame.sprite.spritecollide(player, self.fires, False)

                if player.invi_time:

                    if current_time - player.invi_time > 0:

                        player.image = player.envi_img

                    if current_time - player.invi_time > 2000:

                        player.norm_player()

                elif player.dead_time and player.lives:

                    if current_time - player.dead_time > 2000:

                        player.invi_player()

                elif dead_collision: # Only check for death collision if player not invincible or dead

                    player.dead_player()

                    player.speed = self.SPEED
                    player.num_bombs = self.NUM_BOMBS

                if player.fast_time:

                    if current_time - player.fast_time > 10000:

                        player.speed = self.SPEED

                        player.fast_time = None

                if player.lives <= 0:

                    self.players.remove(player)
                        
            
            # UPDATE DISPLAY           
            pygame.display.update()

            # FILL DISPLAY WHITE
            self.display.fill(self.WHITE)

            # DRAW BLOCKS
            self.blocks.draw(self.display)

            # DRAW PLAYERS
            self.players.draw(self.display)

            # FRAMERATE
            self.clock.tick(self.FRAMERATE)

        # QUIT
        pygame.display.quit()
        quit()
        
c = Controller()
game_intro()
c.main_loop()
