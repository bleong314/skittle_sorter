import numpy as np
import Point
import Peg

class Player:
    def __init__(self, color, number, directions, origin):
        """
        Initialize a player.
        color: string indicating the color of the player (e.g., 'red', 'blue')
        number: integer indicating the number of the player
        directions: an array of strings representing coordinate movements with respect to each player
        pieces: an array of Pegs representing the pegs a player occupies

        Each player should also have a triangle start associated with them 
        Each player should also have a triangle end associated with them
        Each player should also have an array of pegs associated with them
        """
        self.color = color
        self.number = number
        self.directions = {}
        # Intialize the player directions
        self.directions["UL"] = directions[0]
        self.directions["UR"] = directions[1]
        self.directions["R"] = directions[2]
        self.directions["DR"] = directions[3]
        self.directions["DL"] = directions[4]
        self.directions["L"] = directions[5]
        # Set the origin of the pegs and the current state of pegs
        self.initial_pegs = self.initialize_pegs(origin)
        self.current_pegs = self.initial_pegs.copy()
    
    def initialize_pegs(self, origin):
        """
        Initializes the pegs and their position
        origin: tuple representing the origin of the positions
        """
        self.pegs = []
        for i in range(3):
            for j in range(i - 1):
                cur_position = origin + self.directions["UL"] * i + self.directions["R"] * j
                cur_peg = Peg(cur_position, True, False, self.color)
                self.pegs.append(cur_peg)
    
    def reset_pegs(self):
        self.current_pegs = self.initial_pegs.copy()

red_directions = [Point(-1, 1), Point(1, 1), Point(2, 0), Point(1, -1), Point(-1, -1), Point(-2, 0)]
orange_directions = [Point(1, 1), Point(2, 0), Point(1, -1), Point(-1, -1), Point(-2, 0), Point(-1, 1)]
blue_directions = [Point(2, 0), Point(1, -1), Point(-1, -1), Point(-2, 0), Point(-1, 1), Point(1, 1)]
yellow_directions = [Point(1, -1), Point(-1, -1), Point(-2, 0), Point(-1, 1), Point(1, 1), Point(2, 0)]
purple_directions = [Point(-1, -1), Point(-2, 0), Point(-1, 1), Point(1, 1), Point(2, 0), Point(1, -1)]
green_directions = [Point(-2, 0), Point(-1, 1), Point(1, 1), Point(2, 0), Point(1, -1), Point(-1, -1)]

player_1 = Player("Red", 1, red_directions, Point(0, 17))