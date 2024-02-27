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
    distance = 200
    for i in range(len(board.diamonds)) :
        x = abs(board_bot.position.x - board.diamonds[i].position.x)
        y = abs(board_bot.position.y - board.diamonds[i].position.y)
        ratio = (x+y) / board.diamonds[i].properties.points
        if distance > ratio :
            if not (board.diamonds[i].properties.points == 2 and board_bot.properties.diamonds == 4) : 
                distance = ratio
                jejak = board.diamonds[i].position
            # print(board.diamonds[i].position)
    return jejak

        

