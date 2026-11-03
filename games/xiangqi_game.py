# Board representation: 10x9 grid, None = empty.
# Each piece: {"type": "K/A/E/H/R/C/P", "color": "r" or "b"}
# Red moves first (bottom of board, row 9 = red home).

PIECE_VALUES = {"K": 1000, "R": 9, "C": 4.5, "H": 4, "E": 2, "A": 2, "P": 1}

def initial_board():
    b = [[None]*9 for _ in range(10)]
    back = ["R","H","E","A","K","A","E","H","R"]
    for c in range(9):
        b[0][c] = {"type": back[c], "color": "b"}
        b[9][c] = {"type": back[c], "color": "r"}
    b[2][1] = {"type":"C","color":"b"}; b[2][7] = {"type":"C","color":"b"}
    b[7][1] = {"type":"C","color":"r"}; b[7][7] = {"type":"C","color":"r"}
    for c in [0,2,4,6,8]:
        b[3][c] = {"type":"P","color":"b"}
        b[6][c] = {"type":"P","color":"r"}
    return b

def clone(board):
    return [[dict(p) if p else None for p in row] for row in board]

def in_board(r, c):
    return 0 <= r < 10 and 0 <= c < 9

def in_palace(r, c, color):
    if color == "r":
        return 7 <= r <= 9 and 3 <= c <= 5
    return 0 <= r <= 2 and 3 <= c <= 5

def gen_piece_moves(board, r, c):
    p = board[r][c]
    if not p:
        return []
    t, color = p["type"], p["color"]
    moves = []

    def add(rr, cc):
        if not in_board(rr, cc):
            return False
        target = board[rr][cc]
        if target and target["color"] == color:
            return False
        moves.append((rr, cc))
        return target is None  # True = continue sliding

    if t == "K":
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            rr, cc = r+dr, c+dc
            if in_palace(rr, cc, color) and (not board[rr][cc] or board[rr][cc]["color"] != color):
                moves.append((rr, cc))
    elif t == "A":
        for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
            rr, cc = r+dr, c+dc
            if in_palace(rr, cc, color) and (not board[rr][cc] or board[rr][cc]["color"] != color):
                moves.append((rr, cc))
    elif t == "E":
        for dr, dc in [(-2,-2),(-2,2),(2,-2),(2,2)]:
            rr, cc = r+dr, c+dc
            if not in_board(rr, cc):
                continue
            # elephant cannot cross river
            if color == "r" and rr < 5: continue
            if color == "b" and rr > 4: continue
            mid = board[r+dr//2][c+dc//2]
            if mid:  # blocked eye
                continue
            if not board[rr][cc] or board[rr][cc]["color"] != color:
                moves.append((rr, cc))
    elif t == "H":
        # horse with blocking leg
        for dr, dc, lr, lc in [(-2,-1,-1,0),(-2,1,-1,0),(2,-1,1,0),(2,1,1,0),
                                (-1,-2,0,-1),(1,-2,0,-1),(-1,2,0,1),(1,2,0,1)]:
            if not in_board(r+lr, c+lc): continue
            if board[r+lr][c+lc]:  # leg blocked
                continue
            rr, cc = r+dr, c+dc
            if in_board(rr, cc) and (not board[rr][cc] or board[rr][cc]["color"] != color):
                moves.append((rr, cc))
    elif t == "R":
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            rr, cc = r+dr, c+dc
            while in_board(rr, cc):
                if board[rr][cc] is None:
                    moves.append((rr, cc))
                else:
                    if board[rr][cc]["color"] != color:
                        moves.append((rr, cc))
                    break
                rr += dr; cc += dc
    elif t == "C":
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            rr, cc = r+dr, c+dc
            # phase 1: empty squares
            while in_board(rr, cc) and board[rr][cc] is None:
                moves.append((rr, cc))
                rr += dr; cc += dc
            # phase 2: after first piece (screen), next piece of enemy = capture
            rr += dr; cc += dc
            while in_board(rr, cc):
                if board[rr][cc] is not None:
                    if board[rr][cc]["color"] != color:
                        moves.append((rr, cc))
                    break
                rr += dr; cc += dc
    elif t == "P":
        forward = -1 if color == "r" else 1
        rr, cc = r+forward, c
        if in_board(rr, cc) and (not board[rr][cc] or board[rr][cc]["color"] != color):
            moves.append((rr, cc))
        # sideways after crossing river
        crossed = (color == "r" and r <= 4) or (color == "b" and r >= 5)
        if crossed:
            for dc in (-1, 1):
                rr, cc = r, c+dc
                if in_board(rr, cc) and (not board[rr][cc] or board[rr][cc]["color"] != color):
                    moves.append((rr, cc))
    return moves

def find_king(board, color):
    for r in range(10):
        for c in range(9):
            p = board[r][c]
            if p and p["type"] == "K" and p["color"] == color:
                return (r, c)
    return None

def kings_face(board):
    """Flying-general rule: kings cannot face each other on same file with no pieces between."""
    rk = find_king(board, "r"); bk = find_king(board, "b")
    if not rk or not bk or rk[1] != bk[1]:
        return False
    c = rk[1]
    lo, hi = min(rk[0], bk[0]), max(rk[0], bk[0])
    for r in range(lo+1, hi):
        if board[r][c]:
            return False
    return True

def legal_moves_for(board, color):
    out = []
    for r in range(10):
        for c in range(9):
            p = board[r][c]
            if p and p["color"] == color:
                for (rr, cc) in gen_piece_moves(board, r, c):
                    nb = clone(board)
                    nb[rr][cc] = nb[r][c]
                    nb[r][c] = None
                    if kings_face(nb):
                        continue
                    out.append(((r, c), (rr, cc)))
    return out

def apply_move(board, move):
    (r, c), (rr, cc) = move
    nb = clone(board)
    nb[rr][cc] = nb[r][c]
    nb[r][c] = None
    return nb

def is_check(board, color):
    king = find_king(board, color)
    if not king:
        return True
    enemy = "b" if color == "r" else "r"
    for r in range(10):
        for c in range(9):
            p = board[r][c]
            if p and p["color"] == enemy:
                if king in gen_piece_moves(board, r, c):
                    return True
    return kings_face(board)

def is_checkmate_or_stalemate(board, color):
    """Return 'checkmate' if in check with no moves, 'stalemate' if not in check with no moves, None otherwise."""
    moves = legal_moves_for(board, color)
    if moves:
        return None
    return "checkmate" if is_check(board, color) else "stalemate"

def static_eval(board, for_color):
    s = 0
    for r in range(10):
        for c in range(9):
            p = board[r][c]
            if p:
                v = PIECE_VALUES[p["type"]]
                s += v if p["color"] == for_color else -v
    return s

def get_ai_move(board, color, difficulty):
    import random
    moves = legal_moves_for(board, color)
    if not moves:
        return None
    if difficulty == "easy":
        return random.choice(moves)

    enemy = "b" if color == "r" else "r"
    scored = []
    for m in moves:
        nb = apply_move(board, m)
        s = static_eval(nb, color)
        # prefer checkmate
        if is_checkmate_or_stalemate(nb, enemy) == "checkmate":
            s += 10000
        scored.append((s, m))

    if difficulty == "medium":
        best = max(s for s, _ in scored)
        return random.choice([m for s, m in scored if s == best])

    # hard: shallow 2-ply
    best_val, best_move = -10**9, scored[0][1]
    for s1, m1 in scored:
        nb = apply_move(board, m1)
        if is_checkmate_or_stalemate(nb, enemy) == "checkmate":
            return m1
        enemy_moves = legal_moves_for(nb, enemy)
        if not enemy_moves:
            return m1
        # worst case for us after enemy best reply
        worst = 10**9
        for em in enemy_moves:
            nb2 = apply_move(nb, em)
            worst = min(worst, static_eval(nb2, color))
        val = s1 + 0.5 * worst
        if val > best_val:
            best_val, best_move = val, m1
    return best_move

def analyze_xiangqi_moves(history, player_color, threshold=1.5):
    """history: list of {"from":(r,c),"to":(r,c),"board":serialized}"""
    mistakes = []
    for i, h in enumerate(history):
        if h.get("color") != player_color:
            continue
        before = h["board_before"]
        after = h["board_after"]
        loss = static_eval(before, player_color) - static_eval(after, player_color)
        if loss >= threshold:
            mistakes.append({
                "move_no": i // 2 + 1,
                "move": f"{h['from']}->{h['to']}",
                "material_loss": round(loss, 1),
                "severity": "blunder" if loss >= 3 else "mistake",
            })
    return mistakes
