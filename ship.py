import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship and it's starting position"""
        #ship inherits from sprite
        super(Ship, self).__init__()
        #The screen and instance of setting class is passed in
        self.screen = screen
        self.ai_settings = ai_settings

        #Image of the ship
        self.image = pygame.image.load('images/spaceship.png').convert_alpha()

        #creating a rectangular object from 'self.image' which is the image of our ship
        self.rect = self.image.get_rect()
        
        #Dimensions of the screen. Used for positioning elements relative to screen size
        self.screen_rect = screen.get_rect()

        #Centering the game object horizontally on the screen. 
        self.rect.centerx = self.screen_rect.centerx

        #Positioning our object at the botton of the screen
        self.rect.bottom = self.screen_rect.bottom
        
        #Storing a decimal value for the ships center. We take the original center and convert it to a float using the float function
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Update the ship's position based on the movement flag"""
        #Only move the ship if its in range
        if self.moving_right and self.rect.right < self.screen_rect.right: #edge of screen
            #center is adjusted by the rate of the speed of the ship which is stored in settings
            self.center += self.ai_settings.ship_speed_factor
        #Important to use 'if' for left because if it were 'elif', if the player were to hold both left and right keys at same time, ship would go right rather than stay still
        if self.moving_left and self.rect.left > 0: #or self.screen_rect.left
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Center ship to screen"""
        #to center the ship, we set the value of the ship's center attribute to match the center of the screen, which we get through the screen_rect attribute
        self.center = self.screen_rect.centerx
#in pygame (0,0) is the top left corner of the screen, and coordinates increase as you go down and to the right

'''
The ship file contains the ship class and an update method to change the ships position and blitme to draw the ship to the screen
'''