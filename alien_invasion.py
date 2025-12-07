import sys
import pygame
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button


def run_game():
    #initialize game and create screen object
    pygame.init()
    ai_settings = Settings()
    #Initializing the screen dimensions
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))

    background = pygame.image.load("./images/backgroundspace.png").convert()

    #Creating the caption that appears on the screen
    pygame.display.set_caption("Alien Invasion")
    #creating the play button
    play_button = Button(ai_settings, screen, "Play")
    #creating the stats
    stats = GameStats(ai_settings)
    #creating an instance of the ship. Takes in two parameters: The settings and the screen
    sb = Scoreboard(ai_settings, screen, stats)
    
    ship = Ship(ai_settings, screen)
    #make a group to store bullets in. Group is an instance of pygame.sprite.Group, which behaves like a list with some extra functionality
    bullets = Group()
    #create an emtpy group to hold all the aliens
    aliens = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    while True:
    #the game is controlled by a while loop that contains an event loop and code that manages screen updates
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        #need to pass the button here so it pops up when this function is called the first loop
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, background)
        bullets.update()
        #Get rid of bullets that have disappear
      
        
run_game()


'''
The main file of the program. It creates a number of important objects used throughout the game. The settings are stored in ai_settings, the main display surface is stored in screen, and a ship
instance is created in this file as well. Also stored in this file is the main loop of the game, which is a while loop that calls check_events, ship_update, and update_screen. This is the only file
you need to run for the game. All the other files are imported into this one
'''