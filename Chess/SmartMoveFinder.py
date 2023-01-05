import random

pieceScore = {"K": -1, "Q": 10, "R":5, "B": 3, "N": 3, "p": 1}
WIN = 1000
DRAW = 0

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gameState, validMoves):
    turnMultiplier = 1 if gameState.whiteToMove else -1
    minMaxScore = WIN
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gameState.makeMove(playerMove)
        opponentMoves = gameState.getValidMoves()
        if  gameState.eigthRankFinish:
            opponentMaxScore = - WIN
        elif gameState.staleMate:
            opponentMaxScore = DRAW
        else:
            opponentMaxScore = -WIN
            for opponentMove in opponentMoves:
                gameState.makeMove(opponentMove)
                gameState.getValidMoves()
                if gameState.eigthRankFinish:
                    score = WIN
                elif gameState.staleMate:
                    score = DRAW
                else:
                    score = - turnMultiplier * scoreMaterial(gameState.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score 
                gameState.undoMove()
        if opponentMaxScore < minMaxScore:
            minMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gameState.undoMove()
    return bestPlayerMove

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score