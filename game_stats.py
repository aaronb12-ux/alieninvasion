import json

class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        #Start alien invasion in an active state
        self.game_active = False
        #high score should never be reset

        #load the high score from the json file
        filename = 'highscore.txt'
        with open(filename, 'r') as f_obj:
            
                high_score = json.load(f_obj)
                
        self.high_score = high_score

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

        