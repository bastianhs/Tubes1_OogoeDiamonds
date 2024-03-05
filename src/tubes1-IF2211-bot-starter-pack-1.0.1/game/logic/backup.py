import random
from typing import Optional, Tuple, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class one_row_or_one_col(BaseLogic):
# Algoritma greedy yang memilih berdasarkan jarak terdekat
# hanya diamond yang berada di satu baris atau satu kolom dengan bot yang akan diambil
# prioritas diambil berdasarkan diamond yang memiliki point lebih besar
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

# "TeleportGameObject"
    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        # mendapatkan posisi dari bot
        props = board_bot.properties
        x_coordinat_of_bot = board_bot.position.x
        y_coordinat_of_bot = board_bot.position.y
        
        # mendapatkan diamond yang berada di satu baris atau satu kolom dengan bot
        list_of_diamonds = [diamond for diamond in board.diamonds if diamond.position.x == x_coordinat_of_bot or diamond.position.y == y_coordinat_of_bot]
        
        # mendapatkan teleporter
        teleporters_list: List[GameObject] = [teleporter for teleporter in board.game_objects if teleporter.type == "TeleportGameObject"]
        teleporters_near_bot = -1
        teleporters_not_near_bot = -1
        distance_to_near_teleporter = 9999999
        list_of_diamonds_near_teleporter: List[GameObject] = []

        if teleporters_list[0].position.x == x_coordinat_of_bot or teleporters_list[0].position.y == y_coordinat_of_bot:
            for diamond in board.diamonds:
                if teleporters_list[1].position.x == diamond.position.x or teleporters_list[1].position.y == diamond.position.y:
                    list_of_diamonds_near_teleporter.append(diamond)
            teleporters_near_bot = 0
            teleporters_not_near_bot = 1
            distance_to_near_teleporter = abs(x_coordinat_of_bot - teleporters_list[0].position.x) + abs(y_coordinat_of_bot - teleporters_list[0].position.y)
        elif teleporters_list[1].position.x == x_coordinat_of_bot or teleporters_list[1].position.y == y_coordinat_of_bot:
            for diamond in board.diamonds:
                if teleporters_list[0].position.x == diamond.position.x or teleporters_list[0].position.y == diamond.position.y:
                    list_of_diamonds_near_teleporter.append(diamond)
            teleporters_near_bot = 1
            teleporters_not_near_bot = 0
            distance_to_near_teleporter = abs(x_coordinat_of_bot - teleporters_list[1].position.x) + abs(y_coordinat_of_bot - teleporters_list[1].position.y)
        
        # analisis keadaan baru
        if props.diamonds == 5:
            # bergerak ke base
            base = board_bot.properties.base
            self.goal_position = base
        elif props.milliseconds_left < 10000 and props.diamonds >= 3: 
            # 10 detik terakhir, harus kembali ke base (jika sudah memiliki 3 atau lebih diamond)
            base = board_bot.properties.base
            self.goal_position = base
        elif len(list_of_diamonds) > 0:
            # bergerak ke diamond terdekat yang memenuhi syarat
            nearest_diamond: GameObject = get_nearest_diamond(board_bot, list_of_diamonds, props.diamonds)
            nearest_diamond_near_teleporter: GameObject = None
            
            if teleporters_not_near_bot != -1 and len(list_of_diamonds_near_teleporter) > 0:
                nearest_diamond_near_teleporter = (get_nearest_diamond_near_teleporter(list_of_diamonds_near_teleporter, props.diamonds, teleporters_list[teleporters_not_near_bot], distance_to_near_teleporter))
            
            if nearest_diamond_near_teleporter != None:
                if nearest_diamond_near_teleporter[0].properties.points > nearest_diamond[0].properties.points:
                    self.goal_position = teleporters_list[teleporters_near_bot].position
                elif nearest_diamond_near_teleporter[0].properties.points == nearest_diamond[0].properties.points:
                    if nearest_diamond_near_teleporter[1] < nearest_diamond[1]:
                        self.goal_position = teleporters_list[teleporters_near_bot].position
                    else:
                        self.goal_position = nearest_diamond[0].position
                else:
                    self.goal_position = nearest_diamond[0].position
            else:
                self.goal_position = nearest_diamond[0].position
        elif len(list_of_diamonds) == 0:
            # bergerak ke diamond button (reset button)
            for object in board.game_objects:
                if (object.type == "DiamondButtonGameObject"):
                    diamond_button: GameObject = object;
            self.goal_position = diamond_button.position
        else:
            # hanya bergerak random
            self.goal_position = None

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
            # beregerak random
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )
        return delta_x, delta_y

def get_nearest_diamond(bot: GameObject, diamonds: List[GameObject], current_inventory) -> GameObject:
# fungsi untuk mendapatkan diamond terdekat
    min_red_distance = 9999999
    min_blue_distance = 9999999
    nearest_red_diamond: GameObject = None
    nearest_blue_diamond: GameObject = None
    
    for diamond in diamonds:
        distance = abs(bot.position.x - diamond.position.x) + abs(bot.position.y - diamond.position.y)
        if diamond.properties.points == 2 and distance < min_red_distance:
            min_red_distance = distance
            nearest_red_diamond = diamond
        elif diamond.properties.points == 1 and distance < min_blue_distance:
            min_blue_distance = distance
            nearest_blue_diamond = diamond
    if nearest_red_diamond and current_inventory < 4:
        return (nearest_red_diamond, min_red_distance)
    else:
        return (nearest_blue_diamond, min_blue_distance)
    
def get_nearest_diamond_near_teleporter(diamonds: List[GameObject], current_inventory, other_teleporter, distance_to_teleporter) -> GameObject:
    # fungsi untuk mendapatkan diamond terdekat yang berada di dekat teleporter
    min_red_distance = 9999999
    min_blue_distance = 9999999
    nearest_red_diamond: GameObject = None
    nearest_blue_diamond: GameObject = None

    for diamond in diamonds:
        distance = abs(other_teleporter.position.x - diamond.position.x) + abs(other_teleporter.position.y - diamond.position.y) + distance_to_teleporter
        if diamond.properties.points == 2 and distance < min_red_distance:
            min_red_distance = distance
            nearest_red_diamond = diamond
        elif diamond.properties.points == 1 and distance < min_blue_distance:
            min_blue_distance = distance
            nearest_blue_diamond = diamond
    if nearest_red_diamond and current_inventory < 4:
        return (nearest_red_diamond, min_red_distance)
    else:
        return (nearest_blue_diamond, min_blue_distance)