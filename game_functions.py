import sys
import pygame
import json
from alien import Alien
from bullet import Bullet
from time import sleep #pauses the game


def check_keydown_events(event, ai_settings, screen, ship, bullets, sb):
    """Respond to key-presses and mouse events"""
    if event.key == pygame.K_RIGHT:
        #if the passed in event is a right key
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        #if the passed in event is a left key
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #when the player presses space bar, we create a new instance of a bullet and add it to the group of bullets
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        filename = 'highscore.json'
        with open(filename, 'w') as f_object:
            json.dump(sb.stats.high_score, f_object)
        sys.exit()

def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Respond to key-presses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            filename = 'highscore.json'
            with open(filename, 'a') as f_object:
                json.dump(sb.stats.high_score, f_object)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            #if there's a keydown event
            check_keydown_events(event, ai_settings, screen, ship, bullets, sb)
        elif event.type == pygame.KEYUP:
            #if there's a keyup event
            check_keyup_events(event, ship)
            #whenever player clicks on the screen
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """starts a new game when the player clicks play"""
    #if the collide point of where we clicked is within the play buttons rect attribute
    #holds a true of false values 
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #Reset the game settings
        ai_settings.initialize_dynamic_settings()
        #make the cursor not visible once the game begins
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        #Reset the scoreboard images 
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #Emtpy the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


 
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, background):
    """Update images on the screen and flip to the new screen"""
    #Redraw the screen during each pass through the loop
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    #tbe bullets.sprites() method returns a list of all sprites in the group 'bullets'
    for bullet in bullets.sprites():
        #draw_bullets() is a method that draws the bullets to the screen
        bullet.draw_bullet()

    ship.blitme()
    #the 'draw' method is utilized on groups. Pygame automatically draws each element in the group at the position defined by its 'rect' attribute
    aliens.draw(screen)
    
    #Draw the play button if the game is inactive
    sb.show_score()
    
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets"""
    #Update bullet positions
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #Check for any bullets that have hit aliens
    #If so, get rid of the bullret and the alien
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
    #Checking whether the group of aliens is empty

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            #all aliens hit are stored in a dictionary
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        #Destroy existing bullets, speed up the game, create a new fleet
        #Calling create fleet to create a new fleet. This fills the screen the aliens again
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullut if limit not reached yet"""
    #Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    #Create an alien and find the number of aliens in a row
    #Spacing between each alien is equal to the one alien width
    alien = Alien(ai_settings, screen)
    #Getting the width of the alien rect attribute
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #Create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number , row_number)

def update_aliens(aliens):
    """Update the positions of all aliens in the fleet"""
    aliens.update()

def check_fleet_edges(ai_settings, aliens):
    """Respond apporpriately if any aliens have reached an edge"""
    #loop through the fleet and call 'check_edges' on each alien
    for alien in aliens.sprites():
        #if returned true, then an alien is on the edge, so we turn it around
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        #drop all the aliens using 'fleet_drop_speed' and then we change the direction by multiplying the 'fleet_direction' by -1
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if the fleet is at an edge, and then update the positions of all the aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #Look for alien-ship collisions
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
    if pygame.sprite.spritecollideany(ship, aliens):
        #this method 'spritecollideany' takes two arguments. A sprite and a group. THe method looks if any has come in contact with one another
        ship_hit(ai_settings, screen, stats, sb, ship,  aliens, bullets)
    #look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien"""
    #Decrament ships_left
    if stats.ships_left > 0:
        stats.ships_left -= 1

        sb.prep_ships()
        #Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #Pause 
        sleep(0.5)
    else:
        stats.game_active = False

        with open("highscore.json", 'w') as f_object:
            json.dump("", f_object)
            json.dump(sb.stats.high_score, f_object)
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        #An alien has hit the bottom of its bottom rect attribute is greater than the screen rect bottom attribute
        if alien.rect.bottom >= screen_rect.bottom:
        #Treat the same as if a ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """Check to see if there is a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()



'''
The game_functions file contains a number of functions that carry out the bulk of the work in the game. The check_events functions detects relevant events such as keypresses and releases, and
processes each of these types of events through the helped functions check_key_down_events() and check key up. For now, the functions manage the movement of the ship. The game_functions
module also contains update_screen which redraws the screen on each pass through the main loop
'''