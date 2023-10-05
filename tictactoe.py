"""
	TicTacToe
		by Adam 
"""

# Imports
import pygame
import os
import math

# Game path 
GAME_PATH = os.getcwd()

# Resolution
RESOLUTION = (600, 700)

# Colors
COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_BOARD = (244, 191, 66)

# Fonts
FONT_SCORE = None

# Images
IMAGE_X = pygame.image.load(GAME_PATH + "/materials/x.png")
IMAGE_X = pygame.transform.scale(IMAGE_X, (120, 120))
IMAGE_O = pygame.image.load(GAME_PATH + "/materials/o.png")
IMAGE_O = pygame.transform.scale(IMAGE_O, (120, 120))
IMAGE_LOGO = pygame.image.load(GAME_PATH + "/materials/logo.png")
IMAGE_LOGO = pygame.transform.scale(IMAGE_LOGO, (460, 150))
IMAGES = {"x": IMAGE_X, "o": IMAGE_O}

# Title of the window
TITLE = "TicTacToe - by Adam"

# Game values
BOARD = [None] * 9
BOARD_AREA = [None] * 9
CURRENT_PLAYER = 1
SCORES = {1: 0, 2: 0}
CURRENT_ANNOUNCEMENT = "Player #1, it's your turn!"
PLAYING = True

def RegisterWin(winner):
    global SCORES
    SCORES[winner] += 1

# Checking if someone won
def GetGamestate() -> bool:
    # Giant if statement to check if a game has been won, extremely stupid.
    if ((BOARD[0] == BOARD[1] == BOARD[2] and BOARD[1] != None)
        or (BOARD[3] == BOARD[4] == BOARD[5] and BOARD[3] != None)
        or (BOARD[6] == BOARD[7] == BOARD[8] and BOARD[6] != None)
        or (BOARD[0] == BOARD[3] == BOARD[6] and BOARD[6] != None)
        or (BOARD[1] == BOARD[4] == BOARD[7] and BOARD[7] != None)
        or (BOARD[2] == BOARD[5] == BOARD[8] and BOARD[8] != None)
        or (BOARD[0] == BOARD[4] == BOARD[8] and BOARD[8] != None)
            or (BOARD[2] == BOARD[4] == BOARD[6] and BOARD[6] != None)):
        return "win"

    # Draw?
    items_filled = 0
    for x in BOARD:
        if (x != None):
            items_filled += 1

    return (items_filled == 9 and "draw" or None)

# Placing on the board
def Place(place):
    # Global so we can edit it
    global BOARD

    # Set
    BOARD[place] = GetCurrentPlayer()

    # Game state
    game_state = GetGamestate()
    if game_state != None:
        global CURRENT_ANNOUNCEMENT
        global PLAYING 

        if (game_state == "win"):
            RegisterWin(CURRENT_PLAYER)
            CURRENT_ANNOUNCEMENT = f"Player #{CURRENT_PLAYER} wins! Click again to restart."
        elif (game_state == "draw"):
            CURRENT_ANNOUNCEMENT = "Draw, no one wins! Click again to restart."

        PLAYING = False

        return
    # Swap players
    ChangePlayer()

# Getting current player
def GetCurrentPlayer(pl=False) -> str:
    return ((pl or CURRENT_PLAYER) == 1 and "x" or "o")

# Changing player
def ChangePlayer():
    global CURRENT_PLAYER
    global CURRENT_ANNOUNCEMENT

    CURRENT_PLAYER = (CURRENT_PLAYER == 1 and 2 or 1)
    CURRENT_ANNOUNCEMENT = f"Player #{CURRENT_PLAYER}, it's your turn!"

# Mouse Click
def MouseClick(pos):
    # xPos, yPos
    xPos, yPos = pos

    global PLAYING
    global BOARD
    if not PLAYING: 
        PLAYING = True
        BOARD = [None] * 9
        ChangePlayer()
        return

    # Did we click a board place
    clicked = None
    for x, place in enumerate(BOARD_AREA):
        startx, starty, endx, endy = place
        if (xPos >= startx) and (xPos <= endx) and (yPos >= starty) and (yPos <= endy):
            clicked = x

    # if (0) -> False, that's why
    if (clicked != None) and (BOARD[clicked] == None):
        Place(clicked)

def drawText(surface, text, font, xPos, yPos, colour=(0,0,0), align = False):
    textSurface = font.render(text, True, colour)
    adjustedX, adjustedY = 0, 0

    if align:
        surfaceRect = textSurface.get_rect()
        if align == 'right':
            adjustedX -= surfaceRect.width
        elif align == 'centre':
            adjustedX -= math.floor(surfaceRect.width / 2)

    surface.blit(textSurface, (xPos + adjustedX, yPos))
    return textSurface
# Draw
def Render(surface):
    # Reset last draw
    surface.fill(COLOUR_WHITE)
    global BOARD_AREA

    # The board
    def draw_board(xOffset, yOffset):
        for line in range(3):
            for x in range(3):
                xPos = xOffset + (155 * x)
                yPos = yOffset + (155 * line)
                state = BOARD[x + (3 * line)]
                BOARD_AREA[x + (3 * line)] = (xPos, yPos, xPos + 152, yPos + 152)

                pygame.draw.rect(surface, COLOUR_BOARD, (xPos, yPos, 152, 152))
                if state in ("x", "o"):
                    surface.blit(IMAGES[state], (xPos + 16, yPos + 16))

    # Draw our board
    board_size = (150 * 3) + 10
    draw_board(RESOLUTION[0] / 2 - board_size / 2,
               RESOLUTION[1] / 2 - board_size / 2)

    # logo
    # surface.blit(IMAGE_LOGO, (50, 0))

    s = drawText(surface, "Player 1", FONT_SCORE, 30, 30, COLOUR_BLACK)
    drawText(surface, str(SCORES[1]), FONT_SCORE, 30 + math.floor(s.get_rect().width / 2), 56, COLOUR_BLACK, align = 'centre')
    s = drawText(surface, "Player 2", FONT_SCORE, RESOLUTION[0] - 30, 30, COLOUR_BLACK, align = 'right')
    drawText(surface, str(SCORES[2]), FONT_SCORE, RESOLUTION[0] - (30 + math.floor(s.get_rect().width / 2)), 56, COLOUR_BLACK, align = 'centre')

    drawText(surface, CURRENT_ANNOUNCEMENT, FONT_SCORE, RESOLUTION[0] // 2, RESOLUTION[1] - 60, COLOUR_BLACK, align = 'centre')

    # Update
    pygame.display.update()

# On tick
inClick = False
def Tick(surface):
    global inClick 

    # Check our events
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            quit()
            break 

        # Mouse Press
        mousePos = pygame.mouse.get_pos()
        p1, p2, p3 = pygame.mouse.get_pressed()
        
        if p1 and not inClick:
            inClick = True
            MouseClick(mousePos)
        elif not p1 and inClick:
            inClick = False 

    Render(surface)

# Main function
def main() -> None:
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption(TITLE)

    # Get our surface
    surface = pygame.display.set_mode(RESOLUTION)

    global FONT_SCORE 
    FONT_SCORE = pygame.font.SysFont("verdana", 20)

    # Main loop / onTick
    while True:
        Tick(surface)


# Run code
if __name__ == "__main__":
    main()
