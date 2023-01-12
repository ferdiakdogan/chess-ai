'''
This script is the main script to control all the subscripts
'''

import time
import pygame
import ChessEngine, SmartMoveFinder, AlphaBeta
import sys
from multiprocessing import Process, Queue

WIDTH = 520
HEIGHT = 520

DIMENSION = 8

SQUARE_SIZE = WIDTH // DIMENSION
MAX_FPS = 60

IMAGES = {}

def loadImages():
    IMAGES['wp'] = pygame.transform.scale(pygame.image.load("Chess/images/wp.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGES['bp'] = pygame.transform.scale(pygame.image.load("Chess/images/bp.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGES['wR'] = pygame.transform.scale(pygame.image.load("Chess/images/wR.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGES['bR'] = pygame.transform.scale(pygame.image.load("Chess/images/bR.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGES['wN'] = pygame.transform.scale(pygame.image.load("Chess/images/wN.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGES['bN'] = pygame.transform.scale(pygame.image.load("Chess/images/bN.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGES['wB'] = pygame.transform.scale(pygame.image.load("Chess/images/wB.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGES['bB'] = pygame.transform.scale(pygame.image.load("Chess/images/bB.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGES['wQ'] = pygame.transform.scale(pygame.image.load("Chess/images/wQ.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGES['bQ'] = pygame.transform.scale(pygame.image.load("Chess/images/bQ.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGES['wK'] = pygame.transform.scale(pygame.image.load("Chess/images/wK.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGES['bK'] = pygame.transform.scale(pygame.image.load("Chess/images/bK.png"), (SQUARE_SIZE, SQUARE_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gameState = ChessEngine.GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False
    ai_thinking = False
    moveUndone = False
    move_finder_process = None
    animate = False  # flag variable for when we should animate a move

    loadImages()
    running= True
    selectedSquare = ()
    playerClicks = []
    gameOver = False
    playerOne = True # Human playing white = true, ai is false
    playerTwo = False # Human playing black = true, ai is false

    drawGameState(screen, gameState, validMoves, selectedSquare)

    while running:
        humanTurn = (gameState.whiteToMove and playerOne) or (not gameState.whiteToMove and playerTwo)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                    running = False
            if not gameOver and humanTurn:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    col = location[0]//SQUARE_SIZE
                    row = location[1]//SQUARE_SIZE
                    if selectedSquare == (row, col):
                        selectedSquare = ()
                        playerClicks = []
                    else:
                        selectedSquare = (row, col)
                        playerClicks.append(selectedSquare)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gameState.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gameState.makeMove(validMoves[i])
                                moveMade = True
                                selectedSquare = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [selectedSquare]

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gameState.undoMove()
                    moveMade = True
                    gameOver = False
                    
                if e.key == pygame.K_r:
                    gameState = ChessEngine.GameState()
                    validMoves = gameState.getValidMoves()
                    selectedSquare = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False

        # AI move finder logic
        if not gameOver and not humanTurn:
            aiMove = SmartMoveFinder.findBestMoveAlphaBeta(gameState, validMoves)
            if aiMove is None:
                aiMove = SmartMoveFinder.findRandomMove(validMoves)
            gameState.makeMove(aiMove)
            moveMade = True

        # AlphaBeta move finder
        # if not gameOver and not humanTurn and not moveUndone:
        #     if not ai_thinking:
        #         ai_thinking = True
        #         return_queue = Queue()  # used to pass data between threads
        #         move_finder_process = Process(target=AlphaBeta.findBestMove, args=(gameState, validMoves, return_queue))
        #         move_finder_process.start()

        #     if not move_finder_process.is_alive():
        #         ai_move = return_queue.get()
        #         if ai_move is None:
        #             ai_move = AlphaBeta.findRandomMove(validMoves)
        #         gameState.makeMove(ai_move)
        #         moveMade = True
        #         animate = True
        #         ai_thinking = False

        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False

        drawGameState(screen, gameState, validMoves, selectedSquare)

        if gameState.checkMate:
            gameOver = True
            if gameState.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gameState.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')
        elif gameState.eigthRankFinish == 1:
            if gameState.whiteToMove:
                gameOver = True
                if gameState.blackKingLocation[0] == 0:
                    drawText(screen, 'Black king wins the race!')
                else:
                    drawText(screen, 'White king wins the race!')
        elif gameState.eigthRankFinish == 2:
            gameOver = True
            drawText(screen, 'Stalemate!')
        
        clock.tick(MAX_FPS)
        pygame.display.flip()

def highlightSquares(screen, gameState, validMoves, selectedSquare):
    if selectedSquare != ():
        r, c = selectedSquare
        if gameState.board[r][c][0] == ('w' if gameState.whiteToMove else 'b'):
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(50)
            s.fill(pygame.Color('blue'))
            screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))
            s.fill(pygame.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startColumn == c:
                    screen.blit(s, (move.endColumn*SQUARE_SIZE, move.endRow*SQUARE_SIZE))

def drawGameState(screen, gameState, validMoves, selectedSquare):
    drawBoard(screen)
    highlightSquares(screen, gameState, validMoves, selectedSquare)
    drawPieces(screen, gameState.board)

def drawBoard(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawText(screen, text):
    font = pygame.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, pygame.Color('Black'))
    textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

if __name__ == "__main__":
    main()
