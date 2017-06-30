import pygame
import random

from coords import *

class Block(pygame.sprite.Sprite):
 
    WALK_IMG = pygame.image.load('block_images//walk.jpg')
    BARR_IMG = pygame.image.load('block_images//barr.jpg')
    ROCK_IMG = pygame.image.load('block_images//rock.jpg')
    BOMB_1_IMG = pygame.image.load('block_images//bomb_1.jpg')
    BOMB_2_IMG = pygame.image.load('block_images//bomb_2.jpg')
    BOMB_3_IMG = pygame.image.load('block_images//bomb_3.jpg')
    FIRE_IMG = pygame.image.load('block_images//fire.jpg')
    FIREBOMB_IMG = pygame.image.load('block_images//firebomb.jpg')
    PWR_BOMB_IMG = pygame.image.load('block_images//pwr_bomb.jpg')
    PWR_FAST_IMG = pygame.image.load('block_images//pwr_fast.jpg')
    PWR_INVI_IMG = pygame.image.load('block_images//pwr_invi.jpg')
    PWR_LONG_IMG = pygame.image.load('block_images//pwr_long.jpg')

    def __init__(self, pixels, size, form):

        pygame.sprite.Sprite.__init__(self)
        
        self.coords = pixels_coords(pixels)
        self.x_coord = self.coords[0]
        self.y_coord = self.coords[1]
        
        self.pixels = pixels
        self.size = size
        self.x = pixels[0]
        self.y = pixels[1]
        self.w = self.size
        self.h = self.size

        self.form = form
        
        self.contents = None

        self.fire_len = None
        self.fires = set() 
        self.drop_time = None
        self.fire_time = None
        
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        if self.form == 'ROCK':

            self.image = Block.ROCK_IMG

        elif self.form == 'BARR':

            self.image = Block.BARR_IMG

            content = random.randrange(0, 100)

            if content < 50:

                self.contents = 'PWR_BOMB'

            elif content < 58:

                self.contents = 'PWR_FAST'

            elif content < 66:

                self.contents = 'PWR_INVI'

            elif content < 74:

                self.contents = 'PWR_LONG'
 
        else:

            self.image = Block.WALK_IMG
            

    def __repr__(self):

        return str(self.form) + str(self.coords)
    

    def update(self, new_form):

        old_form = self.form

        self.form = new_form

        if self.form == 'BOMB':

            self.image = Block.BOMB_1_IMG

            self.drop_time = pygame.time.get_ticks() # Set a drop time to expire

        elif self.form == 'FIRE':

            if old_form[:3] == 'PWR': # Save power-up form to content to be exposed when turned to walk (like barrels) so power-ups are not deleted by fire

                self.contents = old_form 

            if old_form != 'BOMB': # If not a bomb, turn to fire image

                self.image = Block.FIRE_IMG

            else: # If a bomb, turn to firebomb image

                self.form = 'FIREBOMB' 
                
                self.image = Block.FIREBOMB_IMG

            self.fire_time = pygame.time.get_ticks() # Set a fire time to expire

        elif self.form == 'WALK' and not self.contents: # If being turned to walk and no contents, turn into walk image

            self.contents = None
            
            self.image = Block.WALK_IMG

        elif self.form == 'WALK' and self.contents: # If being turned to walk and contents, turn into power-up image
 
            self.form = self.contents

            if self.form[4:] == 'BOMB':

                self.image = Block.PWR_BOMB_IMG

            elif self.form[4:] == 'FAST':

                self.image = Block.PWR_FAST_IMG

            elif self.form[4:] == 'INVI':

                self.image = Block.PWR_INVI_IMG

            elif self.form[4:] == 'LONG':

                self.image = Block.PWR_LONG_IMG

            self.contents = None
