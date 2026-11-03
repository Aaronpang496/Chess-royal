import streamlit.components.v1 as components
import json

def clickable_chess_board(board_2d, selected=None, legal_targets=None, flipped=False, key="board"):
    """
    Pure HTML/JS board. No npm required. Works on iPhone Safari.
    """
    # Convert board to JSON to pass to JS
    board_json = json.dumps(board_2d)
    selected_json = json.dumps(selected or "")
    targets_json = json.dumps(legal_targets or [])
    flipped_js = "true" if flipped else "false"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; background: transparent; }}
        .board {{ display: grid; grid-template-columns: repeat(8, 1fr); width: 100%; max-width: 400px; aspect-ratio: 1; border: 2px solid #333; }}
        .square {{ position: relative; display: flex; align-items: center; justify-content: center; font-size: 40px; cursor: pointer; user-select: none; -webkit-user-select: none; }}
        .light {{ background-color: #f0d9b5; }}
        .dark {{ background-color: #b58863; }}
        .selected {{ background-color: #a5c9a5 !important; }}
        .dot {{ width: 20%; height: 20%; background-color: #2e7d32; border-radius: 50%; position: absolute; opacity: 0.8; }}
        .capture-ring {{ width: 80%; height: 80%; border: 4px solid #2e7d32; border-radius: 50%; position: absolute; }}
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
                div.onclick = () => {{
                    // Send message to Streamlit
                    window.parent.postMessage({{
                        isStreamlitMessage: true,
                        type: "streamlit:setComponentValue",
                        value: sq
                    }}, "*");
                }};
                
                // Add piece
                if (piece) {{
                    const span = document.createElement('span');
                    span.className = 'pieces';
                    span.innerText = pieceMap[piece] || piece;
                    // Adjust piece color based on case
                    span.style.color = (piece === piece.toUpperCase()) ? '#fff' : '#000';
                    // Add shadow for visibility
                    span.style.textShadow = "1px 1px 2px rgba(0,0,0,0.5)";
                    div.appendChild(span);
                }}
                
                // Add dots / rings
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
    
    # Render the HTML component. Height needs to be roughly square + padding
    val = components.html(html, height=430, scrolling=False)
    
    # components.html doesn't return values directly (it's static). 
    # We need to use the query parameter trick or st.experimental_get_query_params.
    return val
