import pygame
import sys
from math import sqrt


class Tic_Tac_Toe:
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
        """initializing board"""
        pygame.init()
        self.win = pygame.display.set_mode((600, 750))
        pygame.display.set_caption("Tic tac toe")
        self.start_game()

    def start_game(self):
        flag = True
        self.win.fill((255, 255, 255))
        while flag:
            image = pygame.image.load('start.png')
            image = pygame.transform.scale(image, (200, 200))
            win_rect = self.win.get_rect()
            image_rect = image.get_rect()
            image_rect.center = win_rect.center
            self.win.blit(image, image_rect)
            pygame.display.update()
            self.check_events()
            distance = sqrt((image_rect.center[0] - self.mouse_pos_menu[0]) ** 2 +
                            (image_rect.center[1] - self.mouse_pos_menu[1]) ** 2)

            if distance < image_rect[2] // 2:
                self.playing = True
                flag = False

    def run_game(self):
        self.make_board()
        while self.playing:
            self.check_events()
            self.check_rows()
            self.check_diagonals()
            self.check_colums()
            self.check_tie()
            if not self.playing:
                self.wins[self.winner] += 1
            if self.winner or self.full_board():
                if self.winner:
                    self.finish_the_game(self.list[0], self.list[1], self.list[2])
                else:
                    self.finish_the_game()
                self.reset_game()
            pygame.display.update()
        pygame.quit()

    def reset_game(self):
        self.winner = None
        self.playing = True
        self.board = [['', '', ''],
                      ['', '', ''],
                      ['', '', '']]
        self.list = []
        self.current_player = self.player[0]
        self.make_board()

    def make_board(self):
        self.win.fill((0, 0, 0))
        pygame.draw.line(self.win, (255, 255, 255), (0, 200), (600, 200), 5)
        pygame.draw.line(self.win, (255, 255, 255), (0, 400), (600, 400), 5)
        pygame.draw.line(self.win, (255, 255, 255), (200, 0), (200, 600), 5)
        pygame.draw.line(self.win, (255, 255, 255), (400, 0), (400, 600), 5)
        self.write_text("Player1", (70, 630))
        self.write_text("Tie", (275, 630))
        self.write_text("Player2", (420, 630))
        self.write_text(str(self.wins['X']), (110, 670))
        self.write_text(str(self.wins[None]), (290, 670))
        self.write_text(str(self.wins['0']), (460, 670))
        self.write_text("Current player ", (0, 710))
        self.write_text(self.current_player, (240, 710))

    def write_text(self, msg, pos):
        font = pygame.font.SysFont('comics', 40, True)
        text = font.render(msg, 1, (255, 255, 255))
        self.win.blit(text, pos)

    def full_board(self):
        for i in range(3):
            for j in range(3):
                if not self.board[i][j]:
                    return False
        return True

    def flip_player(self):
        if self.current_player == self.player[0]:
            self.current_player = self.player[1]
        else:
            self.current_player = self.player[0]
        pygame.draw.rect(self.win, (0, 0, 0), (240, 710, 40, 40))
        self.write_text(self.current_player, (240, 710))

    def check_rows(self):
        for i in range(3):
            if (self.board[i][0] == self.board[i][1]) and (self.board[i][0] == self.board[i][2]) and self.board[i][0]:
                self.winner = self.board[i][0]
                self.list.append((0, i))
                self.list.append((1, i))
                self.list.append((2, i))
                self.playing = False

    def check_diagonals(self):
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

    def check_colums(self):
        for i in range(3):
            if (self.board[0][i] == self.board[1][i]) and (self.board[0][i] == self.board[2][i]) and self.board[0][i]:
                self.winner = self.board[0][i]
                self.playing = False
                self.list.append((i, 0))
                self.list.append((i, 1))
                self.list.append((i, 2))

    def check_tie(self):
        if '' not in self.board[0] and '' not in self.board[1] and '' not in self.board[2]:
            self.playing = False

    def update_screen(self, pos):
        if self.current_player == self.player[0]:
            points = [(pos[0] * 200 + 30, pos[1] * 200 + 44), (pos[0] * 200 + 44, pos[1] * 200 + 30),
                      (pos[0] * 200 + 170, pos[1] * 200 + 156), (pos[0] * 200 + 156, pos[1] * 200 + 170)]
            pygame.draw.polygon(self.win, (255, 255, 255), points, 0)
            points = [(pos[0] * 200 + 30, pos[1] * 200 + 156), (pos[0] * 200 + 44, pos[1] * 200 + 170),
                      (pos[0] * 200 + 170, pos[1] * 200 + 44), (pos[0] * 200 + 156, pos[1] * 200 + 30)]
            pygame.draw.polygon(self.win, (255, 255, 255), points, 0)
        else:
            pygame.draw.circle(self.win, (255, 255, 255), (pos[0] * 200 + 100, pos[1] * 200 + 100), 70, 20)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.playing:
                        pos = list(pygame.mouse.get_pos())
                        pos[0] //= 200
                        pos[1] //= 200
                        if pos[0] in [0, 1, 2] and pos[1] in [0, 1, 2]:
                            if not self.board[pos[1]][pos[0]]:
                                self.board[pos[1]][pos[0]] = self.current_player
                                self.update_screen(pos)
                                self.flip_player()
                    else:
                        self.mouse_pos_menu.pop()
                        self.mouse_pos_menu.pop()
                        self.mouse_pos_menu = list(pygame.mouse.get_pos())

    def finish_the_game(self, pos1=None, pos2=None, pos3=None):
        if self.winner:
            self.flip_player()
            for i in range(10):
                self.check_events()
                pygame.draw.rect(self.win, (0, 0, 0), (pos1[0] * 200 + 10, pos1[1] * 200 + 10, 180, 180))
                pygame.draw.rect(self.win, (0, 0, 0), (pos2[0] * 200 + 10, pos2[1] * 200 + 10, 180, 180))
                pygame.draw.rect(self.win, (0, 0, 0), (pos3[0] * 200 + 10, pos3[1] * 200 + 10, 180, 180))
                pygame.display.update()
                pygame.time.delay(100)
                self.update_screen(pos1)
                self.update_screen(pos2)
                self.update_screen(pos3)
                pygame.display.update()
                pygame.time.delay(100)
        else:
            for i in range(10):
                self.check_events()
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
    ttc = Tic_Tac_Toe()
    ttc.run_game()
