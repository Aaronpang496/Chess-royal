import streamlit as st
from core.state import persist_xp

XP_TABLE = {
    ("win","easy"):10, ("win","medium"):25, ("win","hard"):50,
    ("draw","easy"):3, ("draw","medium"):8, ("draw","hard"):15,
    ("loss","easy"):1, ("loss","medium"):2, ("loss","hard"):5,
}

def xp_for_result(result, difficulty):
    return XP_TABLE.get((result, difficulty), 0)

def xp_needed_for_next_level(level):
    return int(100 * (1.5 ** (level - 1)))

def add_xp(game, gain):
    xp_key = f"{game}_xp"
    lvl_key = f"{game}_level"
    st.session_state[xp_key] += gain
    while st.session_state[xp_key] >= xp_needed_for_next_level(st.session_state[lvl_key]):
        st.session_state[xp_key] -= xp_needed_for_next_level(st.session_state[lvl_key])
        st.session_state[lvl_key] += 1
    persist_xp()

def register_win(game):
    st.session_state[f"{game}_wins"] += 1
    persist_xp()

def get_progress(game):
    lvl = st.session_state[f"{game}_level"]
    xp = st.session_state[f"{game}_xp"]
    need = xp_needed_for_next_level(lvl)
    return lvl, xp, need
