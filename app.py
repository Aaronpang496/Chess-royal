import streamlit as st
import chess

from core.state import init_state
from core.xp import add_xp, xp_for_result, xp_needed_for_next_level
from core.analysis import analyze_chess_moves
from games import chess_game, xiangqi_game, go_game
from ui.board_render import render_chess, render_xiangqi, render_go

st.set_page_config(page_title="Chess Center", layout="wide")
init_state()

# ---------- Sidebar ----------
with st.sidebar:
    st.header("🎮 Game")
    game_choice = st.radio(
        "Select game",
        ["♟️ Chess", "🀄 象棋", "⚫ 圍棋"],
        index=["chess","xiangqi","go"].index(st.session_state.current_game),
    )
    st.session_state.current_game = {"♟️ Chess":"chess","🀄 象棋":"xiangqi","⚫ 圍棋":"go"}[game_choice]

    st.divider()
    mode = st.radio("Mode", ["vs AI", "2 Players"])
    difficulty = st.select_slider("AI difficulty", ["easy","medium","hard"], value="medium")

    st.divider()
    lvl = st.session_state.level
    xp = st.session_state.xp
    need = xp_needed_for_next_level(lvl)
    st.metric("Level", lvl)
    st.progress(min(xp/need, 1.0), text=f"{xp}/{need} XP")
    st.caption(f"Total wins: {st.session_state.total_wins}")

    st.divider()
    if st.button("🔄 New Game", use_container_width=True):
        g = st.session_state.current_game
        if g == "chess":
            st.session_state.chess_board = chess.Board()
            st.session_state.chess_history = []
            st.session_state.chess_game_over = False
            st.session_state.chess_winner = None
            st.session_state.chess_xp_awarded = False
            st.session_state.chess_analysis = None
        elif g == "xiangqi":
            st.session_state.xq_board = xiangqi_game.initial_board()
            st.session_state.xq_history = []
            st.session_state.xq_game_over = False
            st.session_state.xq_winner = None
            st.session_state.xq_xp_awarded = False
            st.session_state.xq_analysis = None
        else:
            st.session_state.go_board = go_game.initial_board()
            st.session_state.go_history = []
            st.session_state.go_game_over = False
            st.session_state.go_winner = None
            st.session_state.go_xp_awarded = False
            st.session_state.go_passes = 0
        st.rerun()

# =========================================================
# CHESS
# =========================================================
if st.session_state.current_game == "chess":
    st.title("♟️ Chess")

    if st.session_state.chess_board is None:
        st.session_state.chess_board = chess.Board()

    board = st.session_state.chess_board

    last_move = None
    if st.session_state.chess_history:
        last_move = chess.Move.from_uci(st.session_state.chess_history[-1]["uci"])

    render_chess(board, last_move=last_move)

    # game end
    if board.is_game_over() and not st.session_state.chess_game_over:
        st.session_state.chess_game_over = True
        if board.is_checkmate():
            st.session_state.chess_winner = "black" if board.turn == chess.WHITE else "white"
        else:
            st.session_state.chess_winner = "draw"

    if st.session_state.chess_game_over:
        w = st.session_state.chess_winner
        st.success(f"Game over — {w.upper() if w != 'draw' else 'DRAW'}")

        if not st.session_state.chess_xp_awarded and mode == "vs AI":
            player_white = True
            if w == "draw":
                result = "draw"
            elif w == ("white" if player_white else "black"):
                result = "win"
                st.session_state.total_wins += 1
            else:
                result = "loss"
            gain = xp_for_result(result, difficulty)
            add_xp(gain)
            st.info(f"+{gain} XP")
            st.session_state.chess_xp_awarded = True
            from core.state import persist_xp
            persist_xp()

        if st.button("🔍 Analyze my moves"):
            st.session_state.chess_analysis = analyze_chess_moves(
                st.session_state.chess_history, chess.WHITE
            )
        if st.session_state.chess_analysis is not None:
            if st.session_state.chess_analysis:
                st.warning(f"Found {len(st.session_state.chess_analysis)} questionable moves:")
                st.dataframe(st.session_state.chess_analysis, use_container_width=True)
            else:
                st.success("No major mistakes detected! 🎉")
        st.stop()

    # input
    st.subheader(f"{'White' if board.turn == chess.WHITE else 'Black'} to move")
    with st.form("chess_move_form", clear_on_submit=True):
        uci = st.text_input("Move (UCI, e.g. e2e4)")
        submitted = st.form_submit_button("Play")
    if submitted and uci:
        try:
            m = chess.Move.from_uci(uci.strip())
            if m in board.legal_moves:
                san = board.san(m)
                board.push(m)
                st.session_state.chess_history.append(
                    {"uci": m.uci(), "san": san, "fen": board.fen()}
                )
                if mode == "vs AI" and not board.is_game_over():
                    ai = chess_game.get_ai_move(board, difficulty)
                    if ai:
                        san2 = board.san(ai)
                        board.push(ai)
                        st.session_state.chess_history.append(
                            {"uci": ai.uci(), "san": san2, "fen": board.fen()}
                        )
                st.rerun()
            else:
                st.error("Illegal move.")
        except ValueError:
            st.error("Invalid UCI format.")

    with st.expander("Move history"):
        for i, h in enumerate(st.session_state.chess_history):
            st.write(f"{i//2 + 1}. {h['san']}")

# =========================================================
# XIANGQI
# =========================================================
elif st.session_state.current_game == "xiangqi":
    st.title("🀄 象棋")

    if st.session_state.xq_board is None:
        st.session_state.xq_board = xiangqi_game.initial_board()

    board = st.session_state.xq_board
    render_xiangqi(board)

    # determine side to move
    turn = "r" if len(st.session_state.xq_history) % 2 == 0 else "b"

    # end condition
    if not st.session_state.xq_game_over:
        result = xiangqi_game.is_checkmate_or_stalemate(board, turn)
        if result == "checkmate":
            st.session_state.xq_game_over = True
            st.session_state.xq_winner = "b" if turn == "r" else "r"
        elif result == "stalemate":
            st.session_state.xq_game_over = True
            st.session_state.xq_winner = "draw"

    if st.session_state.xq_game_over:
        w = st.session_state.xq_winner
        st.success(f"Game over — {'Red' if w=='r' else 'Black' if w=='b' else 'DRAW'}")

        if not st.session_state.xq_xp_awarded and mode == "vs AI":
            player_color = "r"
            if w == "draw":
                result = "draw"
            elif w == player_color:
                result = "win"
                st.session_state.total_wins += 1
            else:
                result = "loss"
            gain = xp_for_result(result, difficulty)
            add_xp(gain)
            st.info(f"+{gain} XP")
            st.session_state.xq_xp_awarded = True
            from core.state import persist_xp
            persist_xp()

        if st.button("🔍 Analyze my moves"):
            st.session_state.xq_analysis = xiangqi_game.analyze_xiangqi_moves(
                st.session_state.xq_history, "r"
            )
        if st.session_state.xq_analysis is not None:
            if st.session_state.xq_analysis:
                st.warning(f"Found {len(st.session_state.xq_analysis)} questionable moves:")
                st.dataframe(st.session_state.xq_analysis, use_container_width=True)
            else:
                st.success("No major mistakes detected! 🎉")
        st.stop()

    st.subheader(f"{'Red' if turn=='r' else 'Black'} to move")
    st.caption("Enter coordinates from and to. Rows 0-9 top→bottom, cols 0-8 left→right. Red home = row 9.")

    with st.form("xq_form", clear_on_submit=True):
        col1, col2, col3, col4 = st.columns(4)
        fr = col1.number_input("From row", 0, 9, 9)
        fc = col2.number_input("From col", 0, 8, 0)
        tr = col3.number_input("To row", 0, 9, 8)
        tc = col4.number_input("To col", 0, 8, 0)
        submitted = st.form_submit_button("Play")
    if submitted:
        move = ((int(fr), int(fc)), (int(tr), int(tc)))
        legal = xiangqi_game.legal_moves_for(board, turn)
        if move in legal:
            new_board = xiangqi_game.apply_move(board, move)
            st.session_state.xq_history.append({
                "from": move[0], "to": move[1], "color": turn,
                "board_before": board, "board_after": new_board,
            })
            st.session_state.xq_board = new_board
            if mode == "vs AI":
                enemy = "b" if turn == "r" else "r"
                if not xiangqi_game.is_checkmate_or_stalemate(new_board, enemy):
                    ai = xiangqi_game.get_ai_move(new_board, enemy, difficulty)
                    if ai:
                        nb2 = xiangqi_game.apply_move(new_board, ai)
                        st.session_state.xq_history.append({
                            "from": ai[0], "to": ai[1], "color": enemy,
                            "board_before": new_board, "board_after": nb2,
                        })
                        st.session_state.xq_board = nb2
            st.rerun()
        else:
            st.error("Illegal move for that piece, or leaves your king in check.")

# =========================================================
# GO
# =========================================================
else:
    st.title("⚫ 圍棋 (9×9)")

    if st.session_state.go_board is None:
        st.session_state.go_board = go_game.initial_board()

    board = st.session_state.go_board
    render_go(board)

    turn = "b" if len(st.session_state.go_history) % 2 == 0 else "w"

    if st.session_state.go_game_over:
        w = st.session_state.go_winner
        st.success(f"Game over — {w.upper() if w != 'draw' else 'DRAW'}")
        if not st.session_state.go_xp_awarded and mode == "vs AI":
            player = "b"
            if w == "draw":
                result = "draw"
            elif w == player:
                result = "win"
                st.session_state.total_wins += 1
            else:
                result = "loss"
            gain = xp_for_result(result, difficulty)
            add_xp(gain)
            st.info(f"+{gain} XP")
            st.session_state.go_xp_awarded = True
            from core.state import persist_xp
            persist_xp()
        st.stop()

    st.subheader(f"{'Black' if turn=='b' else 'White'} to move — pass count: {st.session_state.go_passes}")

    col1, col2, col3, col4 = st.columns(4)
    r = col1.number_input("Row", 0, 8, 4)
    c = col2.number_input("Col", 0, 8, 4)
    if col3.button("Play"):
        nb, ok, _ = go_game.play_move(board, int(r), int(c), turn)
        if ok:
            st.session_state.go_board = nb
            st.session_state.go_history.append((int(r), int(c)))
            st.session_state.go_passes = 0
            if mode == "vs AI":
                enemy = "w" if turn == "b" else "b"
                ai = go_game.ai_move(nb, enemy, difficulty)
                if ai:
                    nb2, ok2, _ = go_game.play_move(nb, ai[0], ai[1], enemy)
                    if ok2:
                        st.session_state.go_board = nb2
                        st.session_state.go_history.append(ai)
                else:
                    st.session_state.go_passes += 1
            st.rerun()
        else:
            st.error("Illegal move (occupied or suicide).")

    if col4.button("Pass"):
        st.session_state.go_passes += 1
        st.session_state.go_history.append("pass")
        if st.session_state.go_passes >= 2:
            st.session_state.go_game_over = True
            b_score, w_score = go_game.score_board(st.session_state.go_board)
            if b_score > w_score:
                st.session_state.go_winner = "b"
            elif w_score > b_score:
                st.session_state.go_winner = "w"
            else:
                st.session_state.go_winner = "draw"
            st.info(f"Final: Black {b_score} — White {w_score}")
        st.rerun()
