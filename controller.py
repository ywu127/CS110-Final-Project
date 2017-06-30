import pygame

from start import *
from player import *
from block import *

class Controller:

    def __init__(self):
        
        # SETTINGS
        self.NUM_PLAYERS = 0
        self.LIVES = 1
        self.NUM_BOMBS = 3
        self.FIRE_LEN = 3
        self.SPEED = 5
        
        self.WHITE = (255, 255, 255)        
        self.DISP_WIDTH = 780
        self.DISP_HEIGHT = 780
        self.ARENA_UPPER = 11
        self.ARENA_LOWER = 1
        self.BLOCK_SIZE = 60
        self.TICK_TIME = 2500
        self.FIRE_TIME = 400        
        self.STICK_DEG = 3
        self.TURN_ASSIST = .7
        self.FRAMERATE = 80
        self.WINNER = None
        
        # CONTROL DICTIONARY {pygame.event.type.key:(player ID, command)}
        self.CONTROLS = {pygame.K_w:(0, 'UP'), pygame.K_d:(0, 'RIGHT'), pygame.K_s:(0, 'DOWN'), pygame.K_a:(0, 'LEFT'), pygame.K_LSHIFT:(0, 'BOMB'),
                         pygame.K_i:(1, 'UP'), pygame.K_l:(1, 'RIGHT'), pygame.K_k:(1, 'DOWN'), pygame.K_j:(1, 'LEFT'), pygame.K_n: (1, 'BOMB'),
                         pygame.K_UP:(2, 'UP'), pygame.K_RIGHT:(2, 'RIGHT'), pygame.K_DOWN:(2, 'DOWN'), pygame.K_LEFT:(2, 'LEFT'), pygame.K_KP0: (2, 'BOMB'),
                         pygame.K_KP8:(3, 'UP'), pygame.K_KP6:(3, 'RIGHT'), pygame.K_KP5:(3, 'DOWN'), pygame.K_KP4:(3, 'LEFT'), pygame.K_KP_PLUS: (3, 'BOMB')}

        # INITIALIZE DISPLAY OBJECT
        pygame.init()
        self.display = pygame.display.set_mode((self.DISP_WIDTH, self.DISP_HEIGHT))
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


    def populate_arena(self):

        # DELETE CONTROLS IF FEWER PLAYERS
        del_controls = [key for key in self.CONTROLS if self.CONTROLS[key][0] > self.NUM_PLAYERS - 1]
        
        for control in del_controls:
            
            self.CONTROLS.pop(control)

        # INSTANTIATE BLOCKS        
        for x, y, form in gen_blocks():
            
            block = Block((x, y), self.BLOCK_SIZE, form)
            
            self.blocks.add(block)

            if form == 'BARR':

                self.barrels.add(block)

            if form == 'BARR' or form == 'ROCK':

                self.ends.add(block)

        # INSTATNTIATE PLAYERS
        for x, y, ID in gen_players(self.NUM_PLAYERS):

            player = Player((x, y), self.BLOCK_SIZE, ID)
            
            player.lives = self.LIVES
            player.num_bombs = self.NUM_BOMBS
            player.regn_time = pygame.time.get_ticks()
            player.fire_len = self.FIRE_LEN
            player.speed = self.SPEED
            
            self.players.add(player)

        self.player_list = self.players.sprites() # Save list of player objects, ousted players are removed from pygame group
        self.player_list.sort(key=lambda player: player.ID) # Sort list by player ID for indexing (controls dictionary matches key to an ID and a command)

        # CONVERT PLAYER IMAGES
        for player in self.players.sprites():

            player.image.convert()
            player.reg_img.convert()
            player.dead_img.convert()
            player.invi_img.convert()

            
    def check_legal(self, future_x, future_y):

        # CHECK BARREL COLLISION (using pixels)
        future_rect = pygame.Rect(future_x, future_y, self.BLOCK_SIZE, self.BLOCK_SIZE)

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


    def drop_bomb(self, bomber):

        # CHECK IF ANOTHER PLAY IS BLOCKING BOMB SPACE
        future_x, future_y = stick_pixels((bomber.x, bomber.y))
        
        future_rect = pygame.Rect(future_x, future_y, self.BLOCK_SIZE, self.BLOCK_SIZE)

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
       
    
    def main_loop(self):

        crash = False

        while crash == False:

            # PARSE THROUGH EVENTS
            for event in pygame.event.get():

                # HANDLE QUIT EVENT (EXIT LOOP)                
                if event.type == pygame.QUIT:
                    
                    crash = True

                # HANDLE KEY DOWN EVENT
                if event.type == pygame.KEYDOWN:

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
                        
                            future_y = player.y - self.BLOCK_SIZE

                            if self.check_legal(player.x, future_y) : 

                                player.y -= (self.BLOCK_SIZE - player.speed)

                    elif command == 'RIGHT' and near_horizont_rail:
          
                        player.move_y = 0
                        
                        player.move_x = player.speed
                        
                        rail_pixel = coords_pixels(near_horizont_rail)
                        
                        player.y = rail_pixel
                        
                        player.right_pressed = True 
    
                        if player.on_bomb: 
                        
                            future_x = player.x + self.BLOCK_SIZE

                            if self.check_legal(future_x, player.y): 

                                player.x += (self.BLOCK_SIZE - player.speed)

                    elif command == 'DOWN' and near_vertical_rail:
          
                        player.move_x = 0 

                        player.move_y = player.speed

                        rail_pixel = coords_pixels(near_vertical_rail)
                        
                        player.x = rail_pixel 

                        player.down_pressed = True 
    
                        if player.on_bomb: 
                        
                            future_y = player.y + self.BLOCK_SIZE

                            if self.check_legal(player.x, future_y): 

                                player.y += (self.BLOCK_SIZE - player.speed)

                    elif command == 'LEFT' and near_horizont_rail:
         
                        player.move_y = 0 

                        player.move_x = -player.speed
                        
                        rail_pixel = coords_pixels(near_horizont_rail) 

                        player.y = rail_pixel 

                        player.left_pressed = True 
    
                        if player.on_bomb: 
                        
                            future_x = player.x - self.BLOCK_SIZE 

                            if self.check_legal(future_x, player.y): 

                                player.x -= (self.BLOCK_SIZE - player.speed)
                            
                    elif command == 'BOMB':
                        
                        self.drop_bomb(player)

                        # SLIDE OFF BOMB IMMEDIATELY IF DIRECTIONAL KEY WAS PRESSED
                        up_future_y = player.y - self.BLOCK_SIZE
                        right_future_x = player.x + self.BLOCK_SIZE
                        down_future_y = player.y + self.BLOCK_SIZE
                        left_future_x = player.x - self.BLOCK_SIZE

                        if player.up_pressed and self.check_legal(player.x, up_future_y):

                            player.y -= (self.BLOCK_SIZE - player.speed)
                            
                        elif player.right_pressed and self.check_legal(right_future_x, player.y):

                            player.x += (self.BLOCK_SIZE - player.speed)

                        elif player.down_pressed and self.check_legal(player.x, down_future_y):
                       
                            player.y += (self.BLOCK_SIZE - player.speed)

                        elif player.left_pressed and self.check_legal(left_future_x, player.y):

                            player.x -= (self.BLOCK_SIZE - player.speed)
                            
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

            # UPDATE FIRES
            for fire in self.fires.sprites():

                current_time = pygame.time.get_ticks()

                if current_time - fire.fire_time > self.FIRE_TIME:

                    fire.update('WALK')

                    if fire.form[:3] == 'PWR':

                        self.powers.add(fire)

                    self.fires.remove(fire)
                
            # UPDATE PLAYERS
            for player in self.player_list:

                current_time = pygame.time.get_ticks()
                future_x = player.x + player.move_x
                future_y = player.y + player.move_y

                # BOMB REGENERATION
                if player.num_bombs < 3 and current_time - player.regn_time > 6000: # Regenerate bombs every 6 seconds if less than 3 bombs

                    player.num_bombs += 1

                    player.regn_time = pygame.time.get_ticks()

                # UPDATE LEGAL MOVES
                if self.check_legal(future_x, future_y):

                    player.on_bomb = False # Reset on bomb, legal moves never land on a bomb
                
                    player.update()

                # PICK UP POWER UPS
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

                        player.fire_len = min(6, player.fire_len + 1)

                    power.contents = None
                    power.form = 'WALK'
                    power.image = Block.WALK_IMG

                    self.powers.remove(power)

                # DEATH AND TIME UPDATES
                dead_collision = pygame.sprite.spritecollide(player, self.fires, False)

                if player.invi_time: # Check invincibility expiration

                    if current_time - player.invi_time > 0:

                        player.image = player.envi_img

                    if current_time - player.invi_time > 2000:

                        player.norm_player()

                elif player.dead_time and player.lives: # Check respawn if 

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

            if len(self.players.sprites()) == 1:

                self.WINNER = self.players.sprites()[0]

                crash = True
                        
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

    def end_screen(self):

        if not self.WINNER:

            pygame.display.quit()

            quit()

        win_img_str = 'end_screen//end_screen_'+str(self.WINNER.ID+1)+'.png'
        self.end_screen = pygame.image.load(win_img_str)
        self.end_screen.convert()
        
        crash = False

        end_time = pygame.time.get_ticks()
	
        while crash == False:

            current_time = pygame.time.get_ticks()

            # PARSE THROUGH EVENTS
            for event in pygame.event.get():

                # HANDLE QUIT EVENT (EXIT LOOP)                
                if event.type == pygame.QUIT:
                    
                    crash = True

            if current_time - end_time > 5000:

                crash = True
         
            pygame.display.update()

            # FILL DISPLAY WHITE
            self.display.fill(self.WHITE)

            # DRAW BLOCKS
            self.blocks.draw(self.display)

            # DRAW PLAYERS
            self.players.draw(self.display)

            self.display.blit(self.end_screen, (0, 0))

            self.clock.tick(self.FRAMERATE)

        pygame.display.quit()

    def start_screen(self):

        num1_img_str = 'start_screen//2_players.png'
        num2_img_str = 'start_screen//3_players.png'
        num3_img_str = 'start_screen//4_players.png'
        quit_img_str = 'start_screen//quit.png'
        bkgd_img_str = 'start_screen//start_bg.jpg'
        self.num1 = pygame.image.load(num1_img_str)
        num1_rect = pygame.Rect(327, 230, 125, 50)
        self.num2 = pygame.image.load(num2_img_str)
        num2_rect = pygame.Rect(327, 290, 125, 50)
        self.num3 = pygame.image.load(num3_img_str)
        num3_rect = pygame.Rect(327, 350, 125, 50)
        self.quit = pygame.image.load(quit_img_str)
        quit_rect = pygame.Rect(327, 410, 125, 50)
        self.bkgd = pygame.image.load(bkgd_img_str)
        bkgd_rect = pygame.Rect(0, 0, 125, 50)
        
        crash = False

        while crash == False:

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    mouse_pos = pygame.mouse.get_pos()

                    if num1_rect.collidepoint(mouse_pos):

                        self.NUM_PLAYERS = 2

                        crash = True

                    if num2_rect.collidepoint(mouse_pos):

                        self.NUM_PLAYERS = 3
                        
                        crash = True

                    if num3_rect.collidepoint(mouse_pos):

                        self.NUM_PLAYERS = 4
                        
                        crash = True

                    if quit_rect.collidepoint(mouse_pos):

                        pygame.display.quit()

                        quit()
                        
                        crash = True

            pygame.display.update()

            self.display.blit(self.bkgd, (bkgd_rect.x, bkgd_rect.y))
            
            self.display.blit(self.num1, (num1_rect.x, num1_rect.y))
            self.display.blit(self.num2, (num2_rect.x, num2_rect.y))
            self.display.blit(self.num3, (num3_rect.x, num3_rect.y))
            self.display.blit(self.quit, (quit_rect.x, quit_rect.y))

            self.clock.tick(self.FRAMERATE)

            
c = Controller()
c.start_screen()
c.populate_arena()
c.main_loop()
c.end_screen()
