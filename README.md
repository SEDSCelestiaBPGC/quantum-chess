# quantum-chess

![](https://github.com/SEDSCelestiaBPGC/quantum-chess/blob/master/Media/Poster.jpeg)

Hi! Welcome to the Quantum Chess repo.

Here you will find the code to a functional quantum chessboard, on which two players can play a game. Quantum chess differs from classical chess in that it lends various quantum abilities to its pieces in the form of superposition (as though you are playing on two boards at once!) and entanglement (measuring one affects many!). This offers a twist to the age old game and helps us demonstrate these quantum phenomena.
Our qchessboard is built using Qiskit and Pygame.

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

## References
- https://quantumchess.net/
- https://truly-quantum-chess.sloppy.zone/
- https://github.com/caphindsight/TrulyQuantumChess/wiki
- https://chess.stackexchange.com/questions/18278/what-are-the-rules-of-quantum-chess
