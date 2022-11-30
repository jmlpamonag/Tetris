import pygame
import os
import random
main_dir = os.path.split(os.path.abspath(__file__))[0]



class Game:
    def __init__(self, ):
        self.state = "start"
        self.score = 0
        self.combo = -1 #initialize combo meter -Hai Hoang
        self.rotation = 0
        self.ShiftX = 0
        self.ShiftY = 0
        self.Tzoom = 20
        self.Figures = [
            [[1, 5, 9, 13], [4, 5, 6, 7]],
            [[4, 5, 9, 10], [2, 6, 5, 9]],
            [[6, 7, 9, 10], [1, 5, 6, 10]],
            [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
            [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
            [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
            [[1, 2, 5, 6]],
        ]
        self.typet = 0
        self.color = 0

    def make_figure(self):
        self.ShiftX = 3
        self.ShiftY = 0
        self.rotation = 0
        self.typet = random.randint(0, len(self.Figures) - 1)
        self.color = random.randint(1, len(Color.colors) - 1)



    def draw_figure(self, screen, x=100, y=60, colors=()):
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                image = self.Figures[self.typet][self.rotation]
                if p in image:
                    pygame.draw.rect(screen.screen, colors[self.color],
                                     [x + self.Tzoom * (j + self.ShiftX) + 1,
                                      y + self.Tzoom * (i + self.ShiftY) + 1,
                                      self.Tzoom - 2, self.Tzoom - 2])
    

    def go_space(self, board):
        while not self.intersects(self.Figures[self.typet][self.rotation], board):
            self.ShiftY += 1
        self.ShiftY -= 1
        self.freeze(self.Figures[self.typet][self.rotation], board)

    def go_down(self, board):
        self.ShiftY += 1
        if self.intersects(self.Figures[self.typet][self.rotation], board):
            self.ShiftY -= 1
            self.freeze(self.Figures[self.typet][self.rotation], board)

    def go_side(self, dx, board):
        old_x = self.ShiftX
        self.ShiftX += dx
        if self.intersects(self.Figures[self.typet][self.rotation], board):
            self.ShiftX = old_x

    def rotate(self, board):
        def rotate_figure():
            self.rotation = (self.rotation + 1) % len(self.Figures[self.typet])

        old_rotation = self.rotation
        rotate_figure()
        if self.intersects(self.Figures[self.typet][self.rotation], board):
            self.rotation = old_rotation

    def intersects(self, image, board):
        intersection = False
        # code smell - what is 4? Magic number
        for i in range(4):
            for j in range(4):
                if i * 4 + j in image:
                    # out of bounds
                    # code smell - confusing, why Y is related i and X is related j?
                    if i + self.ShiftY > board.height - 1 or \
                            j + self.ShiftX > board.width - 1 or \
                            j + self.ShiftX < 0 or \
                            board.Field[i + self.ShiftY][j + self.ShiftX] > 0:
                        intersection = True
        return intersection


    def default_score_computation(self, lines):
        return lines ** 2
    def combo_score_computation(self, lines):
        if(lines==0):
            self.combo = -1;#combo has broken, reset combo meter
        else:
            self.combo +=lines
        return lines*(3+self.combo)

    #def combo_calculation(self)
    def break_lines(self, board):
        lines = 0
        for i in range(1, board.height):
            zeros = 0
            for j in range(board.width):
                if board.Field[i][j] == 0:
                    zeros += 1
            # this row is full
            if zeros == 0:
                lines += 1
                for k in range(i, 1, -1):
                    for j in range(board.width):
                        board.Field[k][j] = board.Field[k - 1][j]
        self.score+= self.combo_score_computation(lines)



    def freeze(self, image, board):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in image:
                    board.Field[i + self.ShiftY][j + self.ShiftX] = self.color
        self.break_lines(board)
        self.make_figure()
        if self.intersects(image, board):
            self.state = "gameover"

class Sound:
    def load_sound(self,file):
        """ because pygame can be be compiled without mixer."""
        if not pygame.mixer:
            return None
        file = os.path.join(main_dir, "data", file)
        try:
            sound = pygame.mixer.Sound(file)
            return sound
        except pygame.error:
            print("Warning, unable to load, %s" % file)
        return None
    def hitmarker(self):
        self.load_sound('hitmarker_2.mp3').play()
    def highscore(self):
        self.load_sound('ode_to_joy_snip.mp3').play()
        


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    colors = (
        (0, 0, 0),
        (120, 37, 179),
        (100, 179, 179),
        (80, 34, 22),
        (80, 134, 22),
        (180, 34, 22),
        (180, 34, 122),
    )


class Board:
    def __init__(self, height=20, width=10):
        self.height = height
        self.width = width
        self.Field = self.boardy()

    def boardy(self):
        field = []
        for i in range(self.height):
            new_line = [0] * self.width  # polymorphism using *
            field.append(new_line)
        return field

    def draw_board(self, screen, x=100, y=60, zoom=20):
        screen.fill_background(Color.WHITE)
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen.screen, Color.GRAY, [x + zoom * j, y + zoom * i, zoom, zoom], 1)
                if self.Field[i][j] > 0:
                    pygame.draw.rect(screen.screen, Color.colors[self.Field[i][j]],
                                     [x + zoom * j + 1, y + zoom * i + 1, zoom - 2, zoom - 1])


class Screen:
    def __init__(self, width=400, height=500, background_color=Color.WHITE, font_type="monospace", font_size=35,
                 clock_tick=25, caption="Tetris"):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont(font_type, font_size, True, False)
        self.clock = pygame.time.Clock()
        self.clock_tick = clock_tick
        self.caption = pygame.display.set_caption(caption)

    def fill_background(self, background_color):
        self.screen.fill(background_color)

    def update_screen(self):
        pygame.display.flip()
        self.clock.tick(self.clock_tick)

    def add_text(self, font_type, font_size, text, bool, color, range):
        font = pygame.font.SysFont(font_type, font_size, True, False)
        label = font.render(text, bool, color)
        self.screen.blit(label, range)


def play_game():
    board = Board()
    game = Game()
    color = Color()
    screen = Screen()
    sound = Sound()
    colors_list = color.colors
    counter = 0
    pressing_down = False

    game.make_figure()
    done = False
    while not done:
        counter += 1
        if counter > 100000:
            counter = 0

        # Check if we need to automatically go down
        if counter % (25 // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                #makes csgo hitmarker sound on press
                sound.highscore()
                if event.key == pygame.K_UP:
                    game.rotate(board)
                if event.key == pygame.K_LEFT:
                    game.go_side(-1, board)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1, board)
                if event.key == pygame.K_SPACE:
                    game.go_space(board)
                if event.key == pygame.K_q:
                    if game.state == "gameover":
                        done = True
                if event.key == pygame.K_DOWN:
                    pressing_down = True

            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                pressing_down = False

        board.draw_board(screen=screen)

        game.draw_figure(screen=screen, colors=colors_list)
        text = f"Score: {game.score}"
        screen.add_text(font_type='Calibri', font_size=25, text=text, color=Color.BLACK, bool=True, range=[0, 0])

        if game.state == "gameover":
            #to add game sounds here... once someone implements highscore
            screen.add_text(font_type='Calibri', font_size=65, text="Game Over", bool=True, color=(255, 125, 0),
                            range=[20, 200])
            screen.add_text(font_type='Calibri', font_size=65, text="Enter q to Quit", bool=True, color=(255, 215, 0),
                            range=[25, 265])

        # refresh the screen
        screen.update_screen()

    pygame.quit()


def main():
    pygame.init()
    play_game()


if __name__ == "__main__":
    main()
