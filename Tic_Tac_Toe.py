import pygame
import sys
from math import sqrt


class TicTacToe:
    def __init__(self):
        """initializing variables for playing"""
        self.board = [['', '', ''],
                      ['', '', ''],
                      ['', '', '']]
        self.player = ('X', '0')
        self.current_player = self.player[0]
        self.wins = {self.player[0]: 0,
                     self.player[1]: 0,
                     None: 0}
        self.playing = False
        self.winner = None
        self.list = []
        self.mouse_pos_menu = [0, 0]
        self.mouse_pos_reset = (0, 0)
        """initializing board"""
        pygame.init()
        self.winWidth = 600
        self.winHeight = 750
        self.win = pygame.display.set_mode((self.winWidth, self.winHeight))
        pygame.display.set_caption("Tic tac toe")
        self._start_game()
        self._reset_button()

    def _start_game(self):
        flag = True
        self.win.fill((255, 255, 255))
        while flag:
            image = pygame.image.load('start.png')
            image = pygame.transform.scale(image, (int(self.winWidth / 3), int(self.winWidth // 3)))
            win_rect = self.win.get_rect()
            image_rect = image.get_rect()
            image_rect.center = win_rect.center
            redbox = pygame.image.load("redbox.png")
            redbox = pygame.transform.scale(redbox, (int(self.winWidth * 2 / 3), int(self.winWidth * 2 / 3)))
            redbox_rect = redbox.get_rect()
            redbox_rect.center = win_rect.center
            greenbox = pygame.image.load("greenbox.png")
            greenbox = pygame.transform.scale(greenbox, (int(redbox_rect.height), int(redbox_rect.width)))
            self.win.blit(image, image_rect)
            pygame.display.update()
            self._check_events()
            mx, my = self.mouse_pos_menu[0], self.mouse_pos_menu[1]

            if (mx > redbox_rect.x) and (mx < (redbox_rect.x + redbox_rect.width)) and (my > redbox_rect.y) and (
                    my < redbox_rect.y + redbox_rect.height):
                self.win.blit(greenbox, redbox_rect)
                if pygame.mouse.get_pressed()[0]:
                    self.playing = True
                    flag = False
            else:
                self.win.blit(redbox, redbox_rect)

    def _reset_button(self):
        image = pygame.image.load('rst.png')
        image = pygame.transform.scale(image, (50, 50))
        rect = image.get_rect()
        win_rect = self.win.get_rect()
        rect.midbottom = win_rect.midbottom
        self.win.blit(image, rect)
        self._check_events()
        if rect.collidepoint(self.mouse_pos_reset[0], self.mouse_pos_reset[1]):
            self._reset_stats()

    def run_game(self):
        self._make_board()
        while self.playing:
            self._reset_button()
            self._check_events()
            self._check_rows()
            self._check_diagonals()
            self._check_colums()
            self._check_tie()
            if not self.playing:
                self.wins[self.winner] += 1
            if self.winner or self._full_board():
                if self.winner:
                    self._finish_the_game(self.list[0], self.list[1], self.list[2])
                else:
                    self._finish_the_game()
                self._reset_stats()
            pygame.display.update()
        pygame.quit()

    def _reset_stats(self):
        self.winner = None
        self.playing = True
        self.board = [['', '', ''],
                      ['', '', ''],
                      ['', '', '']]
        self.list = []
        self.current_player = self.player[0]
        self._make_board()

    def _make_board(self):
        self.win.fill((0, 0, 0))
        pygame.draw.line(self.win, (255, 255, 255), (0, 200), (600, 200), 5)
        pygame.draw.line(self.win, (255, 255, 255), (0, 400), (600, 400), 5)
        pygame.draw.line(self.win, (255, 255, 255), (200, 0), (200, 600), 5)
        pygame.draw.line(self.win, (255, 255, 255), (400, 0), (400, 600), 5)
        self._write_text("Player1", (70, 630))
        self._write_text("Tie", (275, 630))
        self._write_text("Player2", (420, 630))
        self._write_text(str(self.wins['X']), (110, 670))
        self._write_text(str(self.wins[None]), (290, 670))
        self._write_text(str(self.wins['0']), (460, 670))
        self._write_text("Current player ", (0, 710))
        self._write_text(self.current_player, (240, 710))

    def _write_text(self, msg, pos):
        font = pygame.font.SysFont('comics', 40, True)
        text = font.render(msg, 1, (255, 255, 255))
        self.win.blit(text, pos)

    def _full_board(self):
        for i in range(3):
            for j in range(3):
                if not self.board[i][j]:
                    return False
        return True

    def _flip_player(self):
        if self.current_player == self.player[0]:
            self.current_player = self.player[1]
        else:
            self.current_player = self.player[0]
        pygame.draw.rect(self.win, (0, 0, 0), (240, 710, 30, 30))
        self._write_text(self.current_player, (240, 710))

    def _check_rows(self):
        for i in range(3):
            if (self.board[i][0] == self.board[i][1]) and (self.board[i][0] == self.board[i][2]) and self.board[i][0]:
                self.winner = self.board[i][0]
                self.list.append((0, i))
                self.list.append((1, i))
                self.list.append((2, i))
                self.playing = False

    def _check_diagonals(self):
        if (self.board[0][0] == self.board[1][1]) and (self.board[0][0] == self.board[2][2]) and self.board[0][0]:
            self.winner = self.board[0][0]
            self.list.append((0, 0))
            self.list.append((1, 1))
            self.list.append((2, 2))
            self.playing = False
        if (self.board[0][2] == self.board[1][1]) and (self.board[1][1] == self.board[2][0]) and self.board[2][0]:
            self.winner = self.board[1][1]
            self.list.append((2, 0))
            self.list.append((1, 1))
            self.list.append((0, 2))
            self.playing = False

    def _check_colums(self):
        for i in range(3):
            if (self.board[0][i] == self.board[1][i]) and (self.board[0][i] == self.board[2][i]) and self.board[0][i]:
                self.winner = self.board[0][i]
                self.playing = False
                self.list.append((i, 0))
                self.list.append((i, 1))
                self.list.append((i, 2))

    def _check_tie(self):
        if self._full_board():
            self.playing = False

    def _update_screen(self, pos):
        if self.current_player == self.player[0]:
            points = [(pos[0] * 200 + 30, pos[1] * 200 + 44), (pos[0] * 200 + 44, pos[1] * 200 + 30),
                      (pos[0] * 200 + 170, pos[1] * 200 + 156), (pos[0] * 200 + 156, pos[1] * 200 + 170)]
            pygame.draw.polygon(self.win, (255, 255, 255), points, 0)
            points = [(pos[0] * 200 + 30, pos[1] * 200 + 156), (pos[0] * 200 + 44, pos[1] * 200 + 170),
                      (pos[0] * 200 + 170, pos[1] * 200 + 44), (pos[0] * 200 + 156, pos[1] * 200 + 30)]
            pygame.draw.polygon(self.win, (255, 255, 255), points, 0)
        else:
            pygame.draw.circle(self.win, (255, 255, 255), (pos[0] * 200 + 100, pos[1] * 200 + 100), 70, 20)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if self.playing:
                        self.mouse_pos_reset = pygame.mouse.get_pos()
                        pos = list(pygame.mouse.get_pos())
                        pos[0] //= 200
                        pos[1] //= 200
                        if pos[0] in [0, 1, 2] and pos[1] in [0, 1, 2]:
                            if not self.board[pos[1]][pos[0]]:
                                self.board[pos[1]][pos[0]] = self.current_player
                                self._update_screen(pos)
                                self._flip_player()

                self.mouse_pos_menu.pop()
                self.mouse_pos_menu.pop()
                self.mouse_pos_menu = list(pygame.mouse.get_pos())


    def _finish_the_game(self, pos1=None, pos2=None, pos3=None):
        if self.winner:
            self._flip_player()
            for i in range(10):
                self._check_events()
                pygame.draw.rect(self.win, (0, 0, 0), (pos1[0] * 200 + 10, pos1[1] * 200 + 10, 180, 180))
                pygame.draw.rect(self.win, (0, 0, 0), (pos2[0] * 200 + 10, pos2[1] * 200 + 10, 180, 180))
                pygame.draw.rect(self.win, (0, 0, 0), (pos3[0] * 200 + 10, pos3[1] * 200 + 10, 180, 180))
                pygame.display.update()
                pygame.time.delay(100)
                self._update_screen(pos1)
                self._update_screen(pos2)
                self._update_screen(pos3)
                pygame.display.update()
                pygame.time.delay(100)
        else:
            for i in range(10):
                self._check_events()
                pygame.draw.line(self.win, (0, 0, 0), (0, 200), (600, 200), 5)
                pygame.draw.line(self.win, (0, 0, 0), (0, 400), (600, 400), 5)
                pygame.draw.line(self.win, (0, 0, 0), (200, 0), (200, 600), 5)
                pygame.draw.line(self.win, (0, 0, 0), (400, 0), (400, 600), 5)
                pygame.display.update()
                pygame.time.delay(100)
                pygame.draw.line(self.win, (255, 255, 255), (0, 200), (600, 200), 5)
                pygame.draw.line(self.win, (255, 255, 255), (0, 400), (600, 400), 5)
                pygame.draw.line(self.win, (255, 255, 255), (200, 0), (200, 600), 5)
                pygame.draw.line(self.win, (255, 255, 255), (400, 0), (400, 600), 5)
                pygame.display.update()
                pygame.time.delay(100)


if __name__ == '__main__':
    ttc = TicTacToe()
    ttc.run_game()
