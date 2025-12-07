import pygame

#two-dimensional image that can be moved around on the screen
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the ship's current position"""
        super(Bullet, self).__init__()
        self.screen = screen

        #Create a bullet rect at (0,0) and then set current position. This line creates a rect object that is like a line, with width and height given
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        #The bullets center is the same as the ship
        self.rect.centerx = ship.rect.centerx
        #The bullet emegers from the top of the ship. So it begins at the same height of the ship
        self.rect.top = ship.rect.top

        #Store the bullet's position as a decimal value. It only moves in the y direction so no x is needed
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color

        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen"""
            #Update the decimal position of the bullet
            #When the bullet travels up, it is actually decreasing in y value, so this is why we include -=
        self.y -= self.speed_factor
            #Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
            #This function fills the part of the screen defined by the bullets rect with the color stored in self.color
        pygame.draw.rect(self.screen, self.color, self.rect)