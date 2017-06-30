import pygame

from coords import *

class Player(pygame.sprite.Sprite):


    def __init__(self, pixels, size, ID):
        
        pygame.sprite.Sprite.__init__(self)

        self.ID = ID
        
        self.pixels = pixels
        self.size = size
        self.x = self.pixels[0]
        self.y = self.pixels[1]
        self.w = self.size
        self.h = self.size
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        self.move_x = 0 # Per frame arrow key movement (added in update)
        self.move_y = 0 

        self.up_pressed = False # Store pressed state to instantly slide off dropped bombs
        self.right_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.on_bomb = False # Store if on bomb to slide off manually afterwards

        self.lives = 0 # These are adopted from controller       
        self.num_bombs = 0
        self.regn_time = 0
        self.fire_len = 0
        self.speed = 0
        
        self.fast_time = None
        self.invi_time = None
        self.dead_time = None

        reg_img_str = 'char_images//char_'+str(self.ID)+'.png'
        dead_img_str = 'char_images//char_'+str(self.ID)+'_dead.png'
        invi_img_str = 'char_images//char_'+str(self.ID)+'_invi.png'
        envi_img_str = 'char_images//char_'+str(self.ID)+'_envi.png'
        self.reg_img = pygame.image.load(reg_img_str)
        self.dead_img = pygame.image.load(dead_img_str)
        self.invi_img = pygame.image.load(invi_img_str)
        self.envi_img = pygame.image.load(envi_img_str)
        self.image = self.reg_img
        
    def __repr__(self):

        return 'Player '+str(self.ID)
        

    def stick_player(self, degree): # Round player position (deg = 1 means nearest block, deg = 2 means nearest half-block, etc.

        x_coord, y_coord = pixels_coords((self.x, self.y))

        x_mini = x_coord * degree
        y_mini = y_coord * degree

        steps = 11

        for step in range(1, (steps * degree) + 1):

            if abs(step - x_mini) <= 0.5:

                self.x = coords_pixels(step / degree)

            if abs(step - y_mini) <= 0.5:

                self.y = coords_pixels(step / degree)

        self.rect = pygame.Rect(self.x, self.y, self.w, self. h)
    

    def dead_player(self):

        self.move_x = 0
        self.move_y = 0

        self.dead_time = pygame.time.get_ticks()
        self.lives -= 1

        self.image = self.dead_img
        

    def invi_player(self):

        self.dead_time = None
        self.invi_time = pygame.time.get_ticks()      
        self.image = self.invi_img

    def norm_player(self):

        self.invi_time = None
        self.image = self.reg_img

    def update(self):

        self.x += self.move_x
        self.y += self.move_y

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)


