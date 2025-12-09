import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_settings, screen):
        """Initialize the alien and set it's starting position"""
        #creating a temporary object of the superclass, allowing us to call its methods
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/officialalien.png').convert_alpha()
        self.rect = self.image.get_rect()

        #Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at it's current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien to the right"""
        #each time we call update, the alien moves to the right by its speed_factor which is stored in settings
        #multiply the x by fleet_direction to dictate whether it moves left or right
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        #we then use x value to update its rect position, which is the actual alien position being tracked
        self.rect.x = self.x
    
    def check_edges(self):
        """Return true if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        #An alieni is at the right edge if the right attribute of its 'rect' is greater than or equal to the right attribute of the screen's rect
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True