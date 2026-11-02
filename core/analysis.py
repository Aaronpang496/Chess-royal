import chess

PIECE_VALUES = {
    chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
    chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0,
}

def _static_eval(board: chess.Board) -> int:
    score = 0
    for _, piece in board.piece_map().items():
        v = PIECE_VALUES[piece.piece_type]
        score += v if piece.color == chess.WHITE else -v
    return score

def analyze_chess_moves(history, player_color, threshold=1.5):
    """
    history: list of dicts {"uci","san","fen"} — fen AFTER the move.
    player_color: chess.WHITE or chess.BLACK
    Returns list of mistake dicts.
    """
    mistakes = []
    prev_fen = chess.STARTING_FEN
    for i, h in enumerate(history):
        b_before = chess.Board(prev_fen)
        b_after = chess.Board(h["fen"])
        if b_before.turn == player_color:
            before = _static_eval(b_before)
            after = _static_eval(b_after)
            loss = (before - after) if player_color == chess.WHITE else (after - before)
            if loss >= threshold:
                mistakes.append({
                    "move_no": i // 2 + 1,
                    "your_move": h["san"],
                    "material_loss": round(loss, 1),
                    "severity": "blunder" if loss >= 3 else "mistake",
                })
        prev_fen = h["fen"]
    return mistakes
