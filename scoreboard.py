#alllows us to write text to the screen
import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """A class to report scoring information"""

    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        
        #Font settings for scoring information
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    
    def prep_score(self):
        """Turn the score into a rendered image"""
        #rounding the value of rounded_score to the nearest 10 and store it in rounded_score
        rounded_score = int(round(self.stats.score, -1))
        #inserting commas into numbers when converting a numerical value to a string
        #doing this to get commas is large score values
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        #Diplay the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def show_score(self):
        """Draw score to screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #using draw to display the ships on the screen
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """Turn the high score into a rendered image"""
        #round high score to nearest 10
        high_score = int(round(self.stats.high_score, -1))
        #convert to a string
        high_score_str = "{:,}".format(high_score)
        #generating an image from the high score
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        #Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        #centering the score horozontally
        self.high_score_rect.centerx = self.screen_rect.centerx
        #top attribute matches the score top attribute, so it will be center and top of the screen
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image"""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color)
        
        """Position the level below the score"""
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        #loop runs once for every ship the player has left
        for ship_number in range(self.stats.ships_left):
            #creating a new ship and putting it at the correct position on the screen
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
