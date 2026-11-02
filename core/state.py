import streamlit as st
import json
import os

XP_FILE = "xp_save.json"

def _load_xp():
    if os.path.exists(XP_FILE):
        try:
            with open(XP_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"xp": 0, "level": 1, "total_wins": 0}

def _save_xp(data):
    with open(XP_FILE, "w") as f:
        json.dump(data, f)

def init_state():
    saved = _load_xp()
    defaults = {
        # global
        "current_game": "chess",   # chess | xiangqi | go
        "xp": saved["xp"],
        "level": saved["level"],
        "total_wins": saved["total_wins"],

        # per-game reset flags
        "chess_board": None,
        "chess_history": [],
        "chess_game_over": False,
        "chess_winner": None,
        "chess_xp_awarded": False,
        "chess_analysis": None,

        "xq_board": None,
        "xq_history": [],
        "xq_game_over": False,
        "xq_winner": None,
        "xq_xp_awarded": False,
        "xq_analysis": None,

        "go_board": None,
        "go_history": [],
        "go_game_over": False,
        "go_winner": None,
        "go_xp_awarded": False,
        "go_passes": 0,
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

def persist_xp():
    _save_xp({
        "xp": st.session_state.xp,
        "level": st.session_state.level,
        "total_wins": st.session_state.total_wins,
    })
