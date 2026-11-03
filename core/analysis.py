import chess

PIECE_VALUES = {
    chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
    chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0,
}

def _static_eval(board):
    score = 0
    for piece in board.piece_map().values():
        v = PIECE_VALUES[piece.piece_type]
        score += v if piece.color == chess.WHITE else -v
    return score

def analyze_chess_moves(history, player_color, threshold=1.5):
    mistakes = []
    good_moves = []
    prev_fen = chess.STARTING_FEN
    
    for i, h in enumerate(history):
        b_before = chess.Board(prev_fen)
        b_after = chess.Board(h["fen"])
        
        if b_before.turn == player_color:
            before = _static_eval(b_before)
            after = _static_eval(b_after)
            # Calculate gain/loss from player's perspective
            loss = (before - after) if player_color == chess.WHITE else (after - before)
            gain = -loss
            
            move_num = i // 2 + 1
            
            if loss >= threshold:
                mistakes.append({
                    "Move": move_num,
                    "Your Move": h["san"],
                    "Material Lost": round(loss, 1),
                    "Type": "Blunder" if loss >= 3 else "Mistake"
                })
            elif gain >= 3: # Good capture
                good_moves.append({
                    "Move": move_num,
                    "Your Move": h["san"],
                    "Material Won": round(gain, 1),
                    "Type": "Good Capture"
                })
                
        prev_fen = h["fen"]
        
    return mistakes, good_moves
