import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class RandomLogic(BaseLogic):
# Algoritma Greedy yang memilih diamond berdasarkan rasio jarak : point
# Bot akan memilih diamond yang memiliki rasio jarak : point terkecil
# Jika bot lawan memiliki posisi lebih dekat dengan diamond yang kita tuju, maka dipilih diamond dengan rasio jarak : point terkecil kedua

    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        ################################ PEMILIHAN DIAMOND / RED BUTTON ################################
        self.goal_position = closestdiamonds(board_bot, board)
        # print(self.goal_position)
        
        ################################ Mendapatkan Properti Bot ################################
        props = board_bot.properties

        ################################ PENENTUAN ARAH GERAK ################################
        if props.diamonds == 5:
            # Saat inventory sudah penuh, bergerak ke base
            base = board_bot.properties.base
            self.goal_position = base
        elif props.diamonds >= 3 and props.milliseconds_left < 10000 :
            # 10 detik terakhir, harus kembali ke base (jika sudah memiliki 3 atau lebih diamond)
            self.goal_position = board_bot.properties.base
        
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
        
        # Menghindari invalid move
        if (delta_x == 0 and delta_y == 0):
            delta_y = 1
        elif (delta_x == 1 and delta_y == 1):
            delta_y = 0
        elif (delta_x == -1 and delta_y == -1):
            delta_y = 0

        return delta_x, delta_y
    
def closestdiamonds(board_bot: GameObject, board: Board) -> Position:
# Mengembalikan posisi diamond yang memiliki rasio jarak : point terkecil jika ada
# Mengembalikan posisi diamond button jika tidak ada diamond yang tersedia
    jejak = Position
    min_ratio = 9999

    # Memilih menekan tombol reset terlebih dahulu
    diamondbutton: Position = getdiamondbutton(board)
    xtobutton = abs(board_bot.position.x - diamondbutton.x)
    ytobutton = abs(board_bot.position.y - diamondbutton.y)
    ratiodiamond = (xtobutton + ytobutton) / 0.8            # Rasio jarak : point untuk diamond button
    if ratiodiamond < min_ratio :
        jejak = diamondbutton
        min_ratio = ratiodiamond

    # Mencari diamond yang memiliki rasio jarak : point terkecil
    for i in range(len(board.diamonds)):
        x = abs(board_bot.position.x - board.diamonds[i].position.x)
        y = abs(board_bot.position.y - board.diamonds[i].position.y)
        step = x+y
        ratio = step / board.diamonds[i].properties.points
        
        stepmusuh = theclosesttothediamond(board, board.diamonds[i].position)
        # print("jarak diamond", ratio, "step anda", step, "Step musuh", stepmusuh)
        if min_ratio > ratio and stepmusuh >= step :
            if not (board.diamonds[i].properties.points == 2 and board_bot.properties.diamonds == 4) : 
                min_ratio = ratio
                jejak = board.diamonds[i].position
            # print(board.diamonds[i].position)
    # print("jarak",distance)
    return jejak

def getdiamondbutton(board: Board) -> Position :
# Mengembalikan posisi diamond button
    for i in range (len(board.game_objects)) :
        if(board.game_objects[i].type == 'DiamondButtonGameObject') :
            return board.game_objects[i].position

def theclosesttothediamond(board:Board, diamondposition: Position) -> int :
# Mengembalikan jarak musuh terdekat ke diamond yang kita tuju
    stepmusuh = 9999
    for i in range(len(board.bots)) :
        x = abs(board.bots[i].position.x - diamondposition.x)
        y = abs(board.bots[i].position.y - diamondposition.y)
        if stepmusuh > (x+y) :
            stepmusuh = x+y
    return stepmusuh
