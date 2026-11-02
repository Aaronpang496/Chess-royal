import streamlit as st
from core.state import persist_xp

XP_TABLE = {
    ("win",  "easy"):   10,
    ("win",  "medium"): 25,
    ("win",  "hard"):   50,
    ("draw", "easy"):    3,
    ("draw", "medium"):  8,
    ("draw", "hard"):   15,
    ("loss", "easy"):    1,
    ("loss", "medium"):  2,
    ("loss", "hard"):    5,
}

def xp_for_result(result: str, difficulty: str) -> int:
    return XP_TABLE.get((result, difficulty), 0)

def xp_needed_for_next_level(level: int) -> int:
    return int(100 * (1.5 ** (level - 1)))

def add_xp(gain: int):
    st.session_state.xp += gain
    while st.session_state.xp >= xp_needed_for_next_level(st.session_state.level):
        st.session_state.xp -= xp_needed_for_next_level(st.session_state.level)
        st.session_state.level += 1
    persist_xp()
