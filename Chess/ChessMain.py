'''
This script is the main script to control all the subscripts
'''

import pygame
import ChessEngine

WIDTH = 1080
HEIGHT = 1080

DIMENSION = 8

SQUARE_SIZE = WIDTH // DIMENSION
MAX_FPS = 15

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

    loadImages()
    running= True
    selectedSquare = ()
    playerClicks = []
    gameOver = False

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                    running = False
            if not gameOver:
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
                                if gameState.whiteKingLocation[0] == 0 or gameState.blackKingLocation[0] == 0:
                                    gameState.eigthRankFinish = True

                        if not moveMade:
                            playerClicks = [selectedSquare]

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gameState.undoMove()
                    moveMade = True
                    gameOver = False
                    gameState.eigthRankFinish = False
                    
                if e.key == pygame.K_r:
                    gameState = ChessEngine.GameState()
                    validMoves = gameState.getValidMoves()
                    selectedSquare = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False

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
        elif gameState.eigthRankFinish:
            gameOver = True
            if gameState.whiteToMove:
                drawText(screen, 'Black king wins the race!')
                print(gameState.blackKingLocation)
            else:
                drawText(screen, 'White king wins the race!')
        
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
