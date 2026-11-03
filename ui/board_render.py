import chess
import chess.svg
import streamlit.components.v1 as components

CHESS_SIZE = 480

def render_chess(board, last_move=None, legal_targets=None, selected_square=None):
    """
    legal_targets: list of chess.Square to show as dots (from python-chess legal moves
                   for the selected piece).
    selected_square: chess.Square currently highlighted.
    """
    arrows = []
    fill = {}
    if selected_square is not None:
        fill[selected_square] = "#a5c9a5"

    svg = chess.svg.board(
        board,
        size=CHESS_SIZE,
        lastmove=last_move,
        arrows=arrows,
        fill=fill,
        colors={"square light": "#f0d9b5", "square dark": "#b58863", "margin": "#ffffff"},
    )

    # Inject dot overlays on top of the SVG by appending circles to the <svg> element
    if legal_targets:
        extra = []
        for sq in legal_targets:
            file = chess.square_file(sq)
            rank = chess.square_rank(sq)
            # chess.svg uses 45px squares with margin (default margin ~20)
            margin = 20
            sq_size = CHESS_SIZE / 8
            x = margin + file * sq_size + sq_size / 2
            # flipped: rank 0 at bottom (default)
            y = margin + (7 - rank) * sq_size + sq_size / 2
            is_capture = board.piece_at(sq) is not None
            if is_capture:
                extra.append(
                    f"<circle cx='{x}' cy='{y}' r='{sq_size*0.42}' "
                    f"fill='none' stroke='#2e7d32' stroke-width='4'/>"
                )
            else:
                extra.append(
                    f"<circle cx='{x}' cy='{y}' r='{sq_size*0.16}' fill='#2e7d32' opacity='0.75'/>"
                )
        # insert before closing </svg>
        svg = svg.replace("</svg>", "".join(extra) + "</svg>")

    components.html(
        f"<div style='display:flex;justify-content:center'>{svg}</div>",
        height=CHESS_SIZE + 30,
    )


# ---------- 象棋 ----------
XQ_LABELS = {
    "rK":"帥","rA":"仕","rE":"相","rH":"馬","rR":"車","rC":"炮","rP":"兵",
    "bK":"將","bA":"士","bE":"象","bH":"馬","bR":"車","bC":"炮","bP":"卒",
}

def render_xiangqi(board, highlight=None):
    cell, pad = 56, 30
    w = pad*2 + cell*8
    h = pad*2 + cell*9
    p = [f"<svg width='{w}' height='{h}' style='background:#e8c88f;border-radius:6px'>"]
    for r in range(10):
        y = pad + r*cell
        p.append(f"<line x1='{pad}' y1='{y}' x2='{pad+8*cell}' y2='{y}' stroke='#3a2a10' stroke-width='1.5'/>")
    for c in range(9):
        x = pad + c*cell
        if c in (0, 8):
            p.append(f"<line x1='{x}' y1='{pad}' x2='{x}' y2='{pad+9*cell}' stroke='#3a2a10' stroke-width='1.5'/>")
        else:
            p.append(f"<line x1='{x}' y1='{pad}' x2='{x}' y2='{pad+4*cell}' stroke='#3a2a10' stroke-width='1.5'/>")
            p.append(f"<line x1='{x}' y1='{pad+5*cell}' x2='{x}' y2='{pad+9*cell}' stroke='#3a2a10' stroke-width='1.5'/>")
    for (r0, c0) in [(0,3),(7,3)]:
        x1 = pad + c0*cell; y1 = pad + r0*cell
        x2 = x1 + 2*cell; y2 = y1 + 2*cell
        p.append(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='#3a2a10' stroke-width='1.5'/>")
        p.append(f"<line x1='{x2}' y1='{y1}' x2='{x1}' y2='{y2}' stroke='#3a2a10' stroke-width='1.5'/>")
    p.append(f"<text x='{pad+2*cell}' y='{pad+4.65*cell}' font-size='20' fill='#3a2a10'>楚 河</text>")
    p.append(f"<text x='{pad+5.5*cell}' y='{pad+4.65*cell}' font-size='20' fill='#3a2a10'>漢 界</text>")
    for r in range(10):
        for c in range(9):
            piece = board[r][c]
            if not piece: continue
            cx = pad + c*cell; cy = pad + r*cell
            fill = "#fff3d6" if piece["color"] == "r" else "#f0e0b8"
            stroke = "#b22222" if piece["color"] == "r" else "#1a1a1a"
            txt = "#b22222" if piece["color"] == "r" else "#1a1a1a"
            p.append(f"<circle cx='{cx}' cy='{cy}' r='{cell*0.42}' fill='{fill}' stroke='{stroke}' stroke-width='2'/>")
            p.append(f"<text x='{cx}' y='{cy+7}' text-anchor='middle' font-size='24' font-weight='bold' fill='{txt}'>{XQ_LABELS[piece['color']+piece['type']]}</text>")
    if highlight:
        (hr, hc) = highlight
        p.append(f"<circle cx='{pad+hc*cell}' cy='{pad+hr*cell}' r='{cell*0.48}' fill='none' stroke='#00aa00' stroke-width='3'/>")
    p.append("</svg>")
    components.html("".join(p), height=h + 20)


# ---------- Go ----------
def render_go(board, highlight=None):
    size, cell, pad = 9, 46, 30
    w = pad*2 + cell*(size-1)
    p = [f"<svg width='{w}' height='{w}' style='background:#dcb35c;border-radius:6px'>"]
    for i in range(size):
        x = pad + i*cell
        p.append(f"<line x1='{pad}' y1='{x}' x2='{pad+cell*(size-1)}' y2='{x}' stroke='#3a2a10' stroke-width='1.2'/>")
        p.append(f"<line x1='{x}' y1='{pad}' x2='{x}' y2='{pad+cell*(size-1)}' stroke='#3a2a10' stroke-width='1.2'/>")
    for (r, c) in [(2,2),(2,6),(6,2),(6,6),(4,4)]:
        p.append(f"<circle cx='{pad+c*cell}' cy='{pad+r*cell}' r='3' fill='#3a2a10'/>")
    for r in range(size):
        for c in range(size):
            s = board[r][c]
            if s:
                cx = pad + c*cell; cy = pad + r*cell
                fill = "#111" if s == "b" else "#fafafa"
                stroke = "#000" if s == "b" else "#888"
                p.append(f"<circle cx='{cx}' cy='{cy}' r='{cell*0.45}' fill='{fill}' stroke='{stroke}' stroke-width='1'/>")
    if highlight:
        (hr, hc) = highlight
        p.append(f"<circle cx='{pad+hc*cell}' cy='{pad+hr*cell}' r='{cell*0.5}' fill='none' stroke='#00aa00' stroke-width='3'/>")
    p.append("</svg>")
    components.html("".join(p), height=w + 20)
