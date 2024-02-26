import random
from typing import Optional, Tuple, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class AlwaysRedLogic(BaseLogic):

    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        props = board_bot.properties
        red_diamonds: List[GameObject] = [diamond for diamond in board.diamonds if diamond.properties.points == 2]
        
        # Analyze new state
        if props.diamonds == 4:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        elif props.milliseconds_left < 10000 and props.diamonds > 0: # should take into account distance from base
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        elif len(red_diamonds) > 0:
            # Move to the nearest red diamond
            nearest_red_diamond: GameObject = get_nearest_object(board_bot, red_diamonds)
            self.goal_position = nearest_red_diamond.position
        else:
            # Move to the diamond button (reset button)
            for object in board.game_objects:
                if (object.type == "DiamondButtonGameObject"):
                    diamond_button: GameObject = object;
            
            self.goal_position = diamond_button.position

        # Move to goal if the goal exists
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


# Additional functions

def get_steps_from_object(board_bot: GameObject, another_object: GameObject) -> int:
    y_steps: int = abs(board_bot.position.y - another_object.position.y)
    x_steps: int = abs(board_bot.position.x - another_object.position.x)
    return y_steps + x_steps

def get_nearest_object(board_bot: GameObject, objects: List[GameObject]) -> GameObject:
    nearest_object: GameObject = objects[0]
    smallest_steps: int = get_steps_from_object(board_bot, nearest_object)
    for object in objects:
        steps: int = get_steps_from_object(board_bot, object)
        if (steps < smallest_steps):
            nearest_object = object
            smallest_steps = steps
    
    return nearest_object
