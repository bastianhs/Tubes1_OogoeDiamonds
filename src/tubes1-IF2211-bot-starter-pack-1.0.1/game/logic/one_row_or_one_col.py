import random
from typing import Optional, Tuple, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

# Test Bot
# python main.py --logic one_row_or_one_col --email=your_email@example.com --name=your_name --password=your_password --team etimo

class one_row_or_one_col(BaseLogic):
# Algoritma greedy yang memilih berdasarkan jarak dan point
# hanya diamond yang berada di satu baris atau satu kolom dengan bot yang akan diambil
# prioritas diambil berdasarkan diamond yang memiliki point lebih besar
# jika pada baris/kolom yang sama dengan bot terdapat teleport, maka diamond yang berada pada satu baris dengan teleport lainnya juga dihitung
    
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        ################################ MENDAPATKAN POSISI DARI BOT ################################
        props = board_bot.properties
        x_coordinat_of_bot = board_bot.position.x
        y_coordinat_of_bot = board_bot.position.y

        ################################ PENCARIAN DIAMOND ################################
        # Diamond yang berada langsung pada baris/kolom yang sama dengan bot
        list_of_diamonds = [diamond for diamond in board.diamonds if diamond.position.x == x_coordinat_of_bot or diamond.position.y == y_coordinat_of_bot]

        # Diamond yang berada dekat dengan teleport
        # Mendapatkan teleport
        list_of_teleport = [teleporter for teleporter in board.game_objects if teleporter.type == "TeleportGameObject"]
        teleporter_near_bot = -1
        other_teleport = -1
        distance_to_near_teleport = 9999999
        
        list_of_diamonds_near_teleporter: List[GameObject] = []
        # Mendapatkan diamond yang satu baris dengan teleport lainnya
        if ((list_of_teleport[0].position.x == x_coordinat_of_bot or list_of_teleport[0].position.y == y_coordinat_of_bot) and
           (list_of_teleport[1].position.x == x_coordinat_of_bot or list_of_teleport[1].position.y == y_coordinat_of_bot)) :
            # jika kedua teleport berada pada kolom/baris yang sama dengan bot
            # ambil teleport terdekat yang akan jadi kandidat untuk didekati bot
            # teleport yang lain akan jadi patokan untuk pencarian diamond
            distance_to_teleleport_1 = abs(x_coordinat_of_bot - list_of_teleport[0].position.x) + abs(y_coordinat_of_bot - list_of_teleport[0].position.y)
            distance_to_teleleport_2 = abs(x_coordinat_of_bot - list_of_teleport[1].position.x) + abs(y_coordinat_of_bot - list_of_teleport[1].position.y)
            if distance_to_teleleport_1 < distance_to_teleleport_2:
                list_of_diamonds_near_teleporter = [diamond for diamond in board.diamonds if diamond.position.x == list_of_teleport[1].position.x or diamond.position.y == list_of_teleport[1].position.y]
                teleporter_near_bot = 0
                other_teleport = 1
                distance_to_near_teleport = distance_to_teleleport_1
            else:
                list_of_diamonds_near_teleporter = [diamond for diamond in board.diamonds if diamond.position.x == list_of_teleport[0].position.x or diamond.position.y == list_of_teleport[0].position.y]
                teleporter_near_bot = 1
                other_teleport = 0
                distance_to_near_teleport = distance_to_teleleport_2
        else :
            if list_of_teleport[0].position.x == x_coordinat_of_bot or list_of_teleport[0].position.y == y_coordinat_of_bot:
                list_of_diamonds_near_teleporter = [diamond for diamond in board.diamonds if diamond.position.x == list_of_teleport[1].position.x or diamond.position.y == list_of_teleport[1].position.y]
                teleporter_near_bot = 0
                other_teleport = 1
                distance_to_near_teleport = abs(x_coordinat_of_bot - list_of_teleport[0].position.x) + abs(y_coordinat_of_bot - list_of_teleport[0].position.y)
            elif list_of_teleport[1].position.x == x_coordinat_of_bot or list_of_teleport[1].position.y == y_coordinat_of_bot:
                list_of_diamonds_near_teleporter = [diamond for diamond in board.diamonds if diamond.position.x == list_of_teleport[0].position.x or diamond.position.y == list_of_teleport[0].position.y]
                teleporter_near_bot = 1
                other_teleport = 0
                distance_to_near_teleport = abs(x_coordinat_of_bot - list_of_teleport[1].position.x) + abs(y_coordinat_of_bot - list_of_teleport[1].position.y)
        
        ################################ PENENTUAN ARAH GERAK ################################
        if props.diamonds == 5:
            # Saat inventory sudah penuh, bergerak ke base
            base = board_bot.properties.base
            self.goal_position = base
        elif props.milliseconds_left < 10000 and props.diamonds >= 3: 
            # 10 detik terakhir, harus kembali ke base (jika sudah memiliki 3 atau lebih diamond)
            base = board_bot.properties.base
            self.goal_position = base
        elif len(list_of_diamonds) > 0:
            # Bergerak ke diamond yang memenuhi syarat
            nearest_diamond : GameObject = get_nearest_diamond(board_bot, list_of_diamonds, props.diamonds)         # diamond terdekat yang satu kolom/baris dengan bot

            if len(list_of_diamonds_near_teleporter) > 0:
                # jika ada teleporter didekat bot, dan diteleporter yang lain terdapat diamond
                nearest_diamond_near_teleport : GameObject = get_nearest_diamond_near_teleport(list_of_diamonds_near_teleporter, props.diamonds, list_of_teleport[other_teleport])
                
                distace_to_nearest_diamond = abs(x_coordinat_of_bot - nearest_diamond.position.x) + abs(y_coordinat_of_bot - nearest_diamond.position.y)
                distace_to_nearest_diamond_near_teleport = abs(x_coordinat_of_bot - nearest_diamond_near_teleport.position.x) + abs(y_coordinat_of_bot - nearest_diamond_near_teleport.position.y) + distance_to_near_teleport

                if nearest_diamond_near_teleport.properties.points > nearest_diamond.properties.points:
                    self.goal_position = list_of_teleport[teleporter_near_bot].position
                elif nearest_diamond_near_teleport.properties.points == nearest_diamond.properties.points:
                    if distace_to_nearest_diamond_near_teleport < distace_to_nearest_diamond:
                        self.goal_position = list_of_teleport[teleporter_near_bot].position
                    else:
                        self.goal_position = nearest_diamond.position
                else:
                    self.goal_position = nearest_diamond.position
            else:
                self.goal_position = nearest_diamond.position
        elif len(list_of_diamonds) == 0:
            # Saat tidak ada diamond yang berada satu baris/kolom dengan bot
            if len(list_of_diamonds_near_teleporter) > 0:
                self.goal_position = list_of_teleport[teleporter_near_bot].position
            else:
                for object in board.game_objects:
                    if (object.type == "DiamondButtonGameObject"):
                        diamond_button: GameObject = object;
                self.goal_position = diamond_button.position
        else:
            # Hanya bergerak random
            self.goal_position = None

        ################################ ME-RETURN ARAH GERAK ################################
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

        # Menghindari invalid move
        if (delta_x == 0 and delta_y == 0):
            delta_y = 1
        elif (delta_x == 1 and delta_y == 1):
            delta_y = 0
        elif (delta_x == -1 and delta_y == -1):
            delta_y = 0
            
        return delta_x, delta_y


################################ FUNGSI TAMBAHAN ################################
def get_nearest_diamond(bot: GameObject, diamonds: List[GameObject], current_inventory) -> GameObject:
# Mengembalikan diamond terdekat yang berada pada satu baris / kolom dengan bot
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
        return nearest_red_diamond
    else:
        return nearest_blue_diamond
    
def get_nearest_diamond_near_teleport(diamonds: List[GameObject], current_inventory, teleport: GameObject) -> GameObject:
# Mengembalikan diamond terdekat yang berada pada satu baris / kolom dengan teleport
    min_red_distance = 9999999
    min_blue_distance = 9999999
    nearest_red_diamond: GameObject = None
    nearest_blue_diamond: GameObject = None

    for diamond in diamonds:
        distance = abs(teleport.position.x - diamond.position.x) + abs(teleport.position.y - diamond.position.y)
        if diamond.properties.points == 2 and distance < min_red_distance:
            min_red_distance = distance
            nearest_red_diamond = diamond
        elif diamond.properties.points == 1 and distance < min_blue_distance:
            min_blue_distance = distance
            nearest_blue_diamond = diamond
    
    if nearest_red_diamond and current_inventory < 4:
        return nearest_red_diamond
    else:
        return nearest_blue_diamond