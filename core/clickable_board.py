import streamlit as st
import streamlit.components.v1 as components
import json
import chess

def clickable_chess_board(board, selected, legal_targets, flipped=False, key="board"):
    # Convert board to 8x8 char grid
    grid = [[""] * 8 for _ in range(8)]
    for sq, piece in board.piece_map().items():
        r = 7 - chess.square_rank(sq)
        c = chess.square_file(sq)
        grid[r][c] = piece.symbol()
        
    board_json = json.dumps(grid)
    selected_json = json.dumps(selected or "")
    targets_json = json.dumps([chess.square_name(s) for s in legal_targets])
    flipped_js = "true" if flipped else "false"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; background: transparent; }}
        .board {{ display: grid; grid-template-columns: repeat(8, 1fr); width: 100%; max-width: 400px; aspect-ratio: 1; border: 2px solid #333; border-radius: 4px; overflow: hidden; }}
        .square {{ position: relative; display: flex; align-items: center; justify-content: center; font-size: clamp(24px, 8vw, 40px); cursor: pointer; user-select: none; -webkit-user-select: none; -webkit-tap-highlight-color: transparent; }}
        .light {{ background-color: #f0d9b5; }}
        .dark {{ background-color: #b58863; }}
        .selected {{ background-color: #a5c9a5 !important; }}
        .dot {{ width: 20%; height: 20%; background-color: #2e7d32; border-radius: 50%; position: absolute; opacity: 0.8; }}
        .capture-ring {{ width: 80%; height: 80%; border: 4px solid #2e7d32; border-radius: 50%; position: absolute; box-sizing: border-box; }}
        .pieces {{ font-family: "Arial Unicode MS", "Segoe UI Symbol", sans-serif; line-height: 1; }}
    </style>
    </head>
    <body>
    <div class="board" id="board"></div>
    
    <script>
        const boardData = {board_json};
        const selectedSq = {selected_json};
        const legalTargets = {targets_json};
        const flipped = {flipped_js};
        
        const pieceMap = {{
            'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚',
            'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔'
        }};
        
        const files = ['a','b','c','d','e','f','g','h'];
        const ranks = ['8','7','6','5','4','3','2','1'];
        
        let rows = [0,1,2,3,4,5,6,7];
        let cols = [0,1,2,3,4,5,6,7];
        if (flipped) {{
            rows = [7,6,5,4,3,2,1,0];
            cols = [7,6,5,4,3,2,1,0];
        }}

        const boardEl = document.getElementById('board');
        
        rows.forEach(r => {{
            cols.forEach(c => {{
                const sq = files[c] + ranks[r];
                const isLight = (r + c) % 2 === 0;
                const piece = boardData[r][c];
                const isSelected = selectedSq === sq;
                const isTarget = legalTargets.includes(sq);
                const isCapture = isTarget && piece !== "";
                
                const div = document.createElement('div');
                div.className = `square ${{isLight ? 'light' : 'dark'}} ${{isSelected ? 'selected' : ''}}`;
                
                // On click, append query param to parent URL
                div.onclick = () => {{
                    const url = new URL(window.parent.location.href);
                    url.searchParams.set('clicked', sq);
                    window.parent.location.href = url.toString();
                }};
                
                if (piece) {{
                    const span = document.createElement('span');
                    span.className = 'pieces';
                    span.innerText = pieceMap[piece] || piece;
                    span.style.color = (piece === piece.toUpperCase()) ? '#fff' : '#000';
                    span.style.textShadow = "1px 1px 2px rgba(0,0,0,0.5)";
                    div.appendChild(span);
                }}
                
                if (isTarget) {{
                    const marker = document.createElement('div');
                    marker.className = isCapture ? 'capture-ring' : 'dot';
                    div.appendChild(marker);
                }}
                
                boardEl.appendChild(div);
            }});
        }});
    </script>
    </body>
    </html>
    """
    components.html(html, height=420, scrolling=False)

def get_clicked_square():
    """Reads the 'clicked' query param and clears it."""
    params = st.query_params
    if "clicked" in params:
        sq = params["clicked"]
        del st.query_params["clicked"]
        return sq
    return None
