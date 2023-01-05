import random

pieceScore = {"K": 0, "Q": 10, "R":5, "B": 3, "N": 3, "p": 1}
WIN = 1000
DRAW = 0
DEPTH = 1

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


def findBestMoveMinMax(gameState, validMoves):
    global nextMove
    nextMove = None
    findMoveMinMax2(gameState, validMoves, DEPTH, 1 if gameState.whiteToMove else -1)
    return nextMove

def findMoveMinMax(gameState, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreBoard(gameState)
    
    if whiteToMove:
        maxScore = - WIN
        for move in validMoves:
            gameState.makeMove(move)
            nextMoves = gameState.getValidMoves()
            score = findMoveMinMax(gameState, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gameState.undoMove()
        return maxScore
    else:
        minScore = - WIN
        for move in validMoves:
            gameState.makeMove(move)
            nextMoves = gameState.getValidMoves()
            score = findMoveMinMax(gameState, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gameState.undoMove()
        return minScore

def findMoveMinMax2(gameState, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gameState)
    
    maxScore = - WIN

    random.shuffle(validMoves)

    for move in validMoves:
        gameState.makeMove(move)
        nextMoves = gameState.getValidMoves()
        score = -findMoveMinMax2(gameState, nextMoves, depth - 1, - turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        
        gameState.undoMove()
    return maxScore



def scoreBoard(gameState):
    if gameState.eigthRankFinish:
        if gameState.whiteToMove:
            return -WIN
        else:
            return WIN
    elif gameState.staleMate:
        return DRAW

    score = 0
    for row in gameState.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    score += 1 * (7 - gameState.whiteKingLocation[0])
    score -= 1 * (7 - gameState.blackKingLocation[0])
    return score

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score