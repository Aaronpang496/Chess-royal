import os
import subprocess
import threading
import queue

PIKAFISH_PATH = os.environ.get("PIKAFISH_PATH", "./pikafish")  # or .exe on Windows

class Pikafish:
    def __init__(self, path=PIKAFISH_PATH, depth=10):
        self.depth = depth
        self.proc = subprocess.Popen(
            [path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )
        self._send("uci")
        self._read_until("uciok")
        self._send("isready")
        self._read_until("readyok")

    def _send(self, cmd):
        self.proc.stdin.write(cmd + "\n")
        self.proc.stdin.flush()

    def _read_until(self, token):
        while True:
            line = self.proc.stdout.readline()
            if not line:
                return None
            if line.strip() == token:
                return line

    def best_move(self, fen, depth=None):
        """fen: xiangqi FEN string. Returns (from_rc, to_rc) or None."""
        self._send(f"position fen {fen}")
        self._send(f"go depth {depth or self.depth}")
        while True:
            line = self.proc.stdout.readline()
            if not line:
                return None
            if line.startswith("bestmove"):
                parts = line.split()
                if len(parts) < 2 or parts[1] == "(none)":
                    return None
                uci = parts[1]
                return uci[:2], uci[2:4]
        return None

    def close(self):
        try:
            self._send("quit")
        except Exception:
            pass

_cached = {}

def get_engine():
    if "engine" not in _cached:
        try:
            _cached["engine"] = Pikafish()
        except Exception:
            _cached["engine"] = None
    return _cached["engine"]

def is_available():
    return get_engine() is not None

def best_move_uci(fen, depth=10):
    eng = get_engine()
    if eng is None:
        return None
    try:
        return eng.best_move(fen, depth)
    except Exception:
        return None
