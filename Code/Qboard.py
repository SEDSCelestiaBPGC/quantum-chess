# from Code.Quant import quantum_obj
from copy import error
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
from PySide2.QtCore import QFile, QObject, QTextStream, QXmlStreamEntityResolver
from PySide2.QtGui import QPixmap
import sys
import chess
from functools import partial

from PySide2.QtCore import Qt
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui

sys.path.append('hichess-mod\examples\BoardWidgetExample') 
sys.path.append('hichess-mod\hichess') 
import hichess
from context import resources
from Quant import *

from hichess import CellWidget, _PromotionDialog, IllegalMove
from chess import *

class QchessBoard(chess.Board):
    qpcs = []

    def generate_pseudo_legal_moves(self, from_mask = chess.BB_ALL, to_mask = chess.BB_ALL ):
        print('psudoLegalCalled')
        # //BUG allows non quantum pcs to kill their own
        temp_occupied_co = self.occupied_co.copy()
        for qpc in self.qpcs:
            for state in qpc.qnum.keys():
                if qpc.qnum[state][1] !=1:
                    temp_occupied_co[self.turn] &= ~chess.BB_SQUARES[qpc.qnum[state][0]]
                    temp_occupied_co[not self.turn] &= ~chess.BB_SQUARES[qpc.qnum[state][0]]

        our_pieces = self.occupied_co.copy()[self.turn]
        our_q_pieces = temp_occupied_co.copy()[self.turn]

        our_pieces_L = self.occupied_co.copy()
        our_q_pieces_L = temp_occupied_co.copy()

        # Generate piece moves.
        non_pawns = our_pieces & ~self.pawns & from_mask
        for from_square in scan_reversed(non_pawns):
            self.occupied = our_q_pieces_L[0] | our_q_pieces_L[1]
            moves = self.attacks_mask(from_square) & ~our_q_pieces & to_mask
            self.occupied = our_pieces_L[0] | our_pieces_L[1]
            for to_square in scan_reversed(moves):
                yield Move(from_square, to_square)

        # Generate castling moves.
        if from_mask & self.kings:
            yield from self.generate_castling_moves(from_mask, to_mask)

        # The remaining moves are all pawn moves.
        pawns = self.pawns & self.occupied_co[self.turn] & from_mask
        if not pawns:
            return

        # Generate pawn captures.
        capturers = pawns
        for from_square in scan_reversed(capturers):
            targets = (
                BB_PAWN_ATTACKS[self.turn][from_square] &
                self.occupied_co[not self.turn] & to_mask)

            for to_square in scan_reversed(targets):
                if square_rank(to_square) in [0, 7]:
                    yield Move(from_square, to_square, QUEEN)
                    yield Move(from_square, to_square, ROOK)
                    yield Move(from_square, to_square, BISHOP)
                    yield Move(from_square, to_square, KNIGHT)
                else:
                    yield Move(from_square, to_square)

        # Prepare pawn advance generation.
        if self.turn == WHITE:
            single_moves = pawns << 8 & ~self.occupied
            double_moves = single_moves << 8 & ~self.occupied & (BB_RANK_3 | BB_RANK_4)
        else:
            single_moves = pawns >> 8 & ~self.occupied
            double_moves = single_moves >> 8 & ~self.occupied & (BB_RANK_6 | BB_RANK_5)

        single_moves &= to_mask
        double_moves &= to_mask

        # Generate single pawn moves.
        for to_square in scan_reversed(single_moves):
            from_square = to_square + (8 if self.turn == BLACK else -8)

            if square_rank(to_square) in [0, 7]:
                yield Move(from_square, to_square, QUEEN)
                yield Move(from_square, to_square, ROOK)
                yield Move(from_square, to_square, BISHOP)
                yield Move(from_square, to_square, KNIGHT)
            else:
                yield Move(from_square, to_square)

        # Generate double pawn moves.
        for to_square in scan_reversed(double_moves):
            from_square = to_square + (16 if self.turn == BLACK else -16)
            yield Move(from_square, to_square)

        # Generate en passant captures.
        if self.ep_square:
            yield from self.generate_pseudo_legal_ep(from_mask, to_mask)

class QBoardWidget(hichess.BoardWidget):

    def __init__(self) -> None:
        super().__init__()
        self.board = QchessBoard(fen=chess.STARTING_FEN)

    split_turn = False # //HACK use this instance in mainWindow
    entangle_move = False # //HACK use this instance in somewhere else
    previous_entangle_move = False
    qpcs = [] # //TODO organize code to only have req stuff in main window, and board related stuff here
    moveMade = QtCore.Signal(chess.Move)
    cellWidgetClickedSig = QtCore.Signal(hichess.CellWidget)
    illegalClassicalMove = QtCore.Signal(chess.Move)

    def _push(self, move: chess.Move) -> None:
        self._updateJustMovedCells(False)

        turn = self.board.turn

        if self._isCellAccessible(self.cellWidgetAtSquare(move.from_square)) \
                and move.promotion is None and self.isPseudoLegalPromotion(move):
            w = self.cellWidgetAtSquare(move.to_square)

            promotionDialog = _PromotionDialog(parent=self, color=turn, order=self._flipped)
            if not self._flipped and turn:
                promotionDialog.move(self.mapToGlobal(w.pos()))
            else:
                promotionDialog.move(self.mapToGlobal(QtCore.QPoint(w.x(), w.y() - 3 * w.height())))
            promotionDialog.setFixedWidth(w.width())
            promotionDialog.setFixedHeight(4 * w.height())

            exitCode = promotionDialog.exec_()
            if exitCode == _PromotionDialog.Accepted:
                move.promotion = promotionDialog.chosenPiece
            elif exitCode == _PromotionDialog.Rejected:
                self.foreachCells(CellWidget.unhighlight, lambda w: w.setChecked(False))
                return

        if not self.board.is_legal(move) or move.null():
            # //HACK this is the only way for a move to be illegal (without playtesting)
            # self.illegalClassicalMove.emit(move)
            self.entangle_move = True
            # raise IllegalMove(f"illegal move {move} by ")
        # logging.debug(f"\n{self.board.lan(move)} ({move.from_square} -> {move.to_square})")

        san = self.board.san(move)
        self.board.push(move)
        # logging.debug(f"\n{self.board}\n")

        self._updateJustMovedCells(True)
        self.popStack.clear()

        self.foreachCells(CellWidget.unmark, CellWidget.unhighlight)
        self.synchronizeAndUpdateStyles()

        self.moveMade.emit(move)
        self.movePushed.emit(san)

    def _updateJustMovedCells(self, justMoved):
        # //TODO finish this func
        pass

    @QtCore.Slot()
    def _onCellWidgetClicked(self, w):
        # self.cellWidgetClickedSig.emit(w)
        if w.highlighted:
            self.pushPiece(self.squareOf(w), self.lastCheckedCellWidget)
            self.unmarkCells()
        elif not w.piece:
            self.foreachCells(hichess.CellWidget.unhighlight, hichess.CellWidget.unmark,
                              lambda w: w.setChecked(False))
        else:
            self.unmarkCells()

    @QtCore.Slot()
    def _onCellWidgetToggled(self, w: CellWidget, toggled: bool):
        if toggled:
            self.cellWidgetClickedSig.emit(w)
            if self.board.turn != w.getPiece().color or not self._isCellAccessible(w):
                w.setChecked(False)
                return

            if self.blockBoardOnPop and self.popStack:
                w.setChecked(False)
                return
            
            if not len(self.board.move_stack) <1 and self.split_turn:
                if self.board.peek().from_square != self.squareOf(w):
                    return 
            # //FIXME this lets player check multiple pcs (check stylesheet for 'checked' variable)

            def callback(_w: CellWidget):
                if _w != w:
                    _w.setChecked(False)

            self.foreachCells(CellWidget.unmark, CellWidget.unhighlight, callback)
            if not self.highlightLegalMoveCellsFor(w):
                w.setChecked(False)
            self.lastCheckedCellWidget = w
        else:
            self.unhighlightCells()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.previous_move = chess.Move(chess.A1, chess.A2) # //HACK get previous move from board?

        self.centralWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # Initialize board
        self.boardWidget = QBoardWidget()
        #quant stuff here plis
        self.Qpieces = []
        self.quantum_mode = False
        self.split_turn = False # for second move when split
        self.boardWidget.foreachCells(self.setQboard)

        # The user can interract with both colors of the board
        self.boardWidget.accessibleSides = hichess.BOTH_SIDES
        # Enable drag and drop
        self.boardWidget.dragAndDrop = True

        # background image
        self.boardWidget.setBoardPixmap(defaultPixmap=QPixmap(":/images/chessboard.png"),
                                        flippedPixmap=QPixmap(":/images/flipped_chessboard.png"))

        # qss
        qss = QFile(":/style/styles.css")
        if qss.open(QFile.ReadOnly):
            textStream = QTextStream(qss)
            self.boardWidget.setStyleSheet(textStream.readAll())

        self.flipButton = QPushButton("Flip")
        # flip the board when the button is pressed
        self.flipButton.clicked.connect(self.boardWidget.flip)

        self.mainLayout.addWidget(self.boardWidget)
        self.mainLayout.addWidget(self.flipButton)
        self.centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.centralWidget)

        self.boardWidget.moveMade.connect(self.checkQmove)
        self.boardWidget.illegalClassicalMove.connect(self.entangleMove)
    
    def setQboard(self, cellWid):
        '''
        sets initial qObjs when game starts
        '''
        if cellWid.getPiece() is not None:
            q_pc = quantum_obj(self.boardWidget.squareOf(cellWid), cellWid.getPiece())
            self.Qpieces.append(q_pc)
            self.boardWidget.board.qpcs.append(q_pc)

    def updateQboard(self, turn):
        '''
        turn = True if white to play
        Updates board according to Qpieces, useful when calling measure
        '''
        newBoard = chess.Board(fen = None) 
        for qObj in self.Qpieces:
            for state in qObj.qnum.keys():
                newBoard.set_piece_at(qObj.qnum[state][0], qObj.piece)
        self.boardWidget.board.set_fen(newBoard.fen())
        self.boardWidget.board.turn = turn
        self.boardWidget.board.qpcs = self.Qpieces
        self.boardWidget._synchronize()

    def checkQmove(self, move):
        '''
        Handles all special moves for quantum chess
        order: https://witeboard.com/305eecf0-6abe-11eb-a9a9-6531453db8f7
        '''

        qObj, qObj_state = self.findQobj(move.from_square)
        qpc_squares = 0

        if self.boardWidget.entangle_move:
            qpc_squares = self.boardWidget.board.occupied & int(chess.SquareSet.between(move.from_square, move.to_square))

        if self.findQobj(move.to_square) is not None: #atk
            if self.boardWidget.entangle_move: #meas in b/w when atking
               for sq in qpc_squares:
                qObj_mid, _ = self.findQobj(sq)
                qObj_mid.meas()

            self.attackMove(move)
            return

        if self.quantum_mode:
            if self.boardWidget.split_turn:
                if self.boardWidget.previous_entangle_move:
                    if self.boardWidget.entangle_move:
                        self.entangleMove(move)
                        self.boardWidget.board.qpcs = self.Qpieces
                        self.updateQboard(self.boardWidget.board.turn)
                        return
                    else:
                        self.entangleMove(self.previous_move)

                self.splitMove(qObj, qObj_state, move.to_square, self.previous_move.to_square)
                self.boardWidget.board.qpcs = self.Qpieces
                self.updateQboard(self.boardWidget.board.turn)
            else:
                self.boardWidget.board.turn = not self.boardWidget.board.turn
                self.boardWidget.setPieceAt(move.from_square, qObj.piece)
                self.split_turn = True # //HACK remove
                self.boardWidget.split_turn = True
                self.previous_move = move
                self.boardWidget.board.move_stack.append(self.previous_move)

                if self.boardWidget.entangle_move:
                    self.boardWidget.previous_entangle_move=True
                else:
                    self.boardWidget.previous_entangle_move=False # //HACK i'm scared to remove this

                self.boardWidget.board.qpcs = self.Qpieces
                return
        else:
            if self.boardWidget.entangle_move:
                self.entangleMove(move)
                self.boardWidget.previous_entangle_move = True
                self.boardWidget.entangle_move = False
            else:
                qObj.qnum[qObj_state][0] = move.to_square
                self.boardWidget.previous_entangle_move = False

        self.boardWidget.board.qpcs = self.Qpieces
        # self.updateQboard(self.boardWidget.board.turn) # //FIXME only update when needed
    def attackMove(self, move):
        '''
        Attacking, measures if attacked/attacking has more than one state/add 
        '''
        self.quantum_mode = False # //HACK shouldn't disable quantum_mode if we allow shrodinger's pcs
        self.split_turn = False
        self.boardWidget.split_turn = False

        qObj, qObj_state = self.findQobj(move.from_square)
        qObj_attacked, qObj_attacked_state = self.findQobj(move.to_square)

        if qObj.qnum[qObj_state][1] !=1:
            qObj.meas()
            print('mes1')
            self.updateQboard(turn = not qObj.piece.symbol().isupper()) 
            if qObj.qnum['0'][0] == move.from_square: # attack*ing* piece exists
                self.checkQmove(move)
            for qpc in self.Qpieces:
                print(qpc.piece, qpc.qnum)
            return

        if  qObj_attacked.qnum[qObj_attacked_state][1] !=1:
            qObj_attacked.meas()
            print('mes2')
            # if qObj_attacked.qnum['0'][0] != move.to_square: # attack*ed* piece doen't exist
            #     qObj.qnum[qObj_state][0] = move.to_square

            self.updateQboard(turn = not qObj.piece.symbol().isupper()) 
            self.checkQmove(move)
            for qpc in self.Qpieces:
                print(qpc.piece, qpc.qnum)
            return

        del qObj_attacked.qnum[qObj_attacked_state]
        qObj.qnum[qObj_state][0] = move.to_square
        self.updateQboard(turn= not qObj.piece.symbol().isupper())
        return

    def splitMove(self, qObj, qObj_State, square1, square2):
        # //FIXME Don't allow pawns to split
        qObj.split(qObj_State, square1, square2)
        self.split_turn = False
        self.boardWidget.split_turn = False
        self.quantum_mode = False
        print('Split_complete')

    def entangleMove(self, move):
        # //BUG cannot entangle more than once
        # //BUG measure on two non-classical entangle pcs doesn't change the entagling obj
        # //BUG entangle dosnt create a copy on init location on board (without update)
        qObj, qObj_state = self.findQobj(move.from_square)

        qpc_squares = self.boardWidget.board.occupied & int(chess.SquareSet.between(move.from_square, move.to_square))
        if len(chess.SquareSet(qpc_squares)) >1:
            self.boardWidget.board.move_stack.pop()
            return
        
        if not self.boardWidget.split_turn:
            qpc_square = self.getSquareFromSquareSet(qpc_squares)
            qObj_other, qObj_other_state = self.findQobj(qpc_square)
            print('entangling', qObj.qnum[qObj_state], 'with', qObj_other.qnum[qObj_other_state])
            qObj.entangle_oneblock(qObj_state, move.to_square, qObj_other, qObj_other_state) 
            self.updateQboard(self.boardWidget.board.turn)
            print(qObj.qnum, 'other:', qObj_other.qnum)
        else:
            prev = self.previous_move
            qpc_squares2 = self.boardWidget.board.occupied & int(chess.SquareSet.between(prev.from_square, prev.to_square))
            if len(chess.SquareSet(qpc_squares2)) >1:
                self.boardWidget.board.move_stack.pop()
                return
            qpc_square = self.getSquareFromSquareSet(qpc_squares)
            qpc_square2 = self.getSquareFromSquareSet(qpc_squares2)

            qObj_other, qObj_other_state = self.findQobj(qpc_square)
            qObj_other2, qObj_other2_state = self.findQobj(qpc_square2)

            qObj.entangle_twoblock(qObj_state, move.to_square, prev.to_square, qObj_other, qObj_other_state, qObj_other2, qObj_other2_state)
            print('entangled2')

    def getSquareFromSquareSet(self, bigInt): #convinence method
        square_set = chess.SquareSet(bigInt)
        hi = []
        for i, boolV in enumerate(square_set.tolist()):
            if boolV:
                hi.append(i)
        if len(hi)<=1:
            return hi[0]
        else:
            raise error

    def findQobj(self, square):
        for pc in self.Qpieces:
            for state in pc.qnum.keys():
                if(pc.qnum[state][0] == square):
                    return pc, state

    def keyPressEvent(self, event): # press shift to toggle quantum mode
        if(event.key()==Qt.Key_Shift):
            if not self.boardWidget.split_turn:
                self.quantum_mode = not self.quantum_mode
            # self.split_turn = True

    def on_click_rel(self, w):
        try:
            a, _ = self.findQobj(self.boardWidget.squareOf(w))
            print(a.piece, a.qnum)
        finally:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    # mainWindow.boardWidget.setPieceAt(chess.D4,chess.Piece(chess.PAWN,chess.WHITE))    
    # mainWindow.boardWidget.moveMade.connect(mainWindow.sayHi)
    mainWindow.boardWidget.cellWidgetClickedSig.connect(mainWindow.on_click_rel)

    sys.exit(app.exec_())
