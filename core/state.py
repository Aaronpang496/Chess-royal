import streamlit as st
import json, os

XP_FILE = "xp_save.json"

def _load():
    if os.path.exists(XP_FILE):
        try:
            with open(XP_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "chess":    {"xp": 0, "level": 1, "wins": 0},
        "xiangqi":  {"xp": 0, "level": 1, "wins": 0},
        "go":       {"xp": 0, "level": 1, "wins": 0},
    }

def _save(data):
    with open(XP_FILE, "w") as f:
        json.dump(data, f, indent=2)

def init_state():
    saved = _load()
    for game in ("chess", "xiangqi", "go"):
        st.session_state.setdefault(f"{game}_xp", saved[game]["xp"])
        st.session_state.setdefault(f"{game}_level", saved[game]["level"])
        st.session_state.setdefault(f"{game}_wins", saved[game]["wins"])

    st.session_state.setdefault("current_game", "chess")

    # chess
    st.session_state.setdefault("chess_board", None)
    st.session_state.setdefault("chess_history", [])       # list of {"uci","san","fen"}
    st.session_state.setdefault("chess_game_over", False)
    st.session_state.setdefault("chess_winner", None)
    st.session_state.setdefault("chess_xp_awarded", False)
    st.session_state.setdefault("chess_analysis", None)
    st.session_state.setdefault("chess_selected", None)    # (row,col) for click UI

    # xiangqi
    st.session_state.setdefault("xq_board", None)
    st.session_state.setdefault("xq_history", [])
    st.session_state.setdefault("xq_game_over", False)
    st.session_state.setdefault("xq_winner", None)
    st.session_state.setdefault("xq_xp_awarded", False)
    st.session_state.setdefault("xq_analysis", None)

    # go
    st.session_state.setdefault("go_board", None)
    st.session_state.setdefault("go_history", [])
    st.session_state.setdefault("go_game_over", False)
    st.session_state.setdefault("go_winner", None)
    st.session_state.setdefault("go_xp_awarded", False)
    st.session_state.setdefault("go_passes", 0)

def persist_xp():
    data = {}
    for game in ("chess", "xiangqi", "go"):
        data[game] = {
            "xp": st.session_state[f"{game}_xp"],
            "level": st.session_state[f"{game}_level"],
            "wins": st.session_state[f"{game}_wins"],
        }
    _save(data)
