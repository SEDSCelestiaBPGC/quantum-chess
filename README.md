# quantum-chess

![](https://github.com/SEDSCelestiaBPGC/quantum-chess/blob/master/Media/Poster.jpeg)

Hi! Welcome to the Quantum Chess repo.

Chess is a much loved, classic game, but what happens when we give it a quantum twist? Quantum chess works on the same rules as classical chess, but each piece has quantum abilities too- you can put a piece in a superposition, or even entangle two pieces. Our version is built using Qiskit, and is a great way to demonstrate and understand quantum properties. The game needs a good understanding of how various probabilities interact, to be able to comprehend how the state collapses upon observation, which happens when the piece is either capturing or being captured, and decides the position of a piece in superposition. These probabilities are decided by the quantum state of the piece, and thus adds an element of chance to this game of strategy.

## Rules
- The board is a regular 8x8 chessboard with the same 16 pieces on each side(black and white).
- The number next to the piece corresponds to the probability of the piece being at that position.
- All the pieces move according to the [normal rules](https://www.chess.com/learn-how-to-play-chess#chess-pieces-move).
- On a turn, a player can choose to either make a normal move or a quantum move.

#### Quantum Moves
- In the quantum mode, a piece can be moved to different positions in the same move.
- If both positions are unobstructed, the probability of the piece being in each of the new positions is 0.5.
- If obstructed by a quantum piece, the two pieces get 'entangled' and the piece being moved is split into two, each with a probability dependent on the probability of the obstructing piece.
- Entanglement of two pieces means that measuring either of the pieces will determine the state of the other.
- A piece is measured in two cases - either when it is perfoming a move to kill another piece, or when it is being killed.

## How to run
Qiskit is not compatible with Python 3.9

Use v3.8 or less.

`pip install chess`

`pip install qiskit`

## References
- https://quantumchess.net/
- https://truly-quantum-chess.sloppy.zone/
- https://github.com/caphindsight/TrulyQuantumChess/wiki
- https://chess.stackexchange.com/questions/18278/what-are-the-rules-of-quantum-chess
