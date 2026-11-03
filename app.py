# --- GAME OVER HANDLING ---
    if board.is_game_over() and not st.session_state.chess_game_over:
        st.session_state.chess_game_over = True
        if board.is_checkmate():
            st.session_state.chess_winner = "black" if board.turn == chess.WHITE else "white"
        else:
            st.session_state.chess_winner = "draw"

    if st.session_state.chess_game_over:
        w = st.session_state.chess_winner
        
        # Display Result
        if w == "draw":
            st.warning("Game over — DRAW")
        else:
            st.success(f"Game over — {w.upper()} WINS")
            
        # XP Logic (Only if vs AI and not yet awarded)
        if not st.session_state.chess_xp_awarded and mode == "vs AI":
            player_color = "white" # Assuming player is always White for now
            if w == "draw":
                result = "draw"
            elif w == player_color:
                result = "win"
                register_win("chess")
            else:
                result = "loss"
                
            gain = xp_for_result(result, difficulty)
            add_xp("chess", gain)
            st.info(f"Result: {result.upper()} — +{gain} XP")
            st.session_state.chess_xp_awarded = True

        # Analysis Button
        if st.button("🔍 Analyze my moves"):
            player_c = chess.WHITE # Assumes you play White
            mistakes, good_moves = analyze_chess_moves(st.session_state.chess_history, player_c)
            st.session_state.chess_analysis = {"mistakes": mistakes, "good": good_moves}
            
        # Display Analysis Results
        if st.session_state.chess_analysis is not None:
            mistakes = st.session_state.chess_analysis["mistakes"]
            good = st.session_state.chess_analysis["good"]
            
            if not mistakes and not good:
                st.success("Flawless game! No major mistakes or brilliant captures. 🎉")
            else:
                if mistakes:
                    st.error(f"Found {len(mistakes)} mistakes/blunders:")
                    st.dataframe(mistakes, use_container_width=True, hide_index=True)
                if good:
                    st.success(f"Found {len(good)} great captures:")
                    st.dataframe(good, use_container_width=True, hide_index=True)
                    
        st.stop()
