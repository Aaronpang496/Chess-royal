# Inside the CHESS section of app.py:

    if st.session_state.chess_board is None:
        st.session_state.chess_board = chess.Board()
    board = st.session_state.chess_board

    selected = st.session_state.chess_selected
    legal_targets = []
    if selected is not None:
        sq = chess.parse_square(selected)
        for m in board.legal_moves:
            if m.from_square == sq:
                legal_targets.append(m.to_square)

    # 1. Render the board
    clickable_chess_board(
        board, 
        selected, 
        legal_targets, 
        flipped=(board.turn == chess.BLACK and mode == "vs AI")
    )

    # 2. Check for a click
    clicked = get_clicked_square()
    if clicked:
        if selected is None:
            piece = board.piece_at(chess.parse_square(clicked))
            if piece and piece.color == board.turn:
                st.session_state.chess_selected = clicked
                st.rerun()
        else:
            try:
                m = chess.Move.from_uci(selected + clicked)
                if m in board.legal_moves:
                    san = board.san(m)
                    board.push(m)
                    st.session_state.chess_history.append({"uci": m.uci(), "san": san, "fen": board.fen()})
                    st.session_state.chess_selected = None
                    if mode == "vs AI" and not board.is_game_over():
                        ai = chess_game.get_ai_move(board, difficulty)
                        if ai:
                            san2 = board.san(ai)
                            board.push(ai)
                            st.session_state.chess_history.append({"uci": ai.uci(), "san": san2, "fen": board.fen()})
                    st.rerun()
                else:
                    # Deselect or reselect
                    piece = board.piece_at(chess.parse_square(clicked))
                    if piece and piece.color == board.turn:
                        st.session_state.chess_selected = clicked
                    else:
                        st.session_state.chess_selected = None
                    st.rerun()
            except ValueError:
                st.session_state.chess_selected = None
                st.rerun()
