import React from "react";
import ReactDOM from "react-dom/client";
import Board from "./Board.jsx";

function App() {
  // Streamlit passes args via window.__streamlit_args
  const args = window.__streamlit_args || {};
  return (
    <Board
      board={args.board}
      selected={args.selected}
      legalTargets={args.legal_targets || []}
      flipped={args.flipped || false}
      onSquareClick={(sq) => {
        window.parent.postMessage(
          { isStreamlitMessage: true, type: "streamlit:setComponentValue", value: sq },
          "*"
        );
      }}
    />
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
