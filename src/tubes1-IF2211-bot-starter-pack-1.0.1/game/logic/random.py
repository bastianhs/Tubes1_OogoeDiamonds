import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class RandomLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        self.goal_position = closestdiamonds(board_bot, board)
        print(self.goal_position)
        props = board_bot.properties
        # Analyze new state
        if props.diamonds > 0 and props.milliseconds_left < 10000 :
            # Waktu mepet
            self.goal_position = board_bot.properties.base
        elif props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base

        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )
        return delta_x, delta_y
    
def closestdiamonds(board_bot: GameObject, board: Board) -> Position :
    jejak = Position
    distance = 2000

    # Memungkinkan untuk menekan tombol reset
    diamondbutton: Position = getdiamondbutton(board)
    xtobutton = abs(board_bot.position.x - diamondbutton.x)
    ytobutton = abs(board_bot.position.y - diamondbutton.y)
    ratiodiamond = (xtobutton + ytobutton) / 0.8
    if ratiodiamond < distance :
        jejak = diamondbutton
        distance = ratiodiamond

    for i in range(len(board.diamonds)) :
        x = abs(board_bot.position.x - board.diamonds[i].position.x)
        y = abs(board_bot.position.y - board.diamonds[i].position.y)
        step = x+y
        ratio = step / board.diamonds[i].properties.points
        stepmusuh = theclosesttothediamond(board, board.diamonds[i].position)
        print("jarak diamond", ratio, "step anda", step, "Step musuh", stepmusuh)
        if distance > ratio and stepmusuh >= step :
            if not (board.diamonds[i].properties.points == 2 and board_bot.properties.diamonds == 4) : 
                distance = ratio
                jejak = board.diamonds[i].position
            # print(board.diamonds[i].position)
    print("jarak",distance)
    return jejak

def getdiamondbutton(board: Board) -> Position :
    for i in range (len(board.game_objects)) :
        if(board.game_objects[i].type == 'DiamondButtonGameObject') :
            return board.game_objects[i].position

#Mencari musuh yang memiliki jarak terdekat dengan diamond
def theclosesttothediamond(board:Board, diamondposition: Position) -> int :
    stepmusuh = 2000
    for i in range(len(board.bots)) :
        x = abs(board.bots[i].position.x - diamondposition.x)
        y = abs(board.bots[i].position.y - diamondposition.y)
        if stepmusuh > (x+y) :
            stepmusuh = x+y
    return stepmusuh

