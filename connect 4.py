from four import *
import time
import pygame
from pygame.locals import QUIT,MOUSEBUTTONDOWN
import threading

pygame.init()

width = 500
height = 500
SCREEN = (width, height)

screen = pygame.display.set_mode(SCREEN)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

black = (0, 0, 0)
white = (255, 255, 255)
red = (255,50,50)
yellow = (255,255,50)

board = initial_state()

def draw(board):
    board = transpose(board)
    for j in range(6):
        for i in range(7):
            if board[j][i] == 'X':
                pygame.draw.circle(screen, red, (100+50*i, 175+50*j), 20)
            elif board[j][i] == 'O':
                pygame.draw.circle(screen, yellow, (100+50*i, 175+50*j), 20)


continue_code = True
user = None
comp = False

while continue_code:
    for event in pygame.event.get():
        if event.type == QUIT:
            continue_code = False

    screen.fill((100,100,100))

    if user is None:
        # Draw title
        title = largeFont.render("CONNECT 4", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Player 1", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Player 2", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = True
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = False

    else:
        pygame.draw.rect(screen, (50,50,255), pygame.Rect(75,150,350,300), border_radius=20)
        for i in range(7):
            for j in range(6):
                pygame.draw.circle(screen, (100,100,100), (100+50*i, 175+50*j), 20)
        draw(board)

        Player = player(board)

        if terminal(board):
            Winner = winner(board)
            if Winner is None:
                title = f"Game Over: Tie."
            elif Winner == user:
                title = f"You win!."
            else:
                title = f"I win"
        elif user == Player:
            title = f"Your turn"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)
        
        if terminal(board):
            againButton = pygame.Rect(width / 3, 100, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = initial_state()
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == Player and not terminal(board):
            x,y = pygame.mouse.get_pos()
            X = (x-75)//50
            board = result(board, X)

            
        elif user != Player and not terminal(board):
            if comp:
                time.sleep(0.5)
                move = minimax(board)
                board = result(board, move)
                comp = False
            else:
                comp = True
            

    pygame.display.flip()

pygame.quit()


