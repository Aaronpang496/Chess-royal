import chess
import chess.svg
import streamlit.components.v1 as components

CHESS_SIZE = 480

def render_chess(board: chess.Board, last_move=None):
    svg = chess.svg.board(
        board,
        size=CHESS_SIZE,
        lastmove=last_move,
        colors={
            "square light": "#f0d9b5",
            "square dark": "#b58863",
            "margin": "#ffffff",
        },
    )
    components.html(
        f"<div style='display:flex;justify-content:center'>{svg}</div>",
        height=CHESS_SIZE + 20,
    )

# ---------- 象棋 SVG ----------
XQ_LABELS = {
    "rK":"帥","rA":"仕","rE":"相","rH":"馬","rR":"車","rC":"炮","rP":"兵",
    "bK":"將","bA":"士","bE":"象","bH":"馬","bR":"車","bC":"炮","bP":"卒",
}

def render_xiangqi(board, highlight=None):
    cell = 56
    pad = 30
    w = pad*2 + cell*8
    h = pad*2 + cell*9
    parts = [f"<svg width='{w}' height='{h}' style='background:#e8c88f;border-radius:6px'>"]
    # grid
    for r in range(10):
        y = pad + r*cell
        parts.append(f"<line x1='{pad}' y1='{y}' x2='{pad+8*cell}' y2='{y}' stroke='#3a2a10' stroke-width='1.5'/>")
    for c in range(9):
        x = pad + c*cell
        if c == 0 or c == 8:
            parts.append(f"<line x1='{x}' y1='{pad}' x2='{x}' y2='{pad+9*cell}' stroke='#3a2a10' stroke-width='1.5'/>")
        else:
            parts.append(f"<line x1='{x}' y1='{pad}' x2='{x}' y2='{pad+4*cell}' stroke='#3a2a10' stroke-width='1.5'/>")
            parts.append(f"<line x1='{x}' y1='{pad+5*cell}' x2='{x}' y2='{pad+9*cell}' stroke='#3a2a10' stroke-width='1.5'/>")
    # palace diagonals
    for (r0, c0) in [(0,3),(7,3)]:
        x1 = pad + c0*cell; y1 = pad + r0*cell
        x2 = x1 + 2*cell; y2 = y1 + 2*cell
        parts.append(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='#3a2a10' stroke-width='1.5'/>")
        parts.append(f"<line x1='{x2}' y1='{y1}' x2='{x1}' y2='{y2}' stroke='#3a2a10' stroke-width='1.5'/>")
    # river text
    parts.append(f"<text x='{pad+2*cell}' y='{pad+4.65*cell}' font-size='20' fill='#3a2a10'>楚 河</text>")
    parts.append(f"<text x='{pad+5.5*cell}' y='{pad+4.65*cell}' font-size='20' fill='#3a2a10'>漢 界</text>")
    # pieces
    for r in range(10):
        for c in range(9):
            p = board[r][c]
            if not p: continue
            cx = pad + c*cell
            cy = pad + r*cell
            fill = "#fff3d6" if p["color"] == "r" else "#f0e0b8"
            stroke = "#b22222" if p["color"] == "r" else "#1a1a1a"
            txt_color = "#b22222" if p["color"] == "r" else "#1a1a1a"
            parts.append(f"<circle cx='{cx}' cy='{cy}' r='{cell*0.42}' fill='{fill}' stroke='{stroke}' stroke-width='2'/>")
            label = XQ_LABELS[p["color"] + p["type"]]
            parts.append(f"<text x='{cx}' y='{cy+7}' text-anchor='middle' font-size='24' font-weight='bold' fill='{txt_color}'>{label}</text>")
    if highlight:
        (hr, hc) = highlight
        parts.append(f"<circle cx='{pad+hc*cell}' cy='{pad+hr*cell}' r='{cell*0.48}' fill='none' stroke='#00aa00' stroke-width='3'/>")
    parts.append("</svg>")
    components.html("".join(parts), height=h + 20)

# ---------- Go SVG ----------
def render_go(board, highlight=None):
    size = 9
    cell = 46
    pad = 30
    w = pad*2 + cell*(size-1)
    h = w
    parts = [f"<svg width='{w}' height='{h}' style='background:#dcb35c;border-radius:6px'>"]
    for i in range(size):
        x = pad + i*cell
        parts.append(f"<line x1='{pad}' y1='{x}' x2='{pad+cell*(size-1)}' y2='{x}' stroke='#3a2a10' stroke-width='1.2'/>")
        parts.append(f"<line x1='{x}' y1='{pad}' x2='{x}' y2='{pad+cell*(size-1)}' stroke='#3a2a10' stroke-width='1.2'/>")
    for (r, c) in [(2,2),(2,6),(6,2),(6,6),(4,4)]:
        parts.append(f"<circle cx='{pad+c*cell}' cy='{pad+r*cell}' r='3' fill='#3a2a10'/>")
    for r in range(size):
        for c in range(size):
            stone = board[r][c]
            if stone:
                cx = pad + c*cell
                cy = pad + r*cell
                fill = "#111" if stone == "b" else "#fafafa"
                stroke = "#000" if stone == "b" else "#888"
                parts.append(f"<circle cx='{cx}' cy='{cy}' r='{cell*0.45}' fill='{fill}' stroke='{stroke}' stroke-width='1'/>")
    if highlight:
        (hr, hc) = highlight
        parts.append(f"<circle cx='{pad+hc*cell}' cy='{pad+hr*cell}' r='{cell*0.5}' fill='none' stroke='#00aa00' stroke-width='3'/>")
    parts.append("</svg>")
    components.html("".join(parts), height=h + 20)
