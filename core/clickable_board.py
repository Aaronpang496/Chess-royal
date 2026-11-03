import os
import streamlit.components.v1 as components

_COMPONENT_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend", "build")

if os.path.isdir(_COMPONENT_DIR):
    _clickable_board = components.declare_component("clickable_board", path=_COMPONENT_DIR)
else:
    _clickable_board = None

def clickable_chess_board(board_2d, selected=None, legal_targets=None, flipped=False, key=None):
    """
    board_2d: 8x8 list of piece-char strings
    returns: clicked square name (e.g. "e4") or None
    """
    if _clickable_board is None:
        return None
    return _clickable_board(
        board=board_2d,
        selected=selected or "",
        legal_targets=legal_targets or [],
        flipped=flipped,
        key=key,
        default=None,
    )

def is_available():
    return _clickable_board is not None
