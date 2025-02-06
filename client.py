import pygame
from network import Network
import pickle
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 190
        self.height = 100

    def draw(self, win):
        # Gradient Effect
        pygame.draw.rect(win, (self.color[0] + 30, self.color[1] + 30, self.color[2] + 30), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, self.color, (self.x + 2, self.y + 2, self.width - 4, self.height - 4))

        font = pygame.font.SysFont("Arial", 45, bold=True)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))

    def click(self, pos):
        x1, y1 = pos
        return self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height


def redrawWindow(win, game, p):
    win.fill((200, 200, 200))  # Lighter background

    if not game.connected():
        font = pygame.font.SysFont("Arial", 40, bold=True)
        text = font.render("Waiting for Player...", 1, (255, 50, 50))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("Arial", 40, bold=True)
        win.blit(font.render("Your Move", 1, (0, 128, 255)), (80, 200))
        win.blit(font.render("Opponent's Move", 1, (0, 128, 255)), (350, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if p == 0:
                text1 = font.render(move1 if game.p1Went else "Waiting", 1, (0, 0, 0))  # Show Player 1's move
                text2 = font.render("Locked In" if game.p2Went else "Waiting", 1, (0, 0, 0))  # Hide Player 2's move

            else:
                text1 = font.render("Locked In" if game.p1Went else "Waiting", 1, (0, 0, 0))  # Hide Player 1's move
                text2 = font.render(move2 if game.p2Went else "Waiting", 1, (0, 0, 0))  # Show Player 2's move

        win.blit(text1, (100, 350))
        win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 50, 500, (0, 102, 204)), Button("Scissors", 250, 500, (204, 0, 0)), Button("Paper", 450, 500, (0, 204, 102))]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("Arial", 90, bold=True)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (0, 200, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (200, 200, 0))
            else:
                text = font.render("You Lost!", 1, (200, 0, 0))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((200, 200, 200))
        font = pygame.font.SysFont("Arial", 90, bold=True)
        text = font.render("Click to Play", 1, (255, 50, 50))
        win.blit(text, ((width - text.get_width()) // 2, (height - text.get_height()) // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()

main()
