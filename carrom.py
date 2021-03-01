import pygame
from coin import CarromMen, Queen, Striker
from pygame import Rect
from pygame import Vector2
from math import sqrt
from itertools import combinations
from board import Board

class Carrom:
    def __init__(self, board_rect: Rect):
        board = Board(board_rect)
        self.board = board
        self.center = Vector2(board.container.center)
        self.queen = Queen(board.coin_radius, Board.COIN_MASS, self.center, board.container)
        self.striker = Striker(board.striker_radius, Board.STRIKER_MASS, board.container)
        self.coins = [CarromMen(i % 2, board.coin_radius, Board.COIN_MASS, self.center, board.container) for i in range(6)] \
            + [CarromMen(0, board.coin_radius, Board.COIN_MASS, self.center, board.container) for _ in range(6)]\
            + [CarromMen(1, board.coin_radius, Board.COIN_MASS, self.center, board.container) for _ in range(6)]
        self.rotate_carrom_men(60)

        self.player_coins = ([], [])
        for coin in self.coins:
            self.player_coins[coin.get_player()].append(coin)
        self.pocketed_coins = ([], [])
        self.foul_count = [0, 0]
        self.has_queen = [False, False]
        self.pocketed_queen = False
        self.queen_on_hold = False
        self.pocketed_striker = False
        self.current_pocketed = []
        self.player_turn = 0
        self.game_over = False
        self.winner = None
        self.reason = None
        self.first_collision = None

    def rotate_carrom_men(self, init_rotation=60):
        vec = Vector2(0, -1)
        vec.rotate_ip(init_rotation)
        vec.scale_to_length(self.board.coin_radius * 2)
        for index, coin in enumerate(self.coins):
            if index == 6:
                vec.scale_to_length(self.board.coin_radius * 4)
            elif index == 12:
                vec.scale_to_length(self.board.coin_radius * (2 * sqrt(3)))
                vec.rotate_ip(30)
            coin.position = self.center + vec
            vec.rotate_ip(60)

    def check_moving(self):
        coins = self.player_coins[0] + self.player_coins[1]
        if not self.pocketed_striker:
            coins.append(self.striker)
        if not self.pocketed_queen:
            coins.append(self.queen)
        return any(coin.check_moving() for coin in coins)

    def update(self, dt, decelerate, e):
        coins = sorted(self.player_coins[0] + self.player_coins[1],
                       key=lambda coin_: coin_.get_player() == self.player_turn, reverse=True)
        if not self.pocketed_striker:
            coins.append(self.striker)
        if not self.pocketed_queen:
            coins.append(self.queen)

        for coin1, coin2 in combinations(coins, 2):
            if coin1.check_collision(coin2):
                if not self.first_collision and (coin1.check_moving() or coin2.check_moving()):
                    self.first_collision = [coin1, coin2]
                coin1.collide(coin2, e)

        for coin in coins:
            coin.update(dt, decelerate)
            if self.board.pocketed(coin):
                if coin == self.striker:
                    self.pocketed_striker = True
                elif coin == self.queen:
                    self.pocketed_queen = True
                else:
                    assert isinstance(coin, CarromMen)
                    self.player_coins[coin.get_player()].remove(coin)
                    self.pocketed_coins[coin.get_player()].append(coin)
                    self.current_pocketed.append(coin)

    def __handle_fouls__(self, player):
       for _ in range(self.foul_count[player]):
            if self.pocketed_coins[player]:
                coin = self.pocketed_coins[player].pop()
                self.player_coins[player].append(coin)
                coin.reset()
                self.foul_count[player] -= 1
            else:
                assert not (self.has_queen[0] and self.has_queen[1])
                if self.pocketed_queen and self.has_queen[player]:
                    self.has_queen[player] = False
                    self.queen_on_hold = False
                    self.pocketed_queen = False
                    self.queen.reset()
                    self.foul_count[player] -= 1
                break

    def __update_turn__(self, change: bool):
        self.__handle_fouls__(0)
        self.__handle_fouls__(1)

        if not self.player_coins[self.player_turn]:
            if not self.pocketed_queen:
                self.foul_count[self.player_turn] += 2
                self.__update_turn__(change=True)
                return
            else:
                self.winner = self.player_turn
                self.reason = "Player pocketed all coins"
                self.game_over = True
                return
        other_player = (self.player_turn + 1) % 2
        if not self.player_coins[other_player]:
            if not self.pocketed_queen or not (self.has_queen[0] or self.has_queen[1]):
                coin = self.pocketed_coins[other_player].pop()
                self.player_coins[other_player].append(coin)
                coin.reset()
                self.foul_count[self.player_turn] += 2
                if self.pocketed_queen:
                    self.queen_on_hold = False
                    self.pocketed_queen = False
                    self.queen.reset()

                self.__update_turn__(change=True)
                return
            else:
                self.winner = other_player
                self.reason = "Player pocketed all of other players coins"
                self.game_over = True
                return

        self.current_pocketed = []
        self.pocketed_striker = False
        self.striker.velocity = Vector2()
        if change:
            self.player_turn = (self.player_turn + 1) % 2

    def current_player(self):
        return "WHITE" if self.player_turn == 0 else "BLACK"

    @staticmethod
    def get_player(player):
        return "WHITE" if player == 0 else "BLACK"

    def apply_rules(self):
        if self.first_collision:
            coin1, coin2 = self.first_collision
            assert isinstance(coin1, Striker) or isinstance(coin2, Striker)
            coin = coin2 if isinstance(coin1, Striker) else coin1
            if not isinstance(coin, Queen):
                if self.player_turn != coin.get_player():
                    self.foul_count[self.player_turn] += 1
            self.first_collision = None
        if self.pocketed_striker:
            if self.pocketed_queen and not self.has_queen[0] and not self.has_queen[1]:
                self.queen_on_hold = False
                self.pocketed_queen = False
                self.queen.reset()
            for coin in self.current_pocketed:
               if coin.get_player() == self.player_turn:
                    self.player_coins[coin.get_player()].append(coin)
                    self.pocketed_coins[coin.get_player()].remove(coin)
                    coin.reset()
            self.foul_count[self.player_turn] += 1
            self.__update_turn__(change=True)

        elif self.pocketed_queen and not self.has_queen[0] and not self.has_queen[1]:
            for coin in self.current_pocketed:
                if coin.get_player() == self.player_turn:
                    self.has_queen[self.player_turn] = True
                    self.queen_on_hold = False
                    self.__update_turn__(change=False)
                    break
            else:
                if self.queen_on_hold:
                    self.queen_on_hold = False
                    self.pocketed_queen = False
                    self.queen.reset()
                    self.__update_turn__(change=True)
                else:
                    self.queen_on_hold = True
                    self.__update_turn__(change=False)

        else:
            for coin in self.current_pocketed:
                if coin.get_player() == self.player_turn:
                    self.__update_turn__(change=False)
                    break
            else:
                self.__update_turn__(change=True)

    def draw(self, win):
        self.board.draw(win)
        coins = self.player_coins[0] + self.player_coins[1]
        if not self.pocketed_striker:
            coins.append(self.striker)
        if not self.pocketed_queen:
            coins.append(self.queen)
        for coin in coins:
            coin.draw(win)
        captured_coins_0 = self.pocketed_coins[0].copy()
        if self.has_queen[0]:
            captured_coins_0.append(self.queen)
        captured_coins_1 = self.pocketed_coins[1].copy()
        if self.has_queen[1]:
            captured_coins_1.append(self.queen)
        self.board.draw_captured_coins(win, 0, captured_coins_0)
        self.board.draw_captured_coins(win, 1, captured_coins_1)
