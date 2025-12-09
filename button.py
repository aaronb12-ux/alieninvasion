#lets python render font to the screen
import pygame.font


class Button():
    
    def __init__(self, ai_settings, screen, msg):
        """Initialize button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        #creating the font with default 'None' and size 48
        self.font = pygame.font.SysFont(None, 48)

        #Build the button's rect object and center it
        #using .rect to initialize the x location, y location, width and height of the rect object of the button
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        #the just made rects center is the center of the screen
        self.rect.center = self.screen_rect.center

        #The button message needs to be prepped only once
        self.prep_msg(msg)
    
    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button"""
        #turns the text stored in msg into an image
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        #centering the button and message
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        #Draw blank button and then draw message:
        #screen.fill fills in the color
        self.screen.fill(self.button_color, self.rect)
        #Drawing to screen using 'blit'
        self.screen.blit(self.msg_image, self.msg_image_rect)
