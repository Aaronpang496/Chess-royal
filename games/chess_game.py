import chess
import random

PIECE_VALUES = {
    chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
    chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0,
}

def legal_moves(board):
    return list(board.legal_moves)

def ai_easy(board):
    return random.choice(legal_moves(board))

def ai_medium(board):
    best, best_score = None, -9999
    for m in legal_moves(board):
        score = 0
        if board.is_capture(m):
            victim = board.piece_at(m.to_square)
            if victim:
                score += PIECE_VALUES[victim.piece_type] * 10
        board.push(m)
        if board.is_checkmate():
            score += 100000
        elif board.is_check():
            score += 5
        board.pop()
        # small random tiebreak
        score += random.random()
        if score > best_score:
            best_score, best = score, m
    return best or random.choice(legal_moves(board))

def ai_hard(board, depth=3):
    def evaluate(b):
        if b.is_checkmate():
            return -99999 if b.turn == chess.WHITE else 99999
        s = 0
        for _, p in b.piece_map().items():
            v = PIECE_VALUES[p.piece_type]
            s += v if p.color == chess.WHITE else -v
        return s

    def minimax(b, d, alpha, beta, maximizing):
        if d == 0 or b.is_game_over():
            return evaluate(b)
        moves = list(b.legal_moves)
        # simple move ordering: captures first
        moves.sort(key=lambda m: b.is_capture(m), reverse=True)
        if maximizing:
            best = -10**9
            for m in moves:
                b.push(m)
                best = max(best, minimax(b, d-1, alpha, beta, False))
                b.pop()
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = 10**9
            for m in moves:
                b.push(m)
                best = min(best, minimax(b, d-1, alpha, beta, True))
                b.pop()
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best

    best_move, best_val = None, -10**9
    for m in list(board.legal_moves):
        board.push(m)
        val = minimax(board, depth-1, -10**9, 10**9, False)
        board.pop()
        if val > best_val:
            best_val, best_move = val, m
    return best_move

def get_ai_move(board, difficulty):
    if difficulty == "easy":
        return ai_easy(board)
    if difficulty == "medium":
        return ai_medium(board)
    return ai_hard(board, depth=2)  # depth 3 is slow in pure Python
