import React from "react";

const PIECES = {
  p: "♟", r: "♜", n: "♞", b: "♝", q: "♛", k: "♚",
  P: "♙", R: "♖", N: "♘", B: "♗", Q: "♕", K: "♔",
};

export default function Board({ board, selected, legalTargets, flipped, onSquareClick }) {
  // board: 8x8 array of chars ('P' white, 'p' black, '' empty) row 0 = rank 8
  const files = ["a","b","c","d","e","f","g","h"];
  const ranks = ["8","7","6","5","4","3","2","1"];
  const rows = flipped ? [...Array(8)].map((_, i) => 7 - i) : [...Array(8).keys()];
  const cols = flipped ? [...Array(8)].map((_, i) => 7 - i) : [...Array(8).keys()];

  return (
    <div style={{ fontFamily: "serif", userSelect: "none" }}>
      {rows.map((r) => (
        <div key={r} style={{ display: "flex" }}>
          {cols.map((c) => {
            const sq = files[c] + ranks[r];
            const isLight = (r + c) % 2 === 0;
            const piece = board ? board[r][c] : "";
            const isSelected = selected === sq;
            const isTarget = legalTargets.includes(sq);
            const isCapture = isTarget && piece !== "";
            return (
              <div
                key={c}
                onClick={() => onSquareClick(sq)}
                style={{
                  width: 60, height: 60,
                  background: isSelected ? "#a5c9a5" : isLight ? "#f0d9b5" : "#b58863",
                  display: "flex", alignItems: "center", justifyContent: "center",
                  position: "relative", cursor: "pointer",
                  fontSize: 38,
                }}
              >
                {PIECES[piece] || ""}
                {isTarget && !isCapture && (
                  <div style={{
                    position: "absolute", width: 16, height: 16,
                    borderRadius: "50%", background: "#2e7d32", opacity: 0.7,
                  }} />
                )}
                {isCapture && (
                  <div style={{
                    position: "absolute", inset: 4, borderRadius: "50%",
                    border: "4px solid #2e7d32", pointerEvents: "none",
                  }} />
                )}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}
