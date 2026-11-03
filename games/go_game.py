import random
from copy import deepcopy

SIZE = 9

def initial_board():
    return [[None]*SIZE for _ in range(SIZE)]

def clone(b):
    return [row[:] for row in b]

def neighbors(r, c):
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        rr, cc = r+dr, c+dc
        if 0 <= rr < SIZE and 0 <= cc < SIZE:
            yield rr, cc

def group_and_liberties(board, r, c):
    color = board[r][c]
    if not color:
        return set(), set()
    stack = [(r, c)]
    group, liberties = set(), set()
    while stack:
        cr, cc = stack.pop()
        if (cr, cc) in group:
            continue
        group.add((cr, cc))
        for nr, nc in neighbors(cr, cc):
            if board[nr][nc] is None:
                liberties.add((nr, nc))
            elif board[nr][nc] == color and (nr, nc) not in group:
                stack.append((nr, nc))
    return group, liberties

def play_move(board, r, c, color):
    """Return (new_board, ok, ko_point)."""
    if board[r][c] is not None:
        return board, False, None
    nb = clone(board)
    nb[r][c] = color
    enemy = "w" if color == "b" else "b"
    captured_any = False
    for nr, nc in neighbors(r, c):
        if nb[nr][nc] == enemy:
            grp, libs = group_and_liberties(nb, nr, nc)
            if not libs:
                captured_any = True
                for (gr, gc) in grp:
                    nb[gr][gc] = None
    grp, libs = group_and_liberties(nb, r, c)
    if not libs:
        return board, False, None  # suicide
    # simple ko: if exactly 1 stone captured and resulting group size 1 with 1 liberty
    ko = None
    if captured_any and len(grp) == 1 and len(libs) == 1:
        ko = (r, c)
    return nb, True, ko

def legal_moves(board, color):
    out = []
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] is None:
                _, ok, _ = play_move(board, r, c, color)
                if ok:
                    out.append((r, c))
    return out

def score_board(board):
    """Chinese-style area scoring approximation: stones + surrounded empty."""
    black, white = 0, 0
    visited = set()
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == "b":
                black += 1
            elif board[r][c] == "w":
                white += 1
            elif board[r][c] is None and (r, c) not in visited:
                grp, border = set(), set()
                stack = [(r, c)]
                while stack:
                    cr, cc = stack.pop()
                    if (cr, cc) in grp:
                        continue
                    grp.add((cr, cc))
                    for nr, nc in neighbors(cr, cc):
                        if board[nr][nc] is None and (nr, nc) not in grp:
                            stack.append((nr, nc))
                        elif board[nr][nc]:
                            border.add(board[nr][nc])
                visited |= grp
                if border == {"b"}:
                    black += len(grp)
                elif border == {"w"}:
                    white += len(grp)
    return black, white

def ai_move(board, color, difficulty):
    moves = legal_moves(board, color)
    if not moves:
        return None
    if difficulty == "easy":
        return random.choice(moves)

    enemy = "w" if color == "b" else "b"

    def eval_after(r, c):
        nb, ok, _ = play_move(board, r, c, color)
        if not ok:
            return -999
        # simple: captures + own liberties
        score = 0
        for nr, nc in neighbors(r, c):
            if board[nr][nc] == enemy:
                grp, libs = group_and_liberties(nb, nr, nc)
                score -= len(libs)  # enemy weakened
        grp, libs = group_and_liberties(nb, r, c)
        score += len(libs) * 0.5
        # prefer center early
        score -= abs(r - 4) * 0.1 + abs(c - 4) * 0.1
        return score

    scored = [(eval_after(r, c), (r, c)) for (r, c) in moves]
    if difficulty == "medium":
        best = max(s for s, _ in scored)
        return random.choice([m for s, m in scored if s == best])

    # hard: 1-ply lookahead
    best_val, best_move = -10**9, scored[0][1]
    for s1, m1 in scored:
        nb, ok, _ = play_move(board, m1[0], m1[1], color)
        if not ok:
            continue
        enemy_moves = legal_moves(nb, enemy)
        if not enemy_moves:
            return m1
        worst = 10**9
        for em in enemy_moves[:30]:  # cap for speed
            nb2, ok2, _ = play_move(nb, em[0], em[1], enemy)
            if ok2:
                worst = min(worst, s1 - eval_after(em[0], em[1]))
        if worst > best_val:
            best_val, best_move = worst, m1
    return best_move
